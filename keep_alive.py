from threading import Thread
from flask import Flask

app = Flask('')


@app.route("/")
def foo():
    return "PyBot-2 Is Running!!"


def run():
    app.run(debug=False, host="0.0.0.0", port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()
