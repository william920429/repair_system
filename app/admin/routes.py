from flask import request, render_template
from flask_login import login_required
from . import admin_bp
from ..database.db_helper import render_system_setting
from ..users import admin_required


@admin_bp.route("/admin_dashboard", methods=["GET", "POST"])
@admin_required
@login_required
def dashboard_page():
    pass


@admin_bp.route("/system", methods=["GET", "POST"])
@admin_required
@login_required
def system_page():
    if request.method == "GET":
        buildings, items, offices, statuses = render_system_setting()
        return render_template(
            "system.html",
            buildings=buildings,
            items=items,
            offices=offices,
            statuses=statuses,
        )
    if request.method == "POST":
        pass
