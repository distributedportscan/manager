from flask import Flask
from views.api import api 
from views.templates import templates

app = Flask(__name__,
        template_folder="template",
        static_url_path="/static")

app.register_blueprint(api)
app.register_blueprint(templates)

if __name__ == "__main__":
    app.run(debug=False,host="0.0.0.0")
