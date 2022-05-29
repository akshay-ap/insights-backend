from flask import Flask
from config import config
import os
from routes.form import form_blueprint
from routes.user import user_blueprint

app = Flask(__name__)
app.register_blueprint(form_blueprint, url_prefix="/api/v1/form")
app.register_blueprint(user_blueprint, url_prefix="/api/v1/user")


@app.route("/")
def default():
    return f"insights-backend"


if __name__ == "__main__":
    app.run(debug=True)
