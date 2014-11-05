from bitvid.shared import get_es, get_es_index
from bitvid.lib import BitVidRestful
from bitvid.errors import NotFound

from flask import request
from pprint import pformat
import pyelasticsearch

class SearchResource(BitVidRestful.BitVidRestResource):
    def get(self):
        query = request.args.get("q")
        start = int(request.args.get("page",0)) * 10


        searchquery = {
            "query": {
                "query_string": {
                    "query": query
                    }
            },
            "sort": {
                "created_at": {
                    "order": "desc"
                }
            },
            "from": start
        }

        try:
            seachresult = get_es().search(searchquery, index=get_es_index())
        except pyelasticsearch.exceptions.ElasticHttpNotFoundError:
            raise NotFound

        numresults = seachresult["hits"]["total"]
        actualhits = [hit["_source"] for hit in seachresult["hits"]["hits"]]
        # return pformat(actualhits, indent=4)
        return {"num":numresults,"hits":actualhits}

def register(api):
    api.add_resource(SearchResource,"/search")
