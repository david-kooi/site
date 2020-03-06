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
                          'content_type': 'projects'}


        self.base_info["personal_projects"] = {\
                "03-2020 Minimum Jerk Polynomial Path Planning":{"path":"/static/pdf/path_planning_presentation.pdf"},\
                "05-2019 Regulation and Trajetory Tracking for Robotic Manipulators":{"path":"/static/pdf/regulation_robotic_manipulators.pdf"},\
                "12-2018 Perceptron Branch Predictor ESESC Implementation":{"path":"/static/pdf/ohsnap_perceptron_dkooi.pdf"},\
                "05-2018 Topcon Automated Bulldozer Slides":{"path":"/static/pdf/topcon_automated_bulldozer_slides.pdf"},\
                "05-2018 Topcon Automated Bulldozer Poster":{"path":"/static/pdf/topcon_automated_bulldozer_poster.pdf"},\
                "12-2017 Mechatronics Elevator Bot Report":{"path":"/static/pdf/2017_mechatronics_report.pdf"},\
                }

        self.base_info['by_others']  = {\
                "Optimal Control Using Temporal Logic":{"path":"https://hybrid.soe.ucsc.edu/sites/default/files/preprints/31.pdf"},\
                "Temporal Logic Specifications in for Hybrid Systems":{"path":"https://arxiv.org/abs/1807.02574"},\
                "Hybrid Controller Synthesis using Formal Specification":{"path":"https://ieeexplore.ieee.org/document/8396562?reload=true"}\
                }

        personal_names = [key for key in self.base_info['personal_projects']]
        other_names    = [key for key in self.base_info['by_others']]
 
        def date_sort(item):
            date  = item.split(' ')[0]
            month = date.split('-')[0]
            year  = date.split('-')[1] 
            return year,month

        self.base_info['personal_names']  = sorted(personal_names, key=date_sort, reverse=True) 
        self.base_info['other_names']     = sorted(other_names, reverse=False)
        

    def GetName(self):
        return "Papers and Projects"
    
    def GetRootUrl(self):
        return url_for("Projects.ProjectView")


ProjectPage = ProjectPage("Projects",\
                          __name__, template_folder='templates')

@ProjectPage.route('/papers_and_projects')
def ProjectView():
    config = ProjectPage.GetConfig()

    return render_template('left_image.html', **ProjectPage.base_info)
