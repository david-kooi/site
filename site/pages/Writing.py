import os
import sys
import json
import subprocess

from flask import Blueprint, render_template, url_for

from pages.page import Page

class Writing(Page):
    def __init__(self, *args, **kwargs):
        self.root = ''

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

    link_dict, link_names = GetLinkDict('/writing')
    print(link_dict)


    return render_template('left_image.html', title=title, sub_title=sub_title,\
    link_names=link_names, link_dict=link_dict, content_type=content_type, image_path=image_path) 

@Writing.route('/writing/<content_path>')
def ContentView(content_path):
    pass



def GetLatestCommitSha():
    cmd = "curl  \"https://api.github.com/repos/david-kooi/writing/commits\""
    output = subprocess.check_output(cmd, shell=True)
    output = output.decode("utf-8")

    return json.loads(output)[0]['sha']

def GetLinkDict(root):

    link_dict = dict()
    link_names = []

    root = os.path.join(Writing.root, root)
    sha = GetLatestCommitSha()

    cmd = "curl  \"https://api.github.com/repos/david-kooi/writing/git/trees/"\
                 "{}\"".format(sha)
    output = subprocess.check_output(cmd, shell=True)
    output = output.decode('utf-8') 

    git_tree = json.loads(output)['tree']
 

    for f in git_tree:
        file_name   = f['path']
        url         = f['url']
        content_t   = f['type']
        sha         = f['sha']
        path        = os.path.join(root, file_name)
        
        if(file_name[0] == '.'):
            continue
 
        link_dict[file_name] = {'url':url, 'content':content_t, 'root':root, 'sha':sha,\
                                'path':path} 
        link_names.append(file_name)
    
    
    Writing.root = root
    
    link_names = sorted(link_names)
    return link_dict, link_names
 
