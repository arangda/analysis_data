import sys

from flask import Flask
import os
from config import basedir

if getattr(sys, 'frozen', False):
    template_folder = os.path.join(basedir, 'app','templates')
    static_folder = os.path.join(basedir, 'app','static')
    app = Flask(__name__, template_folder = template_folder,\
                          static_folder = static_folder)
else:
    app = Flask(__name__)
app.config.from_object('config')

from app import views