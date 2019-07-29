from flask import Blueprint, render_template

templates = Blueprint('templates',__name__,url_prefix="/")

@templates.route("/")
def indexPage():
    return render_template("index.html")

@templates.route("/scan-results")
def scanResult():
    return render_template("scan-result.html")

