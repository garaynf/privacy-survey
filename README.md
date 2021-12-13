# Survey Website

This is a website that is useful for conducting surveys. The goal is to make a self-hosted survey page that can be extended to have additional surveys without too much work.

It uses the following libraries:

- [Flask](https://flask.palletsprojects.com/en/2.0.x/) as a web framework
- [BerkeleyDB](https://docs.jcea.es/berkeleydb/latest/) to store survey results
- [Survey.js](https://surveyjs.io/) as a framework for building surveys
- [Knockout](https://knockoutjs.com/) as a web frontend framework

## Setup

To set yourself up here, first make sure you have Python and pip installed. I recommend also using a [virtual environment](https://docs.python.org/3/tutorial/venv.html) as best practice to keep the packages for this project isolated from the rest of your system's python. Setting it up with `python3 -m venv venv; source venv/bin/activate;` puts you in the context of a clean python install, which you can then leave with `deactivate`.

Once you have python configured, install all of the dependencies with `make dependencies`.
This (as of right now) only runs a pip install command that installs all of the python packages you need.

You should now be able to run the server with `make dev`. If you visit it, the home page will (as of right now) tell you "Sorry, that page doesn't exist"

## How does this all work?

When you run `make dev`, it runs the program in `app.py` which starts a server that runs on your machine. It'll print out the URL for the server when it runs. Let's call it `$SERVER`. The server will host all of the files in the `./static` folder and also listen for requests to resources specified in the `@app.route` decorators in the `app.py` file. Of particular importance is the `/survey/<survey_name>` path. This means server listens for requests to `$SERVER/survey/$NAME` for any value of name. Once it gets that request, it gives the client the HTML in `templates/survey.html`, with the survey name replaced to be the `$NAME` value from earlier.

The client, upon getting that HTML has to get a few other resources from the static folder (CSS and JS files). It also requests the file `/surveys/$NAME.json`. The server will try to look in the `./static/surveys/` folder for a file called `$NAME.json`. If it doesn't exist, the client redirects to the 404 not found page. If it does exist, the client loads that JSON object as a SurveyJS form description and lets the user fill it out.

When the user hits submit on the form, the user's data is sent to the server at `/api/results/$NAME`. The server saves the data in the database and gives the user a response code that can then be turned into the survey recruiting system. The code 999959 indicates a database error and the code 999960 indicates a server error. All other codes are derived by taking the user's record ID in the BerkeleyDB and taking 635386 to that value modulo 999959. This is a bit of group arithmetic to make the numbers inscruitable to the user while being easily reversible to us.

## Directory Structure

- `./static` contains files that the server should just serve unaltered
- `./templates` contains [Jinja2 templates](https://jinja.palletsprojects.com/en/3.0.x/templates/). These are files the server will be giving to the user with small changes, which have template parameters.
- `.gitignore`, `Makefile`, `requirements.txt` are all files to make working with the project easier technically.
- `LICENSE` and `README.md` make working with the project easer non-technically.
