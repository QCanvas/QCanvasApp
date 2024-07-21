import logging


def set_levels(levels: dict[str, int]) -> None:
    for k, v in levels.items():
        logging.getLogger(k).setLevel(v)
