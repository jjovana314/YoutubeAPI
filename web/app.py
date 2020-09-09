""" YouTube research API. """

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
from json import loads
from http import HTTPStatus
import helper


app = Flask(__name__)
api = Api(app)
client = MongoClient("mongodb://db:27017")
db = client.YoutubeDB
search = db["Search-results"]

# todo: write documentation and comments


class Search(Resource):
    """ YouTube data API. """
    def post(self):
        with open("schema.json", "r") as f:
            schema = loads(f.read())
        # idea is to separate data in two parts
        # first part is also separated in two parts
        # first part contains outter data (kind, etag, nextPageToken, regionCode, pageInfo)
        # also, first part contains items data, but we validate them differently
        # second part contains result data, with outter and items data, too
        # validation for second and first part is the same, schema is also the same
        # but for readability and debugging, we separate those two segments

        data = request.get_json()
        valid_keys = helper.outter_keys_valid + ["items"]
        data_outter = dict()

        for key in valid_keys:
            data_outter[key] = data.get(key, None)
        try:
            results = data["result"]
        except KeyError:
            return jsonify(
                {
                    "message": "please enter result data",
                    "code": helper.INVALID_SCHEMA
                }
            )

        all_data_valid = helper.validation(data_outter, results, schema)
        if isinstance(all_data_valid, tuple):
            return jsonify({"message": all_data_valid[0], "code": all_data_valid[1]})
        # all_data_valid is list
        outter_data, data_result, items_data, items_result = all_data_valid

        search.insert(
            {
                "Items": items_data,
                "Outter data": outter_data,
                "Results": {
                    "Outter data result": data_result,
                    "Items result": items_result
                }
            }
        )

        return jsonify(
            {
                "message": {
                    "items_data": items_data,
                    "outter_data": outter_data,
                    "data_result": data_result,
                    "items_result": items_result
                },
                "code": HTTPStatus.OK
            }
        )


api.add_resource(Search, "/search")
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
