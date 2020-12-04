from flask import Flask
app = Flask(__name__)

@app.route("/login")
def hello():
    return dict(), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0')
