
from argparse import ArgumentParser

from modules import paths


def preload(parser:ArgumentParser)->None:
    """Add argument to commandline launch option."""
    parser.add_argument("--connect-save-path", type=str, help="url to remote storage", default=f"{paths.models_path}/connects")
