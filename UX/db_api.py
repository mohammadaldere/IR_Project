import csv, sqlite3
# on server intialize
comments_cur = sqlite3.connect( "UX/antique_docs.db" )
documents_cur = sqlite3.connect( "UX/mr_tydi_docs.db" )

# fetch comments data
def get_comment(id_, cur=comments_cur):
  args = (id_,)
  comment = cur.execute("SELECT * FROM comments WHERE doc_id = ?", args).fetchall()
  if len(comment) > 0:
    comment = dict({'doc_id': comment[0][0], 'text': comment[0][1]})
    return comment
  return -1
 
# print(get_comment("1964316_5"))

def get_all_comments(cur=comments_cur):
  return cur.execute("SELECT * FROM comments").fetchall()

# fetch documents data
def get_document(id_, cur=documents_cur):
  args = (id_,)
  document = cur.execute("SELECT * FROM documents WHERE doc_id = ?", args).fetchall()
  print(document)
  print(len(document))
  if len(document) > 0:
    document = dict({'doc_id': document[0][0], 'text': document[0][1]})
    return document
  return -1
 
# print(get_document("1964316_5"))

def get_all_documents(cur=documents_cur):
  return cur.execute("SELECT * FROM documents").fetchall()
