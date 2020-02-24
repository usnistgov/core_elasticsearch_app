""" Utils for the elasticsearch package
"""

import re


def clean_keyword(keyword):
    """ Remove extra characters and format keyword

    Args:
        keyword:

    Returns:

    """
    # lowercase
    keyword = keyword.lower()

    # remove extra characters
    regex = re.compile('<em>.*</em>')
    keyword = re.search(regex, keyword).group()

    # remove highlight tags
    keyword = keyword.replace('<em>', '').replace('</em>', '')

    return keyword
