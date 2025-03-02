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

"""Delete temporary files older than one day."""

import datetime
import pathlib
import queue
import re
import shutil
import threading
import time

RE_DATE = re.compile("^[0-9]{8}-[0-9]{6}-")


def clean(download: pathlib.Path, lifetime: datetime.timedelta):
    """Remove outdated files from the download folder.

    :param pathlib.Path download: Directory to clean.
    :param datetime.timedelta lifetime: Name of files older than this are removed.
    :return: Name of folders that are too young to be removed, together with their removal datetime.
    :rtype: Tuple[pathlib.Path, datetime.datetime]
    """
    young = set()
    for folder in download.iterdir():
        if folder.is_dir() and (match := RE_DATE.match(str(folder.name))):
            deathtime = (
                datetime.datetime.strptime(match.group(), "%Y%m%d-%H%M%S-") + lifetime
            )
            if deathtime < datetime.datetime.now():
                shutil.rmtree(download / folder.name, ignore_errors=True)
            else:
                young.add((download / folder.name, deathtime))
    return young


def _thread_cleaner(toremove: queue.Queue):
    """Read names from the queue, and remove the corresponding files."""
    while True:
        date, path = toremove.get()
        time.sleep(max(0, (date - datetime.datetime.now()).total_seconds()))
        shutil.rmtree(path, ignore_errors=True)


def launch_thread_cleaner(app) -> queue.Queue:
    """Launch the cleaner thread, and return a queue of files to clean."""
    toremove = queue.Queue()
    for folder, deathtime in clean(
        app.config["TEMP_FOLDER"], app.config["PDF_LIFETIME"]
    ):
        toremove.put((deathtime, folder))
    threading.Thread(
        target=_thread_cleaner,
        args=(toremove,),
        daemon=True,
    ).start()
    return toremove
