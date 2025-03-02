# Copyright 2024 Louis Paternault

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

"""Hook to compile Babel catalog when building package."""

import subprocess

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    """Hook that compile babel catalog when building a package."""

    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        subprocess.run(
            "pybabel compile -d pdfimposeweb/translations", shell=True, check=True
        )
