"""
This is a Flask web application that listens on 0.0.0.0, port 5000.
"""

from flask import Flask

app = Flask(__name__)

@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    Returns a greeting message.
    """
    return "Hello HBNB!"

@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Returns the name of the web application.
    """
    return "HBNB"

@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """
    Returns a string that includes the letter 'C' followed by the value of the 'text' parameter,
    with underscores replaced by spaces.
    """
    return "C {}".format(text.replace('_', ' '))

@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text):
    """
    Returns a string that includes the word 'Python' followed by the value of the 'text' parameter
    (or the default value "is cool" if no parameter is provided), with underscores replaced by spaces.
    """
    return "Python {}".format(text.replace('_', ' '))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
