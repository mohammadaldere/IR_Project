print("intializing search engine...")
from flask import Flask, render_template, request
app = Flask(__name__,static_folder='UI/static', template_folder='UI/templates')

# modify this to set in testing mode
test = True
# end

print("starting http server...")
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    # Get the form data
    q = request.form['q']
    print("get request: ", q)
    start_time = time.time()
    
    # TODO: get the documents and assign them to docs
    # docs = get_docs(q,documents_df)
    # comments = get_docs(q, comments_df)
    # test:
    if test:
        docs = [{'doc_id':'doc'+str(i), 'title':'doc' + str(i) +' title', 'text':'doc ' + str(i) + ' text' } for i in range(10)]
    else:
        docs = get_docs(q,documents_df)
        print(docs)
    return render_template('results.html', docs=docs, time=time.time()-start_time, q=q)

@app.route('/get_doc')
def get_doc():
    id = request.args.get('id')
    
    # TODO: get the document by id and set to doc, get all comments
    if test:
        doc = {"doc_id":id, "title":'doc' + str(id) +' title', "text" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Sapien eget mi proin sed libero enim sed faucibus turpis. Purus sit amet volutpat consequat mauris nunc congue nisi. Amet consectetur adipiscing elit pellentesque habitant morbi tristique senectus et. Donec massa sapien faucibus et molestie ac feugiat sed lectus. Posuere urna nec tincidunt praesent. Tortor consequat id porta nibh venenatis cras. Enim nulla aliquet porttitor lacus luctus accumsan tortor posuere. Odio ut sem nulla pharetra diam sit amet. Ut aliquam purus sit amet luctus venenatis. Varius duis at consectetur lorem donec. Faucibus a pellentesque sit amet porttitor eget. Euismod nisi porta lorem mollis aliquam ut. Mus mauris vitae ultricies leo integer malesuada nunc vel. Nibh venenatis cras sed felis eget. Scelerisque in dictum non consectetur a erat. Donec adipiscing tristique risus nec feugiat in fermentum posuere. Varius sit amet mattis vulputate enim. Sem viverra aliquet eget sit. Senectus et netus et malesuada fames. Nullam vehicula ipsum a arcu cursus. Lectus mauris ultrices eros in cursus turpis massa tincidunt dui. Odio tempor orci dapibus ultrices in iaculis nunc sed. Egestas congue quisque egestas diam in arcu cursus. Tincidunt augue interdum velit euismod in pellentesque massa placerat duis. Proin sed libero enim sed faucibus. Volutpat blandit aliquam etiam erat. Eget mauris pharetra et ultrices. Turpis in eu mi bibendum neque egestas."}
        comments_cur = sqlite3.connect( "UX/antique_docs.db" )
        comments = [get_comment("2020338_0",cur=comments_cur)]
        
        print(comments)
    else:
        
        doc = get_document(id)
        comments = get_comments(id)
    

    
    return render_template('doc.html', doc=doc, comments=comments)

if  __name__ =="__main__":
    import time
    start_time = time.time()
    if not test:
        # initiailzing server
        print("starting db services...")
        from UX.db_api import *

        print("starting search enging information retrevial system...")
        from UX.eng_api import *
    
    print("["+str(time.time()-start_time)+" sec] : search engine is ready.")
    app.run(debug=True, use_reloader=False)
    