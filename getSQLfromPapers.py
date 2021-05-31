import sqlite3
import json

nameOfProject = 'Tenocyte'

con = sqlite3.connect('eed18127-ab56-497d-997e-1c80d418a368.db')
cur = con.cursor() # instantiate a cursor obj

cur.execute("SELECT id FROM lists WHERE INSTR(json,'" + nameOfProject + "')")
list_id = cur.fetchone()[0]
print("ReadCube list_id for " + nameOfProject + ": " + list_id + "\n")

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

with open('test.bib', mode='w') as file_object:

    # Get individual papers from the ReadCube list
    for item_id in item_ids:
        print(item_id)
        cur.execute("SELECT json FROM items WHERE id = '" + item_id + "'")
        result = cur.fetchone()
        deserializedItem = json.loads(result[0])

        author  = deserializedItem["article"]["authors"]
        title   = deserializedItem["article"]["title"]
        year    = deserializedItem["article"]["year"]
        journal = deserializedItem["article"]["journal"]
        citekey = deserializedItem["user_data"]["citekey"]

        #print(citekey + author[0] + title + str(year), sep=' ')
        #print(citekey + author[0] + title + str(year), file=file_object)
        bibEntry = bibEntryTemplate.format(citekey=citekey,year=year,title=title,journal=journal, authorline='')
        print(bibEntry)
        print(bibEntry, file=file_object)

        print("\n")
