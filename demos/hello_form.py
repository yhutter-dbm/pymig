from flask import Flask
from flask import render_template
from flask import request
app = Flask("Hello Forms")


@app.route("/form/", methods=['GET', 'POST'])
def form_example():
    if request.method == "POST":
        person = request.form['vorname']
        return 'Hello ' + person + ' from form'
    return render_template("form.html")


@app.route("/hello/")
@app.route("/hello/<name>")
def say_hello(name=False):
    if name:
        return "Hello" + name + "!"
    else:
        return "Not Hello World again..."


if __name__ == "__main__":
    app.run(debug=True, port=5000)
