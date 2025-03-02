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

"""Perform "pdfautonup" imposition."""

import pdfautonup

from .common import parse_format, parse_length, parse_resize


def impose(infile, outfile, arguments):
    """Perform imposition.

    :param dict arguments: Arguments got from the POST html method.
    """
    parameters = {}

    # Paper size
    parameters["size"] = parse_format(arguments, "form-pdfautonup")[1]

    # Orientation
    parameters["orientation"] = arguments.get("form-pdfautonup-orientation", "auto")

    # Algorithm
    parameters["algorithm"] = arguments.get("form-pdfautonup-algo", "fuzzy")

    # Repeat
    if arguments.get("form-pdfautonup-repeat") in ("fit", "auto"):
        parameters["repeat"] = arguments.get("form-pdfautonup-repeat")
    else:
        try:
            parameters["repeat"] = int(arguments.get("form-pdfautonup-repeat-value"))
        except ValueError:
            parameters["repeat"] = 1

    # Margin and gap
    if parameters["algorithm"] == "panel":
        parameters["more"] = {
            "margin": parse_length(arguments, "form-pdfautonup-panel", "margin"),
            "gap": parse_length(arguments, "form-pdfautonup-panel", "gap"),
        }

    # Argument "resize"
    infile = parse_resize(infile, arguments, "form-pdfautonup")

    pdfautonup.pdfautonup(
        files=[infile],
        output=outfile,
        **parameters,
    )
