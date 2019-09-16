from flask import Flask
app = Flask(__name__)

@app.context_processor
def utility_processor():
    def format_activity(activity):
        ty = activity["type"]
        username = activity["user"]["username"]
        userurl = activity["user"]["url"]
        if activity.get("beatmap"):
            beatmaptitle = activity["beatmap"]["title"]
            beatmapurl = activity["beatmap"]["url"]
        if activity.get("beatmapset"):
            beatmapsettitle = activity["beatmapset"]["title"]
            beatmapseturl = activity["beatmapset"]["url"]
        if ty == "rankLost":
            return "<b><a href='{}'>{}</a></b> has lost first place on <a href='{}'>{}</a>".format(userurl, username, beatmapurl, beatmaptitle)
        elif ty == "rank":
            rank = int(activity["rank"])
            special = rank <= 50
            return ("<b><a href='{}'>{}</a></b> achieved ".format(userurl, username) +
                            ("<b>" if special else "") +
                            "rank #{}".format(rank) +
                            ("</b>" if special else "") +
                            " on <a href='{}'>{}</a>".format(beatmapurl, beatmaptitle))
        elif ty == "beatmapsetUpdate":
            return "<b><a href='{}'>{}</a></b> has updated the beatmap \"<a href='{}'>{}</a>\"".format(userurl, username, beatmapseturl, beatmapsettitle)
        elif ty == "beatmapsetRevive":
            return "<a href='{}'>{}</a> has been revived from eternal slumber by <b><a href='{}'>{}</a></b>".format(beatmapseturl, beatmapsettitle, userurl, username)
        elif ty == "beatmapsetApprove":
            approval = activity["approval"]
            return "<a href='{}'>{}</a> by <b><a href='{}'>{}</a></b> has just been {}!".format(beatmapseturl, beatmapsettitle, userurl, username, approval)
        elif ty == "userSupportGift":
            return "<b><a href='{}'>{}</a></b> has received the gift of OSU supporter!".format(userurl, username)
        else:
            return str(activity)
    return dict(format_activity=format_activity)

import api
app.register_blueprint(api.blueprint, url_prefix="/api")

import views
app.register_blueprint(views.blueprint)