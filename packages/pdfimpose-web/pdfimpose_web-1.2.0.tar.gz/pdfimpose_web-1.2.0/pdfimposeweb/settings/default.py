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

"""Default settings for the application."""

import datetime
import secrets

# Set the temporary folder (in which user files and imposed files will be temporary stored).
# If `None`, a default one will be used.
# Example: TEMP_FOLDER = "/path/to/temporary/folder"
TEMP_FOLDER = None

# Maximum size (in bytes) of files that can be processed by the application.
MAX_CONTENT_LENGTH = 50_000_000

# Maximum number of times files are repeated.
# Set to 0 to allow arbitrary big numbers. Do not use 0 in production!
# Users could generate arbitrarily big PDF files, that will clog your server
# CPU, and fill your server memory.
MAX_FILE_REPEAT = 20

# Secret key used for securely signing default cookies.
# By default, a new one will be chosen at random each time the application restarts,
# which means users might experince bugs if you restart the application while they are browsing.
# Example: SECRET_KEY = 'da5ad311558575db9fbd534fd1fc34b1'
SECRET_KEY = secrets.token_hex(16)

# Set how long uploaded PDF files and imposed files should live before being removed,
# either by the cleaner thread (see below) or by manually calling ``pdfimposeweb.clean``.
# Example: PDF_LIFETIME = datetime.timedelta(hours=1)
PDF_LIFETIME = datetime.timedelta(hours=2)

# If ``True``, at the application startup, a thread is started to automatically
# remove outdated PDF files (depending on the `PDF_LIFETIME` option).
# If ``False``, one has to manually run ``pdfimposeweb.clean`` to remove
# outdated PDF files (in a crontab for instance).
RUN_CLEANER_THREAD = True

# Database URI. See the flask-sqlalchemy documentation to see how to connect to your database.
# https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/config/#connection-url-format
# By default, an in-memory sqlite database is used
# (which is reset everytime the application restarts).
SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

# Username and password to view the statistics page http://YOUR-DOMAIN-NAME/stats
# This is a quick-and-dirty page, with a quick-and-dirty authentication method.
# The only reason this page is protected is because it is badly coded, and
# might stress the database.
# By default, random username and password are chosen (basically forbidding
# anybody to see the page).
# This is experimental, and might be broken in later versions without notice.
BASIC_AUTH_USERNAME = secrets.token_hex(16)
BASIC_AUTH_PASSWORD = secrets.token_hex(16)

# Options for flask-limiter, which adds rate limiting to pdfimposeweb.
# Those are only some of the option that are recognisez by `flask_limiter`.
# See the full list of available options here:
# https://flask-limiter.readthedocs.io/en/stable/configuration.html#using-flask-config
# By default, data is stored in memory, but according to the `flask-limiter` documentation,
# this is designed for development and testing purpose, and should not be used in production.
RATELIMIT_DEFAULT = "200 per day, 50 per hour"
RATELIMIT_STORAGE_URI = "memory://"
RATELIMIT_STORAGE_OPTIONS = {}
