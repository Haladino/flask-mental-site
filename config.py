import os


LOC = os.path.dirname(os.path.realpath(__file__))

CITATION_TEXT = []
HELP_TEXT = []
SERVICES = []

with open(os.path.join(LOC, 'static/text/citation.txt')) as f:
    for line in f:
        CITATION_TEXT.append(line)

with open(os.path.join(LOC, 'static/text/help.txt')) as f:
    for line in f:
        HELP_TEXT.append(line)

with open(os.path.join(LOC, 'static/text/services.txt')) as f:
    for line in f:
        SERVICES.append(line.strip().split(','))