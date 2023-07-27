from flask import Flask
from streamlit.server.server import Server

def run():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return 'Hello from Streamlit'

    server = Server(app)
    server.start()
