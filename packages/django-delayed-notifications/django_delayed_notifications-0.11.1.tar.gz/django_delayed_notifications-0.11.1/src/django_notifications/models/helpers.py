"""
helpers for :mod:`django_notifications.models` application.

:creationdate: 31/03/2022 14:08
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: django_notifications.models.helpers
"""

import logging

import bs4
from bs4.element import Tag

__author__ = "fguerin"
logger = logging.getLogger(__name__)


def get_debug_head(soup: bs4.BeautifulSoup, to: list[str]) -> Tag:
    """
    Get the DEBUG head for email debugging.

    :param soup: html body to convert
    :param to: list of recipients
    :return: html head
    """

    def get_email_line(i: int, email: str) -> Tag:
        """Create a line for the email."""
        new_tag = soup.new_tag("li", id=f"id_to_list_item_{i:04d}")
        new_tag.string = email
        return new_tag

    debug_tag = soup.new_tag(
        "div",
        id="id_debug",
        style="display: block; border: 1px solid red; background-color: #ffcccc;",
    )
    to_list_tag = soup.new_tag("ul", id="id_to_list")
    to_list_tag.contents.extend([get_email_line(i, email) for i, email in enumerate(to)])
    title_tag = soup.new_tag("h3")
    title_tag.string = "DEBUG"
    debug_tag.contents = [
        title_tag,
        to_list_tag,
    ]
    return debug_tag


def get_debug_html_body(html_body: str, to: list[str]) -> str:
    """
    Convert html body for email debugging.

    :param html_body: html body to convert
    :param to: list of recipients
    :return: html body with <pre> tags
    """
    soup = bs4.BeautifulSoup(html_body, "html.parser")
    if soup is None or soup.body is None:
        logger.warning("get_debug_html_body() Unable to parse html body")
        return html_body
    debug_tag = get_debug_head(soup, to)
    soup.body.insert(0, debug_tag)
    return soup.decode(pretty_print=True)
