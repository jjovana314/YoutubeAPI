""" Youtube research API. """

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

# todo: test this code
# todo: write documentation and comments
# ! reduce code complexity


class Search(Resource):
    def post(self):
        with open("schema.json", "r") as f:
            schema = loads(f.read())

        data = request.get_json()
        valid_keys = helper.outter_keys_valid + ["items"]
        data_outter = dict()

        for key in valid_keys:
            data_outter[key] = data.get(key, None)

        results = data["result"]

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
