import os
from flask import Blueprint, render_template, url_for, redirect

from pages.page import Page
from utils.utils import GetTextAsList

class CV(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

    def GetName(self):
        return "CV"
    
    def GetRootUrl(self):
        return url_for("CV.CVView")

CV = CV('CV', __name__, template_folder='templates')

@CV.route('/cv')
def CVView():
    config = CV.GetConfig()

    info       = GetTextAsList(config['text_path'], "cv.txt")
    image_path = 'images/headshot_good.JPG'
    title      = 'David Kooi'
    sub_title  = 'kooi.david.w(at)gmail.com'
    content_type = 'text'

    ## All of the above is deprecated because we are serving a PDF

    return redirect(url_for("static", filename="pdf/davidkooi_resume.pdf"))

