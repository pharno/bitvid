from bitvid.shared import get_es, get_es_index
from bitvid.lib import BitVidRestful

from flask import request
from pprint import pformat


class SearchResource(BitVidRestful.BitVidRestResource):
    def get(self):
        searchquery = request.args.get("q")

        seachresult = get_es().search(searchquery, index=get_es_index())

        actualhits = [hit["_source"] for hit in seachresult["hits"]["hits"]]
        # return pformat(actualhits, indent=4)
        return actualhits

def register(api):
    api.add_resource(SearchResource,"/search")
