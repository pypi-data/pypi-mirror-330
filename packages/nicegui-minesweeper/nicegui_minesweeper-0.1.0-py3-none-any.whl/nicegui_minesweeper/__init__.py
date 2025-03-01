"""マインスイーパー"""

from importlib.metadata import metadata

import fire

from .minesweeper import Game, run_game

_package_metadata = metadata(str(__package__))
__version__ = _package_metadata["Version"]
__author__ = _package_metadata.get("Author-email", "")

__all__ = ["Game", "__author__", "__version__"]


def main() -> None:
    """スクリプト実行"""
    fire.Fire(run_game)
