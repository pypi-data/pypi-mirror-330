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

debug:
	python -m flask --app pdfimposeweb run --debug

run:
	python -m flask --app pdfimposeweb run

.PHONY: babel
babel:
	@echo "# Babel translation how-to"
	@echo
	@echo "- Extract strings to translate:"
	@echo "  pybabel extract -F babel.cfg -o messages.pot ."
	@echo
	@echo "- Update French translations catalog (replace update with init for first translation of a new language)"
	@echo "  pybabel update -i messages.pot -d pdfimposeweb/translations -l fr"
	@echo
	@echo "- Manually update translations"
	@echo "  $$EDITOR pdfimposeweb/translations/fr/LC_MESSAGES/messages.po"
	@echo
	@echo "- Compile translations"
	@echo "  pybabel compile -d pdfimposeweb/translations"
