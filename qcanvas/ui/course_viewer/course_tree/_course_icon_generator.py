import itertools
import logging
import random

from cachetools import cached
from qtpy.QtCore import QByteArray
from qtpy.QtGui import QColor, QPainter, QPixmap
from qtpy.QtSvg import QSvgRenderer

_logger = logging.getLogger(__name__)
_transparent = QColor("#00000000")
_colours = [
    QColor(f"#{colour}")
    for colour in [
        "2ad6cb",
        "2d50ed",
        "7a10e4",
        "c61aaf",
        "d91b1b",
        "c7541b",
        "facd07",  # facd07
        "a9cf12",
    ]
]


class CourseIconGenerator:
    @staticmethod
    @cached(cache={})
    def get_for_term(term_id: str) -> "CourseIconGenerator":
        return CourseIconGenerator(term_id)

    def __init__(self, term_id: str):
        shuffled = list(_colours)

        # This is the dumbest way I've ever seen a language implement setting a seed for a RNG.
        # WTF python?! Why???
        random.seed(term_id)
        random.shuffle(shuffled)

        self._iterator = itertools.cycle(shuffled)

    def get_icon(self) -> QPixmap:
        return _create_icon(self._get_colour())

    def _get_colour(self) -> QColor:
        return next(self._iterator)


@cached(cache={}, key=lambda colour: colour.name(QColor.NameFormat.HexRgb))
def _create_icon(base_colour: QColor) -> QPixmap:
    dark_colour = QColor.fromHslF(
        base_colour.hslHueF(),
        base_colour.hslSaturationF(),
        base_colour.lightnessF() * 0.6875,
    )

    result_pixmap = QPixmap(256, 256)
    result_pixmap.fill(_transparent)

    with (painter := QPainter(result_pixmap)):
        svg = _create_svg_from_colours(base_colour, dark_colour)
        svg.render(painter)

    return result_pixmap


def _create_svg_from_colours(light_colour: QColor, dark_colour: QColor) -> QSvgRenderer:
    # Original SVG is from SVGRepo.com
    return QSvgRenderer(
        QByteArray(
            f"""
            <?xml version="1.0" encoding="UTF-8" standalone="no"?>
            <svg width="800px" height="800px" viewBox="0 0 24 24" >
             <g transform="translate(0 -1028.4)">
              <path d="m3 8v2 1 3 1 5 1c0 1.105 0.8954 2 2 2h14c1.105 0 2-0.895 2-2v-1-5-4-3h-18z" transform="translate(0 1028.4)" fill="{dark_colour.name()}"/>
              <path d="m3 1035.4v2 1 3 1 5 1c0 1.1 0.8954 2 2 2h14c1.105 0 2-0.9 2-2v-1-5-4-3h-18z" fill="#ecf0f1"/>
              <path d="m3 1034.4v2 1 3 1 5 1c0 1.1 0.8954 2 2 2h14c1.105 0 2-0.9 2-2v-1-5-4-3h-18z" fill="#bdc3c7"/>
              <path d="m3 1033.4v2 1 3 1 5 1c0 1.1 0.8954 2 2 2h14c1.105 0 2-0.9 2-2v-1-5-4-3h-18z" fill="#ecf0f1"/>
              <path d="m5 1c-1.1046 0-2 0.8954-2 2v1 4 2 1 3 1 5 1c0 1.105 0.8954 2 2 2h2v-1h-1.5c-0.8284 0-1.5-0.672-1.5-1.5s0.6716-1.5 1.5-1.5h12.5 1c1.105 0 2-0.895 2-2v-1-5-4-3-1c0-1.1046-0.895-2-2-2h-4-10z" transform="translate(0 1028.4)" fill="{dark_colour.name()}"/>
              <path d="m8 1v18h1 9 1c1.105 0 2-0.895 2-2v-1-5-4-3-1c0-1.1046-0.895-2-2-2h-4-6-1z" transform="translate(0 1028.4)" fill="{light_colour.name()}"/>
             </g>
            </svg>
            """.strip().encode()
        )
    )
