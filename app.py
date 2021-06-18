from flask import Flask, render_template, Response, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return ("Hello World")


@app.route('/register')
def register_user():
    # return render_template("Registration_del.html")
    return render_template("Registration.html")

if __name__ == '__main__':
    # init_db()
    app.run(debug=True)