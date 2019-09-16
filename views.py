import json

from flask import Blueprint, request, render_template
from bs4 import BeautifulSoup
import requests

blueprint = Blueprint("views", __name__)

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
		r = requests.get("https://osu.ppy.sh/u/{}".format(id))
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