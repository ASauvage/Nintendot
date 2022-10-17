import sqlite3
import logging
import requests
import re


def main():
    pass


def get_value(link: str):
    source = requests.get(link)
    console = re.search(
        "(\"offdeviceConsoleType\":.{2,})\w", source.text)[0][25:]
    title = re.search("(\"gameTitle\":.{2,})\w", source.text)[0][14:]
    release_date = re.search("(releaseDate:.{2,})\w", source.text)[0][14:]
    image_link = re.search(
        "(class=\"img-responsive\" src=\".{2,})\w", source.text)[0][28:]

    return console, title, release_date, image_link
