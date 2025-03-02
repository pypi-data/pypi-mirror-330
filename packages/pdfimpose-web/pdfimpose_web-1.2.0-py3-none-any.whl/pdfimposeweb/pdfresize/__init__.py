# Copyright 2024-2025 Louis Paternault
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

"""Resize PDF (e.g. from A4 to A5)."""

import typing

import papersize
import pymupdf


def resize_scale(source: str, dest: str, scale: float):
    """Scale PDF (multiply or divide width and length by a scaling factor)"""
    sourcepdf = pymupdf.open(source)
    destpdf = pymupdf.open()

    for sourcepage in sourcepdf:
        x1, y1, x2, y2 = sourcepage.mediabox
        destpdf.new_page(
            width=scale * (x2 - x1), height=scale * (y2 - y1)
        ).show_pdf_page(
            pymupdf.Rect((0, 0), (scale * (x2 - x1), scale * (y2 - y1))),
            sourcepdf,
            sourcepage.number,
            keep_proportion=False,
            rotate=sourcepage.rotation,
        )

    destpdf.set_metadata(sourcepdf.metadata)  #  pylint: disable=no-member
    destpdf.save(dest)


def resize_size(source: str, dest: str, size: str | tuple[float]):
    """Resize PDF (to the size given in argument)"""
    sourcepdf = pymupdf.open(source)
    destpdf = pymupdf.open()

    if isinstance(size, str):
        size = map(float, papersize.parse_papersize(size))
    width, height = size

    for sourcepage in sourcepdf:
        destpdf.new_page(width=width, height=height).show_pdf_page(
            pymupdf.Rect((0, 0), (width, height)),
            sourcepdf,
            sourcepage.number,
            keep_proportion=False,
            rotate=sourcepage.rotation,
        )

    destpdf.set_metadata(sourcepdf.metadata)  #  pylint: disable=no-member
    destpdf.save(dest)
