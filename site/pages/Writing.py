import os
import sys
import json
import subprocess

from flask import Blueprint, render_template, url_for

from pages.page import Page

class Writing(Page):
    def __init__(self, *args, **kwargs):
        self.root = ''
        self.link_cache= {} 

        self.base_info = {'image_path'  : 'images/writing.jpg',
                          'title'       : 'Writing',
                          'sub_title'   : 'By David Kooi',
                          'content_type': 'links'}
   


        Page.__init__(self, *args, **kwargs)

    def GetName(self):
        return "Writing"
    
    def GetRootUrl(self):
        return url_for("Writing.WritingView")


Writing = Writing("Writing", __name__, template_folder='templates')

@Writing.route('/writing')
def WritingView():

    link_dict, link_names = GetLinkDict('/writing')
    Writing.link_dict = link_dict


    return render_template('left_image.html', **Writing.base_info, link_names=link_names,\
                                              link_dict=link_dict) 

@Writing.route('/writing/<path:file_path>')
def ContentView(file_path):
    
    file_root = os.path.join('/writing', file_path) 
    link_dict, link_names = GetLinkDict(file_root) # Get file name


    return render_template('left_image.html', **Writing.base_info, link_names=link_names,\
                                              link_dict=link_dict) 





def GetLatestCommitSha():
    cmd = "curl  \"https://api.github.com/repos/david-kooi/writing/commits\""
    output = subprocess.check_output(cmd, shell=True)
    output = output.decode("utf-8")
    print("OUTPUT: {}".format(output))

    return json.loads(output)[0]['sha']

def GetLinkDict(base_file_path):
 
    link_names = []
    file_root = os.path.dirname(base_file_path)

    # Continue down the file tree
 
    print("FILE PATH: {}".format(base_file_path))
    Writing.root = file_root 

    if(base_file_path == '/writing'):
        sha = GetLatestCommitSha()
    else:
        print(Writing.link_cache)
        sha = Writing.link_cache[base_file_path]['sha'] 


    print("")
    print("")

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
        
        if(file_name[0] == '.'):
            continue
 
        file_path = os.path.join(base_file_path, file_name)
        Writing.link_cache[file_path] = {}
        Writing.link_cache[file_path] =    {'url':url, 'content_t':content_t,\
                                            'sha':sha, 'path':file_path, 'name':file_name} 
        link_names.append(file_path)
     
    link_dict = Writing.link_cache
    link_names = sorted(link_names)
    Writing.link_cache[file_path]['link_names'] = link_names


    return link_dict, link_names
 
