from flask import jsonify, send_file
from utils.constants import Constants


class Result:
    def process_result(self):
        pass


class FilePathResult(Result):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def process_result(self):
        return send_file(self.file_path,
                         mimetype=Constants.KML_MIMETYPE,
                         as_attachment=True,
                         download_name='shortest_path.kml'), 200


class JsonPathResult(Result):
    def __init__(self, path: list):
        self.path = path

    def process_result(self):
        return jsonify({'path': self.path}), 200
