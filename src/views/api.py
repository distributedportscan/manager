from controllers.rabbit import Messages
from controllers.normalizer import Reducer
from flask import Blueprint, request, jsonify

api = Blueprint('api',__name__,url_prefix="/api/")
m = Messages()
m.read("scan-result")

@api.route("/simple-scan",methods=["POST"])
def main():
    content = request.json
    if not content or not "iprange" in content or not "queue" in content:
        return jsonify({"msg":"invalid message"})
    subnets = Reducer(content["iprange"])
    queue = content["queue"]
    if queue == "scan-result" or not queue:
        return jsonify({"msg":"You can't sent messages to this queue"})
    messages = Messages()
    if not subnets:
        return jsonify({"msg":"Something goes wrong!"})
    for subnet in subnets:
        messages.send(queue,subnet)
    return jsonify({"msg":"Scan Started!"})

