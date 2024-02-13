"""
I dedicate this file to removing the random crap canvas puts in its data.
Like random NBSPs. Gotta love those fuckers.
Thanks instructure btw for you state of the art WYSIWYG dogshit editor.
"""
from bs4 import BeautifulSoup

NBSP = " "


def remove_garbage_from_title(smelly_canvas_title: str) -> str:
    """
    Removes trailing tabs, spaces and NBSPs from smelly canvas titles.
    Parameters
    ----------
    smelly_canvas_title

    Returns
    -------
    str
        Clean title that is not smelly and has no NBSPs.
    """
    return (smelly_canvas_title
            .strip(f"\t {NBSP}")  # remove trailing garbage
            .replace(NBSP, " ")  # remove any other NBSPs
            )


def remove_stylesheets_from_html(smelly_html: str) -> str:
    """
    Removes all stylesheet links from `smelly_html`.

    Parameters
    ----------
    smelly_html
        The html to remove style sheets from
    Returns
    -------
        The non-smelly html with all stylesheet links removed
    """
    bs = BeautifulSoup(smelly_html, "html.parser")

    # remove links
    for ele in bs.find_all("link", {"rel": "stylesheet"}):
        ele.decompose()

    return str(bs)
