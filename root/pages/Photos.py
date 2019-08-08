import os
from flask import Blueprint, render_template, url_for, redirect

from pages.page import Page
from utils.utils import GetTextAsList

class Photos(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

    def GetName(self):
        return "Photos"
    
    def GetRootUrl(self):
        return url_for("Photos.PhotosView")

Photos = Photos('Photos', __name__, template_folder='templates')

@Photos.route('/photos')
def PhotosView():
    config = Photos.GetConfig()

    ## All of the above is deprecated because we are serving a PDF

    return redirect("https://www.flickr.com/photos/davidkooi")
