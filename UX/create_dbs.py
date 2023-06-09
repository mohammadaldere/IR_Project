import csv, sqlite3
import os

def create_comments_sqlite_database():
  print(os.listdir("."))
  if "antique_docs.db" in os.listdir("."):
    return
  cur = sqlite3.connect( "antique_docs.db" )
  cur.text_factory = str
  cur.execute('CREATE TABLE IF NOT EXISTS comments (doc_id VARCHAR, text VARCHAR)')
  reader = csv.reader(open("antique_docs.csv", "r"))
  for id, doc_id, test in reader:
    print('.', end="")
    cur.execute('INSERT OR IGNORE INTO comments (doc_id, text) VALUES (?,?)', (doc_id, test))
  cur.commit()
  cur.close()

def create_documents_sqlite_database():
  print(os.listdir("."))
  if "mr_tydi_docs.db" in os.listdir("."):
    return
  cur = sqlite3.connect( "mr_tydi_docs.db" )
  cur.text_factory = str  #bugger 8-bit bytestrings
  cur.execute('CREATE TABLE IF NOT EXISTS documents (doc_id VARCHAR ,title VARCHAR ,text VARCHAR)')
  reader = csv.reader(open("mr_tydi_docs.csv", "r"))
  for id, doc_id, title, text in reader:
    print(".", end="")
    cur.execute('INSERT OR IGNORE INTO documents (doc_id, title, text) VALUES (?,?, ?)', (doc_id, title, text))
  cur.commit()
  cur.close()

# create_comments_sqlite_database()
# create_documents_sqlite_database()