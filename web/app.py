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

        try:
            helper.validate_schema(schema, data_outter)
        except helper.InvalidSchemaError as ex:
            return jsonify({"message": ex.args[0], "code": ex.args[1]})
        outter_data = helper.caller(data, helper.send_data_values)
        items_data = helper.caller(data, helper.send_items_values)

        if isinstance(outter_data, KeyError) or isinstance(outter_data, ValueError):
            return jsonify({"message": outter_data.args[0], "code": outter_data.args[1]})
        if isinstance(items_data, KeyError) or isinstance(outter_data, ValueError):
            return jsonify({"message": items_data.args[0], "code": items_data.args[1]})

        results = data["result"]
        try:
            helper.validate_schema(schema, results)
        except helper.InvalidSchemaError as ex:
            return jsonify({"message": ex.args[0], "code": ex.args[1]})
        data_result = helper.caller(results, helper.send_data_values)
        items_result = helper.caller(results, helper.send_items_values)

        if isinstance(data_result, KeyError) or isinstance(data_result, ValueError):
            return jsonify({"message": data_result.args[0], "code": data_result.args[1]})

        if isinstance(items_result, KeyError) or isinstance(items_result, ValueError):
            return jsonify({"message": items_result.args[0], "code": items_result.args[1]})

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
