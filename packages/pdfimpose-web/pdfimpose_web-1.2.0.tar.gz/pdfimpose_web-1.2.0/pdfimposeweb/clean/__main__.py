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

"""Remove outdated files uploaded by users (original and imposed).

Run this from time to time (in a crontab for instance) if option ``RUN_CLEANER_THREAD`` is false.
"""

import sys

from flask import Flask

from .. import clean, settings


def main():
    """Main function: clean outdated files."""
    # Create a fake Flask application (to read settings)
    app = Flask("pdfimposeweb", instance_relative_config=True)
    settings.set_configuration(app)

    clean.clean(
        app.config["TEMP_FOLDER"],
        app.config["PDF_LIFETIME"],
    )


if __name__ == "__main__":
    if len(sys.argv) != 1:
        print(__doc__.strip())
        sys.exit(1)
    main()
