from flask import Flask, render_template
from blueprints.address.address import address

app = Flask(__name__)
app.register_blueprint(address, url_prefix='/address')

@app.route("/")
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)