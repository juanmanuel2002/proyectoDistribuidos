from flask import Flask
from pymongo import MongoClient
app = Flask(__name__)
client = MongoClient("mongodb:27017")

from . import view

