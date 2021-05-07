import logging
from flask import request, render_template, flash, current_app
from flask_login import login_required
from . import user_bp
from ..forms import ReportForm
from ..db_helper import render_buildings, render_items, add_record


@user_bp.route("/report", methods=["GET", "POST"])
@login_required
def report_page():
    form = ReportForm()
    form.building.choices = render_buildings()
    form.item.choices = render_items()
    if request.method == "GET":
        current_app.logger.info("GET /report")
        return render_template("report.html", form=form)
    if request.method == "POST":
        if form.validate_on_submit():
            current_app.logger.info("POST /report")
            building = form.building.data  # id
            location = form.location.data  # str
            item = form.item.data  # id
            description = form.description.data  # id
            add_record(building, location, item, description)
            flash("Successfully report.", "success")
            return render_template("report.html", form=form)
        else:
            current_app.logger.warning("POST /report: Invalid submit.")
            # Flask-wtf will return valid choice when the value is changed.
            for field, error in form.errors.items():
                for msg in error:
                    flash(msg, category="alert")
            return render_template("report.html", form=form)


@user_bp.route("/dashboard")
@login_required
def dashboard_page():
    pass
