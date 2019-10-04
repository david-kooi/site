import os
from flask import Blueprint, render_template, url_for, redirect

from pages.page import Page
from utils.utils import GetTextAsList

class Homepage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

    def GetName(self):
        return "Homepage"
    
    def GetRootUrl(self):
        return url_for("Homepage.HomeView")
    
Homepage = Homepage('Homepage', __name__, template_folder='templates')


@Homepage.route('/robots.txt')
def ReturnRobots():
    return redirect(url_for("static", filename="robots.txt"))


@Homepage.route('/')
def HomeView():
    config = Homepage.GetConfig()

    info         = GetTextAsList(config['text_path'], "info.txt")
    image_path   = "images/headshot_good.JPG"
    title        = 'David Kooi'
    sub_title    = 'dkooi@ucsc.edu'
    content_type = "text"

    return render_template('left_image.html', include_header=False, title=title, sub_title=sub_title,\
                                content_type=content_type, image_path=image_path, info=info) 






