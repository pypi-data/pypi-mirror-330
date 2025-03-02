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

"""Perform "wire" imposition."""

from pdfimpose.schema import wire

from .common import (
    parse_format,
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
    key, value = parse_format(arguments, "form-wire")
    parameters[key] = value

    # Argument "last"
    parameters["last"] = parse_last(arguments, "form-wire")

    # Arguments "imargin" and "omargin"
    parameters["imargin"] = parse_length(arguments, "form-wire", "imargin")
    parameters["omargin"] = parse_length(arguments, "form-wire", "omargin")

    # Argument "mark"
    parameters["mark"] = parse_marks(arguments, "form-wire", ("bind", "crop"))

    # Argument "resize"
    infile = parse_resize(infile, arguments, "form-wire")

    wire.impose(
        files=[infile for _ in range(parse_repeat(arguments, "form-wire"))],
        output=outfile,
        **parameters,
    )
