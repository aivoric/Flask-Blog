"""Error pages located here."""
from flask import render_template
from app.errors import bp
from app import db

@bp.app_errorhandler(404)
def not_found_error(error):
    """ 404 error page """
    return render_template('errors/404.jinja'), 404

@bp.app_errorhandler(500)
def internal_error(error):
    """ 500 error page """
    db.session.rollback()
    return render_template('errors/500.jinja'), 500