from .sanitize_html import (
    default_cleaner,
    markdown_to_raw_html,
    clean_raw_html,
)

import logging

log = logging.getLogger(__name__)


def make_cleaner_from_shop(shop):
    """Given a Shop return a bleach Cleaner object."""
    cleaner = default_cleaner()
    cleaner.link_protection = True
    if shop.domain_name:
        apex_domain_name = shop.domain_name.split(".")[-2:]
        cleaner.whitelist_domains.append("makepostsell.com")
        cleaner.whitelist_domains.append("my.makepostsell.com")
        cleaner.whitelist_domains.append(shop.domain_name)
        cleaner.whitelist_domains.append(apex_domain_name)
        cleaner.absolute_domain = shop.domain_name
    return cleaner


def markdown_to_html(data, shop=None):
    raw_html = markdown_to_raw_html(data)
    if shop:
        cleaner = make_cleaner_from_shop(shop)
    else:
        cleaner = default_cleaner()
    return clean_raw_html(raw_html, cleaner)
