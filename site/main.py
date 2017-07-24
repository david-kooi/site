import os
from flask import Flask, request, render_template, url_for
from flask_restful import Resource, Api


from pages.Home    import Homepage
from pages.CV      import CV
from pages.Writing import Writing

from utils.page_manager import PageManager

app = Flask(__name__)
api = Api(app)

# Setup Config
app.config.from_object(__name__)
app.config['root_path']   = app.root_path
app.config['static_path'] = os.path.join(app.root_path, 'static')
app.config['text_path']   = os.path.join(app.config['static_path'],'text')

# Setup Pages
page_manager = PageManager.GetInstance()
page_list = [Homepage, CV, Writing]

# Register pages to app and page_manager
for page in page_list:
    app.register_blueprint(page)
    page_manager.RegisterPage(page)
    page.SetConfig(app)



# Setup REST Resources
class DataReceive(Resource):
    def put(self, datetime):
        print("Received: {}".format(request.form['data']))

api.add_resource(DataReceive, '/<string:datetime>')



# Provide app with global vars
@app.context_processor
def LayoutLinkProcessor():
    
    # Set main links
    links = []
    home  = {}

    for page in page_list:
 
        links.append({"name":page.GetName(), 
                      "href":page.GetRootUrl()})


    # include_header is true by default
    return dict(links=links, include_header=True)


