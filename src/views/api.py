from controllers.rabbit import Messages
from controllers.normalizer import Reducer
from flask import Blueprint, request, jsonify

api = Blueprint('api',__name__,url_prefix="/api/")
m = Messages()
m.read("subnet-scan-result")

@api.route("/simple-scan",methods=["POST"])
def main():
    content = request.json
    if not content or not "iprange" in content:
        return jsonify({"msg":"invalid message"})
    subnets = Reducer(content["iprange"])
    messages = Messages()
    if not subnets:
        return jsonify({"msg":"Something goes wrong!"})
    for subnet in subnets:
        messages.send("subnet-to-scan",subnet)
    return jsonify({"msg":"Scan Started!"})

