from controllers.rabbit import Messages
from flask import Blueprint, render_template

templates = Blueprint('templates',__name__,url_prefix="/")

@templates.route("/")
def indexPage():
    queues = Messages().queues()
    return render_template("index.html",queues=queues)

@templates.route("/scan-results")
def scanResult():
    return render_template("scan-result.html")

