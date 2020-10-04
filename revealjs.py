import flask
import os
import requests
import zipfile

BASE_PATH = "reveal.js-master"
PDF_EXPORT = """<!-- Printing and PDF exports -->
<script>var link=document.createElement("link");link.rel="stylesheet";link.type="text/css";
link.href = window.location.search.match(/print-pdf/gi) ? "css/print/pdf.css" : "css/print/paper.css";
document.getElementsByTagName("head")[0].appendChild(link);</script>"""
MULTIPLEX = """multiplex: {secret: null, id: '/id/',url: 'https://reveal-multiplex.glitch.me/'},
dependencies: [{ src: 'https://reveal-multiplex.glitch.me/socket.io/socket.io.js', async: true },
{ src: 'https://reveal-multiplex.glitch.me/client.js', async: true }],"""


def get_token():
    """
    get a multiplex token from https://reveal-multiplex.glitch.me
    :returns:
        (token, id)
    """
    resp = requests.get("https://reveal-multiplex.glitch.me/token")
    json = resp.json()
    return json["secret"], json["socketId"]


def download():
    """
    downloads the reveal.js project from github as a zip-file
    """
    resp = requests.get(
        "https://github.com/hakimel/reveal.js/archive/master.zip")
    with open("revealjs.zip", "wb") as f:
        f.write(resp.content)


def extract():
    """
    extracts the zip file to the current directory
    """
    with zipfile.ZipFile("revealjs.zip", "r") as zip_ref:
        zip_ref.extractall(".")


def create_client(socket_id):
    """
    create a client presentation
    :param:
        socket_id: the socket id optained with get_token()
    """
    with open(f"{BASE_PATH}/index.html") as f:
        f = str(f.read())
        if "print-pdf" not in f:
            f = f.replace("</head>", f"{PDF_EXPORT}</head>")
        if "multiplex" not in f:
            f = f.replace(
                "Reveal.initialize({", f"Reveal.initialize({{{MULTIPLEX}")
        f = f.replace("/id/", socket_id)
        with open(f"{BASE_PATH}/index.html", "w") as g:
            g.write(f)


def create_master(secret):
    """
    creates the fitting master presentation to the client presentation
    :param:
        socket_id: the socket id optained with get_token()
    """
    replaces = {"secret: null,": f'secret: "{secret}",',
                "glitch.me/client.js": "glitch.me/master.js"}
    with open(f"{BASE_PATH}/index.html") as f:
        f = f.read()
        if "print-pdf" not in f:
            raise RuntimeError("call create_clint first")
        for replace in replaces:
            f = f.replace(replace, replaces[replace])
        with open(f"{BASE_PATH}/master.html", "w") as g:
            g.write(f)


app = flask.Flask(__name__, static_url_path="", static_folder=BASE_PATH)


@app.route("/")
def index():
    return flask.send_file(f"{BASE_PATH}/index.html")


@app.route("/master")
def master():
    if not "master.html" in os.listdir(BASE_PATH):
        socket_id, secret = get_token()
        create_client(socket_id)
        create_master(secret)
    return flask.send_file(f"{BASE_PATH}/master.html")


def serve():
    """
    serve the given presentation
    """
    app.run("0.0.0.0")


def main():
    download()
    extract()
    socket_id, secret = get_token()
    create_client(socket_id)
    create_master(secret)
    serve()
