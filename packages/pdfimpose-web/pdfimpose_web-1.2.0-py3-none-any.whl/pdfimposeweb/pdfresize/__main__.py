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

"""Resize PDF

This is a test program. It may contain bugs and change without notice. Do not use it.

However, this could be easily be turned into a proper package.
If you think this might be useful, send me an email, it should not take me that long…
"""

import sys

from . import resize_scale, resize_size


def main():
    """Main function: parse arguments, and run script."""
    size, source, dest = sys.argv[1:]
    if size.startswith("x"):
        resize_scale(source, dest, float(size[1:]))
    elif size.startswith("/"):
        resize_scale(source, dest, 1 / float(size[1:]))
    else:
        resize_size(source, dest, size)


if __name__ == "__main__":
    main()
