from flask import Flask, render_template, g, jsonify, request
from bs4 import BeautifulSoup
import json
import sqlite3

# initialize the app
app = Flask(__name__, static_url_path='')


# declare a few global parameters to make life easier
DATABASE = './db/survey.db'
prime = 999959
generator = pow(2, 400, prime)


def initialize_db():
    """Ensure that the database has the CURRENT_KEY key and exists"""
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS survey_results (id INTEGER PRIMARY KEY AUTOINCREMENT, data BLOB);""")
    cur.close()
    db.close()


def get_db():
    """function that is called by a request handler to get a database connection, or create one if one doesn't exist in that connection"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    """function that is called by a request handler to destroy the database connection. Automatically called."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/404')
def error404():
    """Return the 404 page to the client"""
    return render_template('404.html')


@app.route('/')
def root():
    return render_template('survey.html', survey_name=survey_name)


@app.route('/survey/<survey_name>')
def survey(survey_name):
    """Render the survey page with the requested survey name to the client"""
    return render_template('survey.html', survey_name=survey_name)


@app.route('/api/results/<survey_name>', methods=['POST'])
def post_results(survey_name):
    """This endpoint accepts requests from the client that contain survey answers, and returns a code in the response body"""
    data = request.data
    try:
        db = get_db()
        cur = db.cursor()
        cur.execute("insert into survey_results values (?, ?)", (None, data))
        cur.execute("select last_insert_rowid() from survey_results")
        key_int = cur.fetchone()[0]
        cur.close()
        db.commit()
        response_object = {'code': "{:06d}".format(
            pow(generator, key_int, prime))}
        return jsonify(response_object)
    except Exception as e:
        print(e)
        return '{"code":"999959"}', 500


# @app.route('/api/commodity/parse-profile-html', methods=['POST'])
# def parse_profile_html():
#     soup = BeautifulSoup(request.data, 'html.parser')
#     inferences = []
#     for element in soup.find('ul').find_all('li'):
#         inference = element.find('div').find_all('div')[1].text
#        inferences.append(inference)
#     return jsonify(inferences)


# This little bit runs the server when you run this file
if __name__ == '__main__':
    initialize_db()
    app.run()
