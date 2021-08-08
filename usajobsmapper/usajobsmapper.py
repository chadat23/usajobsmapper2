# all the imports
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash


# create our little application :)
app = Flask(__name__)
app.config.from_object('config')

@app.route('/')
def index():
    return render_template('index.html', content={})

if __name__ == '__main__':
    app.run()
