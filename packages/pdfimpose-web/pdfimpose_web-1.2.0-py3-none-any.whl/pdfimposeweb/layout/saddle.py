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

"""Perform "saddle" imposition"""

from pdfimpose.schema import saddle

from .common import (
    parse_bind,
    parse_format,
    parse_group,
    parse_last,
    parse_length,
    parse_marks,
    parse_repeat,
    parse_resize,
)


def impose(infile, outfile, arguments):
    """Perform imposition.

    :param dict arguments: Arguments got from the POST html method.
    """
    parameters = {}

    # Get paper size
    key, value = parse_format(arguments, "form-saddle")
    parameters[key] = value

    # Argument "last"
    parameters["last"] = parse_last(arguments, "form-saddle")

    # Arguments "imargin" and "omargin"
    parameters["imargin"] = parse_length(arguments, "form-saddle", "imargin")
    parameters["omargin"] = parse_length(arguments, "form-saddle", "omargin")

    # Argument "mark"
    parameters["mark"] = parse_marks(arguments, "form-saddle", ("bind", "crop"))

    # Argument "bind"
    parameters["bind"] = parse_bind(arguments, "form-saddle")

    # Argument "group"
    parameters["group"] = parse_group(arguments, "form-saddle")

    # Argument "resize"
    infile = parse_resize(infile, arguments, "form-saddle")

    saddle.impose(
        files=[infile for _ in range(parse_repeat(arguments, "form-saddle"))],
        output=outfile,
        **parameters,
    )
