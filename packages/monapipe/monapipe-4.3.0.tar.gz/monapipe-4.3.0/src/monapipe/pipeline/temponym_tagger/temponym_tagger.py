# SPDX-FileCopyrightText: 2022 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: CC0-1.0

from spacy.language import Language
from spacy.tokens import Span

from monapipe.pipeline.methods import add_extension


class TemponymTagger:
    """Component super class `TemponymTagger`."""

    assigns = {
        "doc.spans": "doc.spans['temponym']",
        "span._.temponym_norm": "temponym_span._.temponym_norm",
    }

    def __init__(self, nlp: Language):
        add_extension(Span, "temponym_norm")
