'''
    Nlp-Provider  Nlp singleton for Altspell plugins.
    Copyright (C) 2025  Nicholas Johnson

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import spacy


try:
    # Load spaCy without any unnecessary components
    shared_nlp = spacy.load('en_core_web_sm')
except OSError:
    from spacy.cli import download  # pylint: disable=import-outside-toplevel
    download('en_core_web_sm')
    shared_nlp = spacy.load('en_core_web_sm')
