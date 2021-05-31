deserializedItem["article"]["title"]

getSomething_sql = """
SELECT json
FROM lists;"""

output = cur.execute(getSomething_sql)

i=0
results = cur.fetchall()
for row in results:
    print(i)
    print(row)
    i=i+1
