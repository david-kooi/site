import os
from flask import Blueprint, render_template, url_for

from pages.page import Page
from utils.utils import GetTextAsList

class ProjectPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.base_info = {'image_path'  : 'images/projects_cropped.jpg',
                          'title'       : 'Projects',
                          'sub_title'   : '* Under Construction *',
                          'content_type': 'links'}
 

    def GetName(self):
        return "Projects"
    
    def GetRootUrl(self):
        return url_for("Projects.ProjectView")


ProjectPage = ProjectPage("Projects", __name__, template_folder='templates')

@ProjectPage.route('/projects')
def ProjectView():
    config = ProjectPage.GetConfig()

    ProjectPage.base_info['content_type'] = 'links'

    return render_template('left_image.html', **ProjectPage.base_info)
