#!/usr/bin/env python3

import sqlite3
import json
import sys

#print(f"Arguments of the script : {sys.argv[1:]=}")

if sys.argv[1]:
    nameOfPapersList = sys.argv[1]
if len(sys.argv) >=  3:
    nameOfBibOutput = sys.argv[2] + '.bib'
else:
    nameOfBibOutput = nameOfPapersList + '.bib'

dbLocation = '/Users/jun/Library/Application Support/Papers/eed18127-ab56-497d-997e-1c80d418a368.db'

con = sqlite3.connect(dbLocation)
cur = con.cursor() # instantiate a cursor obj

cur.execute("SELECT id FROM lists WHERE INSTR(json,'" + nameOfPapersList + "')")
list_id = cur.fetchone()[0]
print("ReadCube list_id for " + nameOfPapersList + ": " + list_id + "\n")

cur.execute("SELECT json FROM lists WHERE id = '" + list_id + "'")
# That's the code for Tenocyte ReadCube list
result = cur.fetchone()

# Get keys from JSON ugh
deserialized = json.loads(result[0])
item_ids = deserialized["item_ids"]
#print(item_ids)
#print(type(item_ids))

bibEntryTemplate = """
@article{{{citekey},
year = {{{year}}},
title = {{{title}}},
author = {{{authorline}}},
journal = {{{journal}}}
}}"""

with open(nameOfBibOutput, mode='w') as file_object:

    # Get individual papers from the ReadCube list
    for item_id in item_ids:
        #print(item_id)
        cur.execute("SELECT json FROM items WHERE id = '" + item_id + "'")
        result = cur.fetchone()
        deserializedItem = json.loads(result[0])

        authors = deserializedItem["article"]["authors"]
        title   = deserializedItem["article"]["title"]
        year    = deserializedItem["article"]["year"]
        journal = deserializedItem["article"]["journal"]
        citekey = deserializedItem["user_data"]["citekey"]

        # format the authorline for bibtex, with last name, comma, first name and authors separated by AND
        authorlineList = []
        for indivAuthor in authors:
            #print(indivAuthor)
            *indivAuthorGivenNames, indivAuthorLastName = indivAuthor.split(" ")
            #print("Last name: " + indivAuthorLastName)
            #print("Given names: " + ' '.join(indivAuthorGivenNames))
            #print("\n")
            authorlineList.append(indivAuthorLastName + ', ' + ' '.join(indivAuthorGivenNames))
        authorline = ' and '.join(authorlineList)
        #print(authorline)

        bibEntry = bibEntryTemplate.format(citekey=citekey,year=year,title=title,journal=journal, authorline=authorline)
        #print(bibEntry)
        #print("\n")
        print(bibEntry, file=file_object)

print("Exported " + str(len(item_ids))  + " to " + nameOfBibOutput  + ".")
