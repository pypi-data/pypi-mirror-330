# SPDX-FileCopyrightText: 2022 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: CC0-1.0

import os
from pathlib import Path

from torch import cuda

# Set the data directory to a custom location if the MONAPIPE_DATA environment variable is set
# Otherwise, use the default location
home = Path.home()
DATA_DIR = os.getenv("MONAPIPE_DATA")
if not DATA_DIR:
    DATA_DIR = os.path.join(home, ".monapipe_data")
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

DATAVERSE = {
    "api_token": "",
    "doi_attribution": "doi:10.25625/2D9CAV&version=1.0",
    "doi_event_classification": "doi:10.25625/0GUOMC&version=1.1",
    "doi_flair_gen_tagger_cv": "doi:10.25625/V7HTB8&version=2.1",
    "doi_generalizing_passages_identification_bert": "doi:10.25625/2PHXNC&version=1.1",
    "doi_heideltime": "doi:10.25625/SIPQEF&version=1.0",
    "doi_open_multilingual_wordnet": "doi:10.25625/LE57DV&version=1.0",
    "doi_parsing": "doi:10.25625/S2LPJP&version=1.1",
    "doi_reflective_passages_identification_bert": "doi:10.25625/0HXWYG&version=1.1",
}

HUGGINGFACE_HUB = {
    "fiction-gbert-char-ner": {
        "pretrained_model_name_or_path": "LennartKeller/fiction-gbert-large-droc-np-ner",
        "revision": "a75cf9fe8be4e45856049c289a0317c82f68c50a",
    }
}

LOCAL_PATHS = {
    "germanet": os.path.join(os.path.dirname(__file__), "..", "..", "..", "germanet"),
    "data_path": DATA_DIR,
    "data_path_container": "/app/data",
}

SETTINGS = {
    "spacy_max_length": 12000000,
    "torch_device": ("cuda" if cuda.is_available() else "cpu"),
}

# ports for the API services: internal/container and external/host
PORTS = {
    "flair_speech_tagger": {"container_port": 80, "host_port": 16000},
    "neural_event_tagger": {"container_port": 81, "host_port": 16001},
    "neural_attribution_tagger": {"container_port": 82, "host_port": 16002},
    "bert_character_ner": {"container_port": 83, "host_port": 16003},
    "neural_reflection_tagger": {"container_port": 84, "host_port": 16004},
    "neural_gen_tagger": {"container_port": 85, "host_port": 16005},
    "flair_gen_tagger": {"container_port": 86, "host_port": 16006},
}
