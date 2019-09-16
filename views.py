import json

from flask import Blueprint, abort, request, render_template, url_for, redirect
from bs4 import BeautifulSoup
import requests

from objects import cache

blueprint = Blueprint("views", __name__)

@cache.cached(timeout=30, key_prefix='fetch_userpage_%s')
def fetch_userpage(id):
	return requests.get("https://osu.ppy.sh/u/{}".format(id))

@blueprint.route("/")
def index():
	return render_template("index.html")

@blueprint.route("/users/<id>")
def userpage_redirect(id):
	return redirect(url_for("views.userpage", id=id))

@blueprint.route("/s/<id>")
def mapsetpage(id):
	return redirect("https://old.ppy.sh/s/{}".format(id))

@blueprint.route("/b/<id>")
def mappage(id):
	return redirect("https://old.ppy.sh/b/{}".format(id))

@blueprint.route("/u/<id>")
def userpage(id):
	mode = request.args.get("m", "0")
	try:
		mode = int(mode)
	except:
		mode = 0

	try:
		r = fetch_userpage(id)
		soup = BeautifulSoup(r.content)
		user_data = json.loads(soup.find("script", {"id": "json-user"}).text)
		extras_data = json.loads(soup.find("script", {"id": "json-extras"}).text)
		user = {
			"data": user_data,
			"extras": extras_data,
			"id": id,
		}
		return render_template("userpage.html", user=user)
	except Exception as e:
		return ("somethign fucked up: " + e)

@blueprint.route("/search/users", methods=["POST"])
def search_users():
	user = request.form.get("id")
	if user is None:
		return abort(404)
	else:
		return redirect(url_for("views.userpage", id=user))