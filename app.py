from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_URL = "https://api.x.ai/v1/chat/completions"

VOICE_IDS = {
    "Damian": "bwFBqSVRgYJeueLra9wA",
    "Lenai": "ZUVYdNbdKEBF3OoO0Sil",
    "Victor": "BQTfjA8kEOa1pGp1jDxb",
    "Elena": "MMKfmW
