import os
import json
import subprocess

from flask import Blueprint, render_template, url_for

from pages.page import Page

class Writing(Page):
    def __init__(self, *args, **kwargs):
        self.git_writing_tree = None

        Page.__init__(self, *args, **kwargs)

    def GetName(self):
        return "Writing"
    
    def GetRootUrl(self):
        return url_for("Writing.WritingView")


Writing = Writing("Writing", __name__, template_folder='templates')

@Writing.route('/writing')
def WritingView():

    image_path = 'images/writing.jpg'
    title      = 'Writing'
    sub_title  = 'By David Kooi'
    content_type='links'

    content_links = GetContentLinks('/')
    print(content_links)


    return render_template('left_image.html', title=title, sub_title=sub_title,\
                    content_links=content_links, content_type=content_type, image_path=image_path) 

@Writing.route('/writing/<content_path>')
def ContentView(content_path):
    pass

def GetLatestCommitSha():
    cmd = "curl  \"https://api.github.com/repos/david-kooi/writing/commits\""
    output = subprocess.check_output(cmd, shell=True)
    output = output.decode("utf-8")

    return json.loads(output)[0]['sha']

def GetContentLinks(root):
    content_links = []

    if(Writing.git_writing_tree is None):
        sha = GetLatestCommitSha()

        cmd = "curl  \"https://api.github.com/repos/david-kooi/writing/git/trees/"\
                     "{}?recursive=0\"".format(sha)
        output = subprocess.check_output(cmd, shell=True)
        output = output.decode('utf-8') 

        Writing.git_writing_tree = json.loads(output)['tree']

    if(root == '/'):

        for f in Writing.git_writing_tree:
            file_path = f['path']
            content_links.append(file_path)
    
    
    

    return content_links

     
