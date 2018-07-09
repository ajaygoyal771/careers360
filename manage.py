#!/usr/bin/env python
import os
import sys
from time import sleep
import threading
import requests
import subprocess
from bs4 import BeautifulSoup

def database_populate():
    sleep(30)
    from hackpy.models import create_link,create_user
    response = requests.get("https://news.ycombinator.com")
    if response.status_code != 200:
        exit("Status code " + str(response.status_code) + " - exiting")
    soup = BeautifulSoup(response.content, "html.parser")
    update = []
    for i in range(30):
        update.append({})
    j=0
    for story in soup.find_all(class_="storylink"):
        update[j]["title"] = story.get_text()
        update[j]["url"] = story["href"]
        j = j + 1
    j=0
    for story in soup.find_all(class_="hnuser"):
        update[j]["submitter"] = story.get_text()
        j = j + 1
    for i in range(30):
        update[i]["submitter"] = create_user(update[i]['submitter'])
        create_link(**update[i])
    


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careers360.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    
    t = threading.Thread(target=database_populate)
    t.start()
    execute_from_command_line(sys.argv)
    