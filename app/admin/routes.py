from flask import request, render_template, current_app, make_response
from flask.helpers import flash
from flask_login import login_required
from . import admin_bp
from .helper import csv_handler
from ..forms import ReportsFilterForm, AddOneUserForm, AddUsersByFileForm
from ..database.db_helper import (
    render_system_setting,
    render_records,
    render_users,
    add_users,
)
from ..users import admin_required


# The page allows admins to browse all reports and make response to the reports.
@admin_bp.route("/admin_dashboard/", methods=["GET", "POST"])
@admin_bp.route("/admin_dashboard/<int:page>", methods=["GET", "POST"])
@admin_required
@login_required
def dashboard_page(page=1):
    # cookies are used to save filter when user turns page
    form = ReportsFilterForm()
    if request.method == "GET":
        current_app.logger.info("GET /admin_dashboard")
        Filter = {}
        if username := request.cookies.get("username"):
            Filter["username"] = username
        if classnum := request.cookies.get("classnum"):
            Filter["classnum"] = classnum
        return render_template(
            "admin_dashboard.html",
            records=render_records(Filter=Filter, page=page),
            form=form,
            statuses=render_system_setting()[3],
        )
    if request.method == "POST":
        if form.validate_on_submit():
            current_app.logger.info("POST /admin_dashboard")
            Filter = dict()
            cookies = []
            if username := form.username.data:
                Filter["username"] = username
                cookies.append(("username", username))
            if classnum := form.classnum.data:
                Filter["classnum"] = classnum
                cookies.append(("classnum", classnum))

            response = make_response(
                render_template(
                    "admin_dashboard.html",
                    records=render_records(Filter),
                    form=form,
                    statuses=render_system_setting()[3],
                )
            )
            response.delete_cookie("username")
            response.delete_cookie("classnum")
            for cookie in cookies:
                response.set_cookie(*cookie, max_age=120)
            return response
        else:
            current_app.logger.info("POST /admin_dashboard: Invalid submit")


# The page allows admins to modify system setting. For example, they can add more buildings, offices and so on to the system.
@admin_bp.route("/system", methods=["GET"])
@admin_required
@login_required
def system_page():
    if request.method == "GET":
        current_app.logger.info("GET /system")
        buildings, items, offices, statuses = render_system_setting()
        return render_template(
            "system.html",
            buildings=buildings,
            items=items,
            offices=offices,
            statuses=statuses,
        )


# The page allows admins to add, edit and delete users.
@admin_bp.route("/manage_user/", methods=["GET", "POST"])
@admin_bp.route("/manage_user/<int:page>", methods=["GET", "POST"])
@admin_required
@login_required
def manage_user_page(page=1):
    form = AddOneUserForm()
    form_csv = AddUsersByFileForm()
    if request.method == "GET":
        # Render all users
        current_app.logger.info("GET /manage_user")
        return render_template(
            "manage_user.html", form=form, form_csv=form_csv, users=render_users(page=page)
        )
    if request.method == "POST":
        # Add user
        # Add one user
        if form.validate_on_submit():
            current_app.logger.info("POST /manage_user")
            data = {
                "username": form.username.data,
                "name": form.name.data,
                "classnum": form.classnum.data,
                "password": form.password.data,
                "email": form.email.data,
                "is_admin": int(form.classnum.data) == 0,
            }
            if len(data["password"]) < 6:
                flash(
                    "Password is too short (at least 6 characters).", category="alert"
                )
            elif already_exists := add_users(data):
                flash(", ".join(already_exists) + " 已經存在", category="alert")
        else:
            current_app.logger.info("POST /manage_user: Invalid submit")

        # Add users by csv
        if form_csv.validate_on_submit():
            current_app.logger.info("POST /manage_user")
            csv_file = form_csv.csv_file.data
            # data format: [{"username": "zxc", "name": "zxc", "password": "123", "classnum": "1400"}]
            if not (data := csv_handler(csv_file.read())):
                flash("Bad encoding.", category="alert")
            else:
                if already_exists := add_users(data):
                    flash(", ".join(already_exists) + " 已經存在", category="alert")
        else:
            current_app.logger.info("POST /manage_user: Invalid submit")
        return render_template(
            "manage_user.html", form=form, form_csv=form_csv, users=render_users()
        )
