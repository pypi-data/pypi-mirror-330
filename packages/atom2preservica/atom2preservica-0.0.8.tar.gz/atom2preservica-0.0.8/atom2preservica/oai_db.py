"""
atom2preservica

Synchronise metadata from AtoM to Preservica

author:     James Carr
licence:    Apache License 2.0

"""
import logging
from urllib.parse import urlparse

from pyAtoM import *
from requests import HTTPError
from sickle import Sickle
from tinydb import TinyDB, Query

logger = logging.getLogger(__name__)

class OaiDB:

    def __init__(self, oai_url: str, api_key: str):
        self.db = TinyDB('oai-pmh.json')
        self.ap_key = api_key
        self.oai_url = f"{oai_url}/;oai"


    def change_date(self, slug: str):
        query = Query()
        results = self.db.search(query.slug == slug)
        for result in results:
            oai_pmh_identifier = result['oai_pmh_identifier']
            sickle = Sickle(self.oai_url, headers={'X-OAI-API-Key': self.ap_key})
            record = sickle.GetRecord(identifier=oai_pmh_identifier, metadataPrefix='oai_dc')
            return record.header.datestamp


    def is_database_available(self):
        if os.path.exists('oai-pmh.json') and os.path.isfile('oai-pmh.json'):
            sickle = Sickle(self.oai_url, headers={'X-OAI-API-Key': self.ap_key})
            try:
                sickle.Identify()
            except HTTPError as e:
                logger.error(f"Unable to connect to OAI-PMH server. Checking for metadata updates is disabled")
                return False
            self.db = TinyDB('oai-pmh.json')
            if len(self.db) > 0:
                return True
        return False


    def create_database(self):
        query = Query()
        self.db.truncate()
        headers = {'X-OAI-API-Key': self.ap_key}
        sickle = Sickle(self.oai_url, headers=headers)
        records = sickle.ListRecords(metadataPrefix='oai_dc')
        for record in records:
            oai_pmh_identifier = record.header.identifier
            if not self.db.contains(query.oai_pmh_identifier == oai_pmh_identifier):
                slug: Optional[str] = None
                for ids in record.metadata['identifier']:
                    if ids.startswith('http://') or ids.startswith('https://'):
                        result = urlparse(ids)
                        slug = result.path.replace("/", "")
                if slug is not None:
                    self.db.insert({'oai_pmh_identifier': oai_pmh_identifier, 'slug': slug})

