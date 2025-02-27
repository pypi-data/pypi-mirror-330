"""
AtoM2Preservica

Synchronise metadata from AtoM to Preservica

author:     James Carr
licence:    Apache License 2.0

"""
import argparse
import os.path
from datetime import datetime
import xml.etree.ElementTree
from pyAtoM import *
from pyPreservica import *

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

ATOM_SLUG = "AToM-Slug"
ATOM_SYNC_DATE = "AToM-Sync-Date"

folder_cache = dict()



def create_folder(entity: EntityAPI, atom_item, parent_ref, security_tag: str):
    """
    Create a new folder in Preservica from an AtoM item

    :param entity:
    :param atom_item:
    :param parent_ref:
    :param security_tag:
    :return:
    """

    title = None
    reference_code = None
    if 'reference_code' in atom_item:
        reference_code = atom_item['reference_code']
        title = reference_code

    slug = atom_item['slug']

    description = atom_item['title'].replace('\xa0', ' ').replace("&", "&amp;")

    print(f"Creating folder: {title, description, parent_ref}")

    folder = entity.create_folder(title=title, description=description, security_tag=security_tag, parent=parent_ref)

    entity.add_identifier(folder, ATOM_SLUG, slug)
    entity.add_identifier(folder, ATOM_SYNC_DATE, datetime.now().isoformat())
    if reference_code:
        entity.add_identifier(folder, "Reference code", reference_code)

    add_asset_metadata(entity, folder, atom_item)

    folder_cache[slug] = folder

    logger.info(f"Created New Folder: {folder.title}")

    return folder

def create_parent_series(atom_client: AccessToMemory, entity: EntityAPI, slug: str, security_tag: str, parent_collection: Folder = None):
    """

    Create the parent series of folders in Preservica starting at the parent_collection level

    :param atom_client:
    :param entity:
    :param slug:
    :param security_tag:
    :param parent_collection:
    :return:
    """

    folder = does_folder_exist(entity, slug)
    if folder is not None:
        return folder

    item = atom_client.get(slug)
    parent_slug: Optional[str] = item.get('parent', None)
    if parent_slug is None:
        print(f"Creating Folder with slug: {parent_slug}")
        return create_folder(entity, item, parent_collection.reference, security_tag)

    parent_item = atom_client.get(parent_slug)
    parent_item_slug = parent_item['slug']

    assert parent_slug == parent_item_slug

    parent_folder = does_folder_exist(entity, parent_item_slug)
    if parent_folder is not None:
        slug_id = item['slug']
        print(f"Creating Folder with slug: {slug_id}")
        return create_folder(entity, item, parent_folder.reference, security_tag)
    else:
        return create_parent_series(atom_client, entity, parent_item_slug, security_tag)


def get_levels(atom_client: AccessToMemory, atom_record, levels):
    """
    Get a list of levels of description from the parent of the AtoM record

    :param atom_client:
    :param atom_record:
    :param levels:
    :return:
    """
    if 'parent' in atom_record:
        parent_slug = atom_record['parent']
        if parent_slug is not None:
            levels.append(parent_slug)
            parent_record = atom_client.get(parent_slug)
            get_levels(atom_client, parent_record, levels)
        return
    else:
        return


def does_folder_exist(entity: EntityAPI, slug: str):
    """
    Check if a parent collection already exists in Preservica

    :param entity:
    :param slug:
    :return:
    """

    # Check the cache first
    if slug in folder_cache:
        return folder_cache[slug]

    entities = entity.identifier(ATOM_SLUG, slug)
    if len(entities) > 1:
        for e in entities:
            folder = entity.entity(e.entity_type, e.reference)
            if folder.entity_type == EntityType.FOLDER:
                folder_cache[slug] = folder
                return folder_cache[slug]
    if len(entities) == 1:
        folder = entities.pop()
        if folder.entity_type == EntityType.FOLDER:
            folder_cache[slug] = folder
            return folder_cache[slug]
        else:
            return None
    else:
        return None


def get_folder(entity: EntityAPI, atom_record, atom_client: AccessToMemory, security_tag: str, parent_collection: Folder):
    """

    Find the parent for the record which is going to be linked, create the parent series of folders if they do not exist

    :param entity:
    :param atom_record:
    :param atom_client:
    :param security_tag:
    :param parent_collection:
    :return:
    """
    parent_slug = atom_record['parent']
    if parent_slug is not None:
        folder = does_folder_exist(entity, parent_slug)
        if folder is not None:
            return folder

    folder_slugs = list()
    get_levels(atom_client, atom_record, folder_slugs)
    folder_slugs.reverse()
    for slug in folder_slugs:
        folder_cache[slug] = create_parent_series(atom_client, entity, slug, security_tag, parent_collection)

    return folder_cache[parent_slug]


def add_asset_metadata(client: EntityAPI, entity: Entity, atom_record: dict):
    """
    
    Create a Dublin Core XML document from the ATOM Record and add it to the Preservica entity
    
    :param client: 
    :param entity: 
    :param atom_record: 
    :return: 
    """""

    xip_object = xml.etree.ElementTree.Element('oai_dc:dc', {"xmlns:oai_dc": "http://www.openarchives.org/OAI/2.0/oai_dc/",  "xmlns:dc": "http://purl.org/dc/elements/1.1/"})

    if 'title' in atom_record:
        xml.etree.ElementTree.SubElement(xip_object, "dc:title").text = atom_record['title']

    xml.etree.ElementTree.SubElement(xip_object, "dc:contributor").text = ""

    if 'place_access_points' in atom_record:
        for place in atom_record['place_access_points']:
            xml.etree.ElementTree.SubElement(xip_object, "dc:coverage").text = place

    if 'creators' in atom_record:
        for creator in atom_record['creators']:
            xml.etree.ElementTree.SubElement(xip_object, "dc:creator").text = creator['authorized_form_of_name']

    if 'dates' in atom_record:
        for date in atom_record['dates']:
            xml.etree.ElementTree.SubElement(xip_object, "dc:date").text = date['date']

    if 'scope_and_content' in atom_record:
        xml.etree.ElementTree.SubElement(xip_object, "dc:description").text = atom_record['scope_and_content']

    if 'extent_and_medium' in atom_record:
        xml.etree.ElementTree.SubElement(xip_object, "dc:format").text = atom_record['extent_and_medium']

    xml.etree.ElementTree.SubElement(xip_object, "dc:identifier").text = atom_record['slug']

    if 'reference_code' in atom_record:
        xml.etree.ElementTree.SubElement(xip_object, "dc:identifier").text = atom_record['reference_code']

    if 'languages_of_material' in atom_record:
        for lang in atom_record['languages_of_material']:
            xml.etree.ElementTree.SubElement(xip_object, "dc:language").text = lang

    xml.etree.ElementTree.SubElement(xip_object, "dc:publisher").text = ""

    if 'repository' in atom_record:
        xml.etree.ElementTree.SubElement(xip_object, "dc:relation").text = atom_record['repository']

    if 'conditions_governing_access' in atom_record:
        xml.etree.ElementTree.SubElement(xip_object, "dc:rights").text = atom_record['conditions_governing_access']

    if 'archival_history'  in atom_record:
        xml.etree.ElementTree.SubElement(xip_object, "dc:source").text = atom_record['archival_history']

    if 'subject_access_points' in atom_record:
        for subject in atom_record['subject_access_points']:
            xml.etree.ElementTree.SubElement(xip_object, "dc:subject").text = subject

    if 'name_access_points' in atom_record:
        for subject in atom_record['name_access_points']:
            xml.etree.ElementTree.SubElement(xip_object, "dc:subject").text = subject

    if 'level_of_description' in atom_record:
        xml.etree.ElementTree.SubElement(xip_object, "dc:type").text = atom_record['level_of_description']

    xml_request = xml.etree.ElementTree.tostring(xip_object, encoding='utf-8')

    client.add_metadata(entity, "http://www.openarchives.org/OAI/2.0/oai_dc/", xml_request.decode('utf-8'))

def synchronise(entity: EntityAPI, search: ContentAPI, folder: Folder, atom_client: AccessToMemory, parent_collection: Folder, security_tag: str):
    """
    Synchronise metadata from items in ATOM onto Preservica Assets


    :param security_tag:        The Preservica security tag to use for new collections
    :param parent_collection:   The Preservica collection where new ATOM levels of description will be added
    :param atom_client:         The Access to Memory client
    :param entity:              The Preservica client
    :param search:              The Preservica search client
    :param folder:              The Preservica folder to search for assets
    :return:
    """

    # Search for assets in Preservica with the AtoM slug
    filter_values = {"xip.document_type": "IO", "xip.identifier": ATOM_SLUG}
    if folder is not None:
        filter_values["xip.parent_hierarchy"] = folder.reference

    num_hits: int = search.search_index_filter_hits(query="%", filter_values=filter_values)

    logger.info(f"Found {num_hits} objects to check")


    for hit in search.search_index_filter_list(query="%", filter_values=filter_values):
        reference: str = hit['xip.reference']
        asset: Asset = entity.asset(reference)
        atom_slug = None
        sync_date = None
        for key, value in identifiersToDict(entity.identifiers_for_entity(asset)).items():
            if key == ATOM_SYNC_DATE:
                sync_date = value
            if key == ATOM_SLUG:
                atom_slug = value
        if atom_slug is not None:
            if sync_date is None:
                atom_record = atom_client.get(slug=atom_slug)
                if atom_record is not None:
                    parent_folder = get_folder(entity, atom_record, atom_client, security_tag, parent_collection)
                    logger.info(f"Found AtoM slug: {atom_slug} for asset: {reference}")
                    if 'title' in atom_record:
                        asset.title = atom_record['title']
                    if 'scope_and_content' in atom_record:
                        asset.description = atom_record['scope_and_content']
                    entity.save(asset)
                    entity.add_identifier(asset, ATOM_SYNC_DATE, datetime.now().isoformat())
                    add_asset_metadata(entity, asset, atom_record)
                    entity.move(asset, parent_folder)
            else:
                logger.info(f"Asset: {asset.title} already synchronised on {sync_date}")


def init(args):
    """
    Parse the command line arguments

    :param args: The command line arguments
    :return:
    """
    cmd_line = vars(args)

    username = cmd_line['preservica_username']
    password = cmd_line['preservica_password']
    server = cmd_line['preservica_server']
    # create the pyPreservica objects
    if (username is not None) and (password is not None) and (server is not None):
            logger.info(f"Using credentials from command line")
            entity: EntityAPI = EntityAPI(username=username, password=password, server=server)
            search: ContentAPI = ContentAPI(username=username, password=password, server=server)
    else:
        if os.path.exists('credentials.properties') and os.path.isfile('credentials.properties'):
            entity: EntityAPI = EntityAPI()
            search: ContentAPI = ContentAPI()
        else:
            logger.error(f"Cannot find credentials.properties file")
            sys.exit(1)

    security_tag: str = cmd_line['security_tag']

    collection = cmd_line['search_collection']
    if collection is not None:
        folder: Folder = entity.folder(collection)
        logger.info(f"Synchronise metadata for objects in collection: {folder.title}")
    else:
        logger.info(f"Synchronise metadata for objects from all collections")

    new_collections = cmd_line["new_collections_root"]
    new_folder_location = Optional[Folder]
    if new_collections is not None:
        new_folder_location: Folder = entity.folder(new_collections)
        logger.info(f"New Collections will be added below: {new_folder_location.title}")
    else:
        logger.info(f"New Collections will be added at the Preservica root")

    atom_server: str = cmd_line["atom_server"]
    if atom_server.startswith("https://"):
        atom_server = atom_server.replace("https://", "")

    if (cmd_line["atom_api_key"] is None) and ((cmd_line["atom_user"] is None) or (cmd_line["atom_password"] is None)):
        logger.error("You must provide either an AtoM API Key or a username and password")
        sys.exit(1)

    if cmd_line["atom_api_key"] is not None:
        atom_client = AccessToMemory(api_key=cmd_line["atom_api_key"],  server=atom_server)
    else:
        atom_client = AccessToMemory(username=cmd_line["atom_user"], password=cmd_line["atom_password"], server=atom_server)


    synchronise(entity, search, collection, atom_client, new_folder_location, security_tag)

def main():
    """
      Entry point for the module when run as python -m AtoM2Preservica

      Sets up the command line arguments and starts the sync process

      :return: None

      """
    cmd_parser = argparse.ArgumentParser(
        prog='atom2preservica',
        description='Synchronise metadata and levels of description from a Access To Memory (AtoM) instance to Preservica',
        epilog='')

    cmd_parser.add_argument("-a", "--atom-server", type=str, help="The AtoM server URL", required=True)

    cmd_parser.add_argument("-k", "--atom-api-key", type=str, help="The AtoM API Key, if not using username and password", required=False)

    cmd_parser.add_argument("-au", "--atom-user", type=str, help="The AtoM username, if not using the API Key", required=False)
    cmd_parser.add_argument("-ap", "--atom-password", type=str, help="The AtoM password, if not using the API Key", required=False)

    cmd_parser.add_argument("-st", "--security-tag", type=str, default="open",
                            help="The Preservica security tag to use for new collections, defaults to open",
                            required=False)

    cmd_parser.add_argument("-c", "--search-collection", type=str,
                            help="The Preservica parent collection uuid to search for linked assets, ignore to Synchronise the entire repository",
                            required=False)

    cmd_parser.add_argument("-cr", "--new-collections-root", type=str,
                            help="The parent Preservica collection to add new AtoM levels of description, ignore to add new collections at the root",
                            required=False)

    cmd_parser.add_argument("-u", "--preservica-username", type=str,
                            help="Your Preservica username if not using credentials.properties", required=False)
    cmd_parser.add_argument("-p", "--preservica-password", type=str,
                            help="Your Preservica password if not using credentials.properties", required=False)
    cmd_parser.add_argument("-s", "--preservica-server", type=str,
                            help="Your Preservica server domain name if not using credentials.properties",
                            required=False)

    args = cmd_parser.parse_args()

    init(args)


if __name__ == "__main__":
    sys.exit(main())