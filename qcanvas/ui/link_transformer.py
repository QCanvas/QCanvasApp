from typing import Sequence

from bs4 import BeautifulSoup

import qcanvas.db as db
from qcanvas.util.course_indexer import resource_helpers
from qcanvas.util.link_scanner import ResourceScanner


class LinkTransformer:
    # This is used to indicate that a "link" is actually a resource. The resource id is concatenated to this string.
    # It just has to be a valid url or qt does not send it to anchorClicked properly
    transformed_url_prefix = "data:,"

    def __init__(self, link_scanners: Sequence[ResourceScanner], files: dict[str, db.Resource]):
        self.link_scanners = link_scanners
        self.files = files

    def transform_links(self, html: str):
        doc = BeautifulSoup(html, 'html.parser')

        for element in doc.find_all(resource_helpers.resource_elements):
            for scanner in self.link_scanners:
                if scanner.accepts_link(element):
                    resource_id = f"{scanner.name}:{scanner.extract_id(element)}"
                    # todo make images actually show on the viewer page if they're downloaded
                    if resource_id in self.files:
                        file = self.files[resource_id]

                        substitute = doc.new_tag(name="a")
                        # Put the file id on the end of the url so we don't have to use the scanners to extract an id again..
                        # The actual url doesn't matter
                        substitute.attrs["href"] = f"{self.transformed_url_prefix}{file.id}"
                        substitute.string = f"{file.file_name} ({db.ResourceState.human_readable(file.state)})"

                        element.replace_with(substitute)
                    else:
                        if element.string is not None:
                            element.string += " (Failed to index)"

                    break

        return str(doc)
