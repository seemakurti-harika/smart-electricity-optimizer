from flask import Flask

from models.database import init_db

app = Flask(__name__)

app.secret_key = "smartenergysecret"

# INITIALIZE DATABASE
init_db()

# IMPORT ROUTES
from routes.auth import *
from routes.dashboard import *
from routes.appliances import *
from routes.reminders import *
from routes.home import *
from routes.reports import *


if __name__ == '__main__':

    app.run(debug=True)