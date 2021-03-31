import locale
import re
import sys
import textwrap

import click
import requests

from . import __version__


language_code, encoding = locale.getlocale()


API_URL = 'https://fr.wikipedia.org/api/rest_v1/page/random/summary'
match = re.search(r'://(\w{2})', API_URL)
API_URL = API_URL.replace(match.group(1), language_code[:2], 1)


@click.command()
@click.version_option(version=__version__)
def main():
    """The hyperjazcap Python project"""
    with requests.get(API_URL) as response:
        try:
            response.raise_for_status()
        except ConnectionError as e:
            click.secho(e.text, bg='red')
            click.echo('Looks like the API is down. Please try again later!')
            sys.exit(0)

        # language_code, encoding = locale.getlocale()
        data = response.json()

    title = data['title']
    extract = data['extract']
    click.secho(title, fg='green')
    click.secho(textwrap.fill(extract), bg='green')
