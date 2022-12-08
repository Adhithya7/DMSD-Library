import os
import glob
from db import make_connection

connection, cursor = make_connection()
path = os.path.dirname(os.path.abspath(__file__))
files = glob.glob(glob.escape(path)+"/*.sql")
queries = []
for f in files:
    with open(f, "r") as file:
        ind_queries = file.read().split("\n\n")
        for q in ind_queries:
            queries.append({
                "file": f,
                "sql": q
            })

queries = sorted(queries, key=lambda x:x["file"].lower())
cursor.execute("select table_name from information_schema.tables where table_schema='public'")
existing_tables = cursor.fetchall()
existing_tables = [v[0] for v in existing_tables]

for order, q in enumerate(queries):
    sql = q["sql"]
    file = q["file"]
    print(f"Trying query no {order} in file: {file}")
    if "CREATE TABLE" in sql:
        t = sql.split("(")[0] \
        .replace("CREATE TABLE","") \
        .replace("\n","") \
        .strip()
        print("t:", t)
        if t.lower() in existing_tables:
            print(f"Table {t} already exists, blocking query")
            continue
    try:
        cursor.execute(sql)
        print("Ran successfully") 
        connection.commit()
    except Exception as e:
        print("An error occured", e)

print(f"Finished running {len(queries)} queries")
connection.close()