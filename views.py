import json

from flask import Blueprint, request, render_template
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