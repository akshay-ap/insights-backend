from flask import Flask
from flask_cors import CORS

from config import config
import os
from routes.form import form_blueprint
from routes.user import user_blueprint
from routes.statistics import stats_blueprint

app = Flask(__name__)
CORS(app)

app.register_blueprint(form_blueprint, url_prefix="/api/v1/form")
app.register_blueprint(user_blueprint, url_prefix="/api/v1/user")
app.register_blueprint(stats_blueprint, url_prefix="/api/v1/stats")


@app.route("/")
def default():
    return f"insights-backend"


if __name__ == "__main__":
    app.run(debug=True)
