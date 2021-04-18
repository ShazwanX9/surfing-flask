# import os
import json
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .dbmodel import Note
from . import db

##############################################################################

view = Blueprint('view', __name__)

# random.choice(os.listdir("./static/BackgroundImages"))

@view.route("/")
@login_required
def home():
    return render_template ( 
                            "index.html", 
                            headerBgPath    = "static/BackgroundImages/" + "bg1.jpg", 
                            headerFgColor   = "#66ff33",
                            bgColor         = "#00fce",
                            user            = current_user
                            )

@view.route("/contact-us")
@login_required
def contact():
    return render_template ( 
                            "about.html", 
                            headerBgPath    = "static/BackgroundImages/" + "bg5.jpg", 
                            headerFgColor   = "#66ff33",
                            bgColor         = "#00fce",
                            user            = current_user
                            )

@view.route("/notes", methods=["GET", "POST"])
@login_required
def notes():
    if request.method == "POST":
        note = request.form.get("note")
        if len(note) < 1:
            flash("Note is too short!", category="error")
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note Append!", category="success")

    return render_template ( 
                            "notes.html", 
                            headerBgPath    = "static/BackgroundImages/" + "bg4.jpg", 
                            headerFgColor   = "#66ff33",
                            bgColor         = "#4a7555",
                            user            = current_user,
                            username        = current_user.username.upper()
                            )

@view.route("/delete-note", methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    noteId = note["noteId"]
    note = Note.query.get(noteId)

    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

