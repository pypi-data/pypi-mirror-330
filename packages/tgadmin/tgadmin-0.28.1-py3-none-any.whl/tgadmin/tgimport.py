# SPDX-FileCopyrightText: 2024 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import logging
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import PurePath
from typing import List

from tgclients import TextgridCrud, TextgridCrudException
from tgclients.databinding import MetadataContainerType
from tgclients.databinding import Object as TextgridObject
from xsdata.exceptions import ConverterWarning, ParserError

from .utils import (
    NAMESPACES,
    PARSER,
    PC_NAMESPACES,
    RDF_RESOURCE,
    base_uri_from,
    is_aggregation,
    is_allowed_in_project_root,
    is_edition,
    is_portalconfig,
    is_readme,
    write_imex,
)

log = logging.getLogger(__name__)


def aggregation_import(
    tgcrud: TextgridCrud,
    sid: str,
    project_id: str,
    filenames: List[str],
    threaded: bool,
    ignore_warnings: bool,
):
    """Import an TextGrid aggregation (or collection or edition).

    Imports recursively with given tgcrud and sid into specified project

    Args:
        tgcrud (TextgridCrud): an instance of tgcrud
        sid (str): Session ID
        project_id (str): Project ID
        filenames (List[str]): path of the aggregation file to import
        threaded (bool): wether to use multiple threads for crud upload
        ignore_warnings (bool): continue also in case of warnings from tgcrud

    Raises:
        TextgridImportException: with a human understandable message  in case of
                                 errors (opening files, crud communication, etc)

    Returns:
        dict: results of import process (location of imex file, num objects uploaded, root aggregation uri)
    """
    imex_map: dict = {}
    portalconfig_file = None
    tguri = ''
    aggregation_filename = 'upload'  # will be name of last aggregation uploaded for imex filename for backwards compatibility

    for filename in filenames:
        filepath = PurePath(filename)
        meta = metafile_to_object(filepath, referenced_in=filename)
        if not is_allowed_in_project_root(meta):
            raise TextgridImportException(f"File '{filename}' is not of type aggregation")

        if is_portalconfig(meta):
            # portalconfig needs to go after avatar img / xslt upload for uri rewrite
            portalconfig_file = filepath
        elif is_readme(meta):
            upload_file(tgcrud, sid, project_id, filepath, imex_map, ignore_warnings)
        else:
            tguri = handle_aggregation_upload(
                tgcrud,
                sid,
                project_id,
                filepath,
                meta,
                imex_map,
                threaded,
                ignore_warnings,
            )
            aggregation_filename = filename

    # finally rewrite and upload portalconfig
    if portalconfig_file:
        handle_portalconfig_upload(
            tgcrud, sid, project_id, portalconfig_file, imex_map, ignore_warnings
        )

    imex_filename = aggregation_filename + '.imex'
    write_imex(imex_map, imex_filename)

    return {
        'objects_uploaded': len(imex_map),
        'imex_location': imex_filename,
        'tguri': tguri,
    }


def handle_portalconfig_upload(tgcrud, sid, project_id, filename, imex_map, ignore_warnings):
    meta = metafile_to_object(filename, referenced_in=filename)
    content = rewrite_portalconfig_file(filename, imex_map, ignore_warnings)
    tguri = upload_modified(
        tgcrud,
        sid,
        project_id,
        content,
        meta,
        ignore_warnings,
        filename,
        default_namespace=PC_NAMESPACES['pc'],
    )
    imex_map[filename] = tguri
    return tguri


def handle_aggregation_upload(
    tgcrud, sid, project_id, filename, agg_meta, imex_map, threaded, ignore_warnings
):
    # if aggregation is edition then upload related work object
    if is_edition(agg_meta):
        work_path = PurePath(PurePath(filename).parent, agg_meta.edition.is_edition_of)
        tguri = upload_file(
            tgcrud,
            sid,
            project_id,
            work_path,
            imex_map,
            ignore_warnings,
            referenced_in=filename,
        )
        agg_meta.edition.is_edition_of = tguri  # update isEditionOf

    agg_xml = ET.parse(filename)
    agg_xml_root = agg_xml.getroot()

    if not threaded:
        for ore_aggregates in agg_xml_root.findall('.//ore:aggregates', NAMESPACES):
            _handle_upload_op(
                tgcrud,
                sid,
                project_id,
                filename,
                ore_aggregates,
                imex_map,
                threaded,
                ignore_warnings,
            )
    else:
        with ThreadPoolExecutor(max_workers=10) as ex:
            futures = [
                ex.submit(
                    _handle_upload_op,
                    tgcrud,
                    sid,
                    project_id,
                    filename,
                    ore_aggregates,
                    imex_map,
                    threaded,
                    ignore_warnings,
                )
                for ore_aggregates in agg_xml_root.findall('.//ore:aggregates', NAMESPACES)
            ]

            for future in as_completed(futures):
                result = future.result()

    tguri = upload_modified(
        tgcrud, sid, project_id, agg_xml_root, agg_meta, ignore_warnings, filename
    )
    # operations on dict seem to be thread safe in cpython
    # https://docs.python.org/3/glossary.html#term-global-interpreter-lock
    imex_map[filename] = tguri
    return tguri


def _handle_upload_op(
    tgcrud,
    sid,
    project_id,
    filename,
    ore_aggregates,
    imex_map,
    threaded,
    ignore_warnings,
):
    data_path = PurePath(PurePath(filename).parent, ore_aggregates.attrib[RDF_RESOURCE])
    meta = metafile_to_object(data_path, referenced_in=filename)

    if is_aggregation(meta):
        tguri = handle_aggregation_upload(
            tgcrud,
            sid,
            project_id,
            data_path,
            meta,
            imex_map,
            threaded,
            ignore_warnings,
        )
    else:
        tguri = upload_file(tgcrud, sid, project_id, data_path, imex_map, ignore_warnings)

    # TODO: is this thread safe?
    ore_aggregates.set(RDF_RESOURCE, base_uri_from(tguri))  # update the xml with the uri


def upload_file(
    tgcrud,
    sid,
    project_id: str,
    data_path: PurePath,
    imex_map: dict,
    ignore_warnings,
    referenced_in: str = '',
) -> str:
    """Upload an object and its related .meta file to specified project."""
    if data_path in imex_map:
        log.info(f'file already uploaded: {data_path.name} - has uri {imex_map[data_path]}')
        return imex_map[data_path]
    else:
        log.info(f'uploading unmodified file with meta: {data_path.name}')

    try:
        with open(data_path, 'rb') as the_data:
            mdobj = metafile_to_object(data_path)
            # tgcrud wants a MetadataContainerType, see https://gitlab.gwdg.de/dariah-de/textgridrep/textgrid-python-clients/-/issues/76
            mdcont = MetadataContainerType()
            mdcont.object_value = mdobj

            res = tgcrud.create_resource(sid, project_id, the_data.read(), mdcont)
            handle_crud_warnings(res, data_path.name, ignore_warnings)

            tguri = res.object_value.generic.generated.textgrid_uri.value
            imex_map[data_path] = tguri
            return tguri
    except FileNotFoundError:
        raise TextgridImportException(
            f"File '{data_path}' not found, which is referenced in '{referenced_in}'"
        )
    except TextgridCrudException as error:
        handle_crud_exception(error, sid, project_id, data_path)
    return ''


def handle_crud_warnings(res, filename, ignore_warnings):
    for crudwarn in res.object_value.generic.generated.warning:
        log.warning(f' ⚠️ Warning from tgcrud for {filename}: {crudwarn}')
    if len(res.object_value.generic.generated.warning) > 0 and not ignore_warnings:
        raise TextgridImportException(
            'Stopped import. Please fix your input or try again with --ignore-warnings'
        )


def upload_modified(
    tgcrud,
    sid,
    project_id: str,
    etree_data,
    metadata,
    ignore_warnings,
    filename='',
    default_namespace=None,
) -> str:
    """Upload in memory xml and it textgrid-metadata (possibly modified) as textgridobject."""
    log.info(
        f"uploading modified file '{filename}' with title: {metadata.generic.provided.title[0]}"
    )

    if (
        metadata.generic.provided.format == 'text/tg.edition+tg.aggregation+xml'
        and not metadata.edition.is_edition_of.startswith('textgrid:')
    ):
        message = f'no valid textgrid uri referenced in isEditionOf field of {filename}.meta, it is set to: {metadata.edition.is_edition_of}'
        if not ignore_warnings:
            raise TextgridImportException(message)
        else:
            log.warning(f'{message} - but ignore warnings is enabled')

    ET.register_namespace('', default_namespace)
    ET.register_namespace('xml', 'http://www.w3.org/XML/1998/namespace')
    data_str = ET.tostring(etree_data, encoding='utf8', method='xml')

    mdcont = MetadataContainerType()
    mdcont.object_value = metadata
    try:
        res = tgcrud.create_resource(sid, project_id, data_str, mdcont)
        handle_crud_warnings(res, filename, ignore_warnings)
    except TextgridCrudException as error:
        handle_crud_exception(error, sid, project_id, filename)
    return res.object_value.generic.generated.textgrid_uri.value


def rewrite_portalconfig_file(portalconfig_file, imex_map, ignore_warnings):
    data_path = PurePath(portalconfig_file).parent
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
    the_dataXML = ET.parse(portalconfig_file, parser).getroot()

    # modify avatar element
    avatar_location = the_dataXML.find('pc:avatar', PC_NAMESPACES)
    check_path_and_rewrite(imex_map, data_path, avatar_location, ignore_warnings)
    # optionally modify xslt element
    xslt_tag = the_dataXML.find('pc:xslt', PC_NAMESPACES)
    if xslt_tag:
        # look into each tag (only <html> as of now) and rewrite locations
        for html_xslt_location in xslt_tag.findall('pc:html', PC_NAMESPACES):
            check_path_and_rewrite(imex_map, data_path, html_xslt_location, ignore_warnings)

    return the_dataXML


def check_path_and_rewrite(imex_map, data_path, element, ignore_warnings):
    """Check if the path referenced in 'element' is already contained in 'imax_map'.

    Exchange element content if so, fail if not
    """
    path = PurePath(data_path / element.text)
    if path in imex_map:
        element.text = imex_map[path]
    else:
        message = f"'{element.text}' is referenced in portalconfig, but not found in import. Did you forget to add a collection with additional assets?"
        if not ignore_warnings:
            raise TextgridImportException(message)
        else:
            log.warning(f'{message} - but ignore warnings is enabled')


def metafile_to_object(filename: PurePath, referenced_in: str = '') -> TextgridObject:
    metafile_path = PurePath(f'{filename}.meta')
    try:
        with open(metafile_path, 'rb') as meta_file:
            try:
                meta: TextgridObject = PARSER.parse(meta_file, TextgridObject)
            except ParserError:  # try parsing again as metadatacontainertype
                meta_file.seek(0)  # rewind
                metadata: MetadataContainerType = PARSER.parse(meta_file, MetadataContainerType)
                meta = metadata.object_value
        return meta
    except FileNotFoundError:
        if filename == referenced_in:
            raise TextgridImportException(
                f"File '{filename}.meta' not found, which belongs to '{filename}'"
            )
        else:
            raise TextgridImportException(
                f"File '{filename}.meta' not found, which belongs to '{filename}' and is referenced in '{referenced_in}'"
            )
    except ConverterWarning as warning:
        # TODO ConverterWarning is not thrown, only shown
        raise TextgridImportException(f'xsdata found a problem: {warning}')


def handle_crud_exception(error, sid, project_id, filename):
    # TODO: we can check both here, if sessionid is valid, and if project is existing and accessible, for better feedback
    # tgrud should also communicate the cause
    # error mapping
    # * 404 - project not existing
    # * 401 - sessionid invalid
    # * 500 - something went terribly wrong (invalid metadata)

    msg = f"""
        tgcrud responded with an error uploading '{filename}'
        to project '{project_id}'
        with sessionid starting...ending with '{sid[0:3]}...{sid[-3:]}'

        """
    if '404' in str(error):
        msg += 'Are you sure the project ID exists?'
    elif '401' in str(error):
        msg += 'Possibly the SESSION_ID is invalid'
    elif '500' in str(error):
        msg += f"""A problem on tgcrud side - is you metadata valid?
        Please check {filename}.meta"""
    else:
        msg += f'new error code found'

    msg += f"""

        ----
        Error message from tgcrud:
        {error}
    """

    raise TextgridImportException(msg)


class TextgridImportException(Exception):
    """Exception thrown by tgimport module."""
