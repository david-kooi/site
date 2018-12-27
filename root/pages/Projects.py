import os
from flask import Blueprint, render_template, url_for

from pages.page import Page
from utils.utils import GetTextAsList

class ProjectPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.base_info = {'image_path'  : 'images/projects_cropped.jpg',
                          'title'       : 'Papers and Projects',
                          'sub_title'   : '',
                          'content_type': 'links'}

        perceptron_pdf_path = "pdf/ohsnap_perceptron_dkooi.pdf"

        self.base_info['link_dict']  = {\
                "Perceptron Branch Predictor":\
                {"path":urlfor('static',filename=perceptron_pdf_path)},\

                "Optimal Control Using Temporal Logic":{"path":"https://hybrid.soe.ucsc.edu/sites/default/files/preprints/31.pdf"},\
                "Temporal Logic Specifications in for Hybrid Systems":{"path":"https://arxiv.org/abs/1807.02574"},\
                "Hybrid Controller Synthesis using Formal Specification":{"path":"https://ieeexplore.ieee.org/document/8396562?reload=true"}\
                
                }

        link_names = [key for key in self.base_info['link_dict']]

        self.base_info['link_names'] = link_names
        

    def GetName(self):
        return "Papers and Projects"
    
    def GetRootUrl(self):
        return url_for("Projects.ProjectView")


ProjectPage = ProjectPage("Projects",\
                          __name__, template_folder='templates')

@ProjectPage.route('/papers_and_projects')
def ProjectView():
    config = ProjectPage.GetConfig()

    ProjectPage.base_info['content_type'] = 'links'

    return render_template('left_image.html', **ProjectPage.base_info)
