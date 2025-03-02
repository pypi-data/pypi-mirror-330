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

"""Generic functions and data about imposition"""

import importlib
import pathlib
import pkgutil
import sys

LAYOUTS = {
    name: getattr(module, "impose")
    for name, module in (
        (name, importlib.import_module(f".{name}", __name__))
        for finder, name, ispkg in pkgutil.iter_modules(__path__)
    )
    if hasattr(module, "impose")
}


def impose(layout, infile, outfile, arguments):
    """Dispatch arguments to the relevant imposition module."""
    LAYOUTS[layout](infile, outfile, arguments)
