from flask import Flask
from flask import render_template

app = Flask("Hello World")


@app.route("/hello")
def hello_world():
    return render_template("index.html", name="Yannick", elements=[1, 2, 3, 4, 5])


@app.route("/test")
def test():
    return "success"


if __name__ == "__main__":
    app.run(debug=True, port=5000)
