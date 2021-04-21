from flask import Flask, escape, request
import socket
app = Flask(__name__)

@app.route('/')
def get_hostname():
    return "Aplicación servida desde hostname: "+socket.gethostname()
