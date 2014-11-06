from bitvid.shared import get_es, get_es_index, thumb_url, videofile_webserver_path
from bitvid.lib import BitVidRestful
from bitvid.errors import NotFound
from bitvid.models.Video import Video, ConvertedVideo

from flask import request
from flask.ext.restful import fields, marshal
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

        print seachresult
        numresults = seachresult["hits"]["total"]
        actualhits = [self._transform(hit) for hit in seachresult["hits"]["hits"]]
        # return pformat(actualhits, indent=4)
        return {"num":numresults,"hits":actualhits}


    def _transform(self, hit):
        typ = hit["_type"]
        transformator = getattr(self,"_transform"+typ)
        return transformator(hit)

    def _transformVideo(self, hit):
        video = hit["_source"]
        video["thumb"] = thumb_url(video["token"])
        videos = {}
        videomedias = self._getVideoMedias(video["token"])

        for videomedia in videomedias["videos"]:
            if videomedia["codec"] not in videos.keys() or \
                            videomedia["height"] > \
                            videos[videomedia["codec"]]["height"]:
                print(videomedia["codec"])
                videomedia["path"] = videofile_webserver_path(video["token"],
                                               videomedia["height"],
                                               videomedia["codec"])
                videos[videomedia["codec"]] = videomedia

        video["medias"] = videos
        return video

    def _getVideoMedias(self, videoID):
        marshal_fields = {"videos": fields.List(fields.Nested(ConvertedVideo.marshal_fields))}
        video = Video.query.filter_by(token=videoID).first()
        if not video:
            raise ResourceNotFoundException()

        return marshal({"videos": video.convertedVideos}, marshal_fields)
def register(api):
    api.add_resource(SearchResource,"/search")
