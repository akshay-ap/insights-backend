import logging

from flask import Flask
from flask_cors import CORS
from logging.handlers import TimedRotatingFileHandler

from config import config
import os
from routes.form import form_blueprint
from routes.user import user_blueprint
from routes.statistics import stats_blueprint

log_filename = os.path.join('logs', 'app.log')
handler = TimedRotatingFileHandler(filename=log_filename, when="D", interval=1)
logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(message)s",
    level=logging.DEBUG,
    handlers=[handler],
)

app = Flask(__name__)
CORS(app)

app.register_blueprint(form_blueprint, url_prefix="/api/v1/form")
app.register_blueprint(user_blueprint, url_prefix="/api/v1/user")
app.register_blueprint(stats_blueprint, url_prefix="/api/v1/stats")


@app.route("/")
def default():
    return f"insights-backend"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
