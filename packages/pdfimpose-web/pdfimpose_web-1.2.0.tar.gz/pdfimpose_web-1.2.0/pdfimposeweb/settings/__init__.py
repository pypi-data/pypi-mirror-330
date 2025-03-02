# Copyright 2024 Louis Paternault
#
# This file is part of pdfimpose-web.
#
# Pdfimpose-web is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# Pdfimpose-web is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License
# along with pdfimpose-web. If not, see <https://www.gnu.org/licenses/>.

"""Tools to process settings of the application."""

import pathlib

import flask


def set_configuration(app: flask.Flask):
    """Read configuration, and fix default options."""
    app.config.from_object("pdfimposeweb.settings.default")
    app.config.from_envvar("PDFIMPOSEWEB_SETTINGS", silent=True)

    # Fix default options
    if app.config["TEMP_FOLDER"] is None:
        app.config["TEMP_FOLDER"] = pathlib.Path(app.instance_path) / "temp"
    app.secret_key = app.config["SECRET_KEY"]
