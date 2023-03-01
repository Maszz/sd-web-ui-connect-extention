import os
from modules import paths


def preload(parser):
    parser.add_argument("--connect-save-path", type=str, help="url to remote storage", default=os.path.join(paths.models_path, 'connects'))
