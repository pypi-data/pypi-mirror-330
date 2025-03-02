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

"""Common functions related to layout (mainly about parsing arguments)."""

from pdfimpose import DEFAULT_PAPER_SIZE

from .. import pdfresize


def parse_format(arguments, prefix, *, default=DEFAULT_PAPER_SIZE):
    """Parse arguments about paper size."""
    try:
        if arguments[f"{prefix}-format"] == "standard":
            return "size", arguments[f"{prefix}-format-standard"]
        if arguments[f"{prefix}-format"] == "custom":
            return (
                "size",
                "{}{}x{}{}".format(  #  pylint: disable=consider-using-f-string
                    arguments[f"{prefix}-format-custom-width-value"],
                    arguments[f"{prefix}-format-custom-width-unit"],
                    arguments[f"{prefix}-format-custom-height-value"],
                    arguments[f"{prefix}-format-custom-height-unit"],
                ),
            )
        if arguments[f"{prefix}-format"] == "signature":
            return "signature", (
                int(arguments[f"{prefix}-format-signature-width"]),
                int(arguments[f"{prefix}-format-signature-height"]),
            )
    except (KeyError, ValueError):
        return default
    return default


def parse_length(arguments, prefix, key, *, default=0):
    """Parse argument about length (value + unit)."""
    try:
        return "{}{}".format(  #  pylint: disable=consider-using-f-string
            arguments[f"{prefix}-{key}-value"],
            arguments[f"{prefix}-{key}-unit"],
        )
    except KeyError:
        return default


def parse_marks(arguments, prefix, marks, *, default=None):
    """Parse argument about crop and bind marks."""
    try:
        enabled = []
        for mark in marks:
            if arguments[f"{prefix}-marks-{mark}"] == "on":
                enabled.append(mark)
        return enabled
    except KeyError:
        return default


def parse_last(arguments, prefix, *, default=0):
    """Parse arguments about last pages."""
    try:
        return int(arguments[f"{prefix}-last"])
    except (KeyError, ValueError):
        return default


def parse_bind(arguments, prefix, *, default="left"):
    """Parse arguments about binding edge."""
    try:
        return arguments[f"{prefix}-bind"]
    except KeyError:
        return default


def parse_group(arguments, prefix, *, default=1):
    """Parse argument about grouping sheets of paper."""
    try:
        if arguments[f"{prefix}-group"] == "some":
            return int(arguments[f"{prefix}-group-value"])
        if arguments[f"{prefix}-group"] == "no":
            return 1
        if arguments[f"{prefix}-group"] == "all":
            return 0
    except (KeyError, ValueError):
        return default
    return default


def parse_repeat(arguments, prefix):
    """Parse argument about input repetition."""
    try:
        return int(arguments[f"{prefix}-repeat"])
    except (KeyError, ValueError):
        return 1


def parse_resize(infile, arguments, prefix):
    """Parse argument about resizing input, and perform resize.

    Return the input file name (original name if no resizing is done, resized
    file if file has been resized).
    """
    newfile = infile.with_stem(f"{infile.stem}-resized")
    try:
        if arguments[f"{prefix}-resize"] == "dont":
            return infile
        if arguments[f"{prefix}-resize"] == "standard":
            pdfresize.resize_size(
                infile, newfile, arguments[f"{prefix}-resize-standard"]
            )
            return newfile
        if arguments[f"{prefix}-resize"] == "custom":
            pdfresize.resize_size(
                infile,
                newfile,
                "{}{}x{}{}".format(  #  pylint: disable=consider-using-f-string
                    arguments[f"{prefix}-resize-custom-width-value"],
                    arguments[f"{prefix}-resize-custom-width-unit"],
                    arguments[f"{prefix}-resize-custom-height-value"],
                    arguments[f"{prefix}-resize-custom-height-unit"],
                ),
            )
            return newfile
        if arguments[f"{prefix}-resize"] == "scale":
            pdfresize.resize_scale(
                infile, newfile, float(arguments[f"{prefix}-resize-scale"])
            )
            return newfile
        return infile
    except (KeyError, ValueError):
        return infile
