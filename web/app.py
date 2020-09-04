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


class Search(Resource):
    def post(self):
        with open("schema.json", "r") as f:
            schema = loads(f)

        data = request.get_json()
        valid_keys = helper.outter_keys_valid + data["items"]
        data_outter = dict()

        for key in valid_keys:
            data_outter[key] = data.get(key, None)
        try:
            helper.validate_schema(schema, data_outter)
        except helper.InvalidSchemaError as ex:
            return jsonify({"message": ex.args[0], "code": ex.args[1]})

        try:
            data_instance = helper.send_data_values(data)
        except (KeyError, ValueError) as ex:
            return jsonify({"message": ex.args[0], "code": HTTPStatus.BAD_REQUEST})

        try:
            items_data = helper.sent_items_values(data)
        except (KeyError, ValueError) as ex:
            return jsonify({"message": ex.args[0], "code": HTTPStatus.BAD_REQUEST})

        return jsonify(
            {
                "message": "data is passed validation",
                "code": HTTPStatus.OK
            }
        )


api.add_resource(Search, "/search")
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
