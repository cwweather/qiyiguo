from flask import Flask
from flask import render_template, redirect
from flask import request

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("lookup.html", mobile="0")


@app.route("/lookup", methods=["POST", "GET"])
def lookup():
    mobile = request.form.get("mobile")
    url = "http://kd.dh.cx/a5aeb/{mobile}/".format(
        mobile=mobile
    )
    return redirect(url)


if __name__ == '__main__':
    app.run(host='0.0.0.0')