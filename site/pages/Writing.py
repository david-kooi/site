import os
import sys
import json
import pprint
import subprocess

from flask import Blueprint, render_template, url_for

from pages.page import Page

class Writing(Page):
    def __init__(self, *args, **kwargs):
        self.root = ''
        self.tree = {'/writing':
                        {'items':{}
                        }
                    }

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



    SetTreeFromRoot()
    #pprint.PrettyPrinter(indent=1).pprint(Writing.tree['/writing']['items'])
    
    link_dict, link_names= GetLinkDict("/writing")
    #print(link_dict)
    
    Writing.base_info['content_type'] = 'links'

    return render_template('left_image.html', **Writing.base_info, link_names=link_names,\
                                              link_dict=link_dict) 

@Writing.route('/writing/<path:file_path>')
def ContentView(file_path):
    
    file_root = os.path.join('/writing', file_path) 
    print(file_root)
    link_dict, link_names = GetLinkDict(file_root) # Get file name
    #print(link_dict)

    Writing.base_info['content_type'] = 'links'

    return render_template('left_image.html', **Writing.base_info, link_names=link_names,\
                                              link_dict=link_dict) 





def GetLatestCommitSha():
    cmd = "curl  \"https://api.github.com/repos/david-kooi/writing/commits\""
    output = subprocess.check_output(cmd, shell=True)
    output = output.decode("utf-8")
    #print("OUTPUT: {}".format(output))

    return json.loads(output)[0]['sha']

def SetTreeFromRoot():

    sha = GetLatestCommitSha()

    cmd = "curl  \"https://api.github.com/repos/david-kooi/writing/git/trees/"\
                 "{}\"?recursive=1".format(sha)
    output = subprocess.check_output(cmd, shell=True)
    output = output.decode('utf-8') 


    tree_list = json.loads(output)['tree'] # Tree is a list of dictionaries

    for item in tree_list: 
        if(item['path'][0] == '.'):
            continue


        root = os.path.join('/writing', item['path'])
       
        if(item['type'] == 'tree'):
            Writing.tree[root] = {}
            Writing.tree[root]['tree'] = item
            Writing.tree[root]['items'] = {}

        elif(item['type'] == 'blob'): 
            file_root = os.path.dirname(root)
            file_name = root.split('/')[-1]

            Writing.tree[file_root]['items'][file_name] = item



def GetLinkDict(base_path):
 
    link_names = []
    link_dict  = {}


    # Collect from Writing.tree 
 

    base_path_tokens = base_path.split('/')
    for item_path in Writing.tree:
        item_path_tokens = item_path.split('/')
        
        if(len(item_path_tokens) == len(base_path_tokens) + 1):
            item = Writing.tree[item_path]['tree'] 
        

            file_name   = os.path.basename(item['path'])
            path        = os.path.join(base_path, file_name) 
            content_t   = item['type']
            sha         = item['sha']
            
            if(file_name[0] == '.'):
                continue
      
            link_names.append(file_name)
            link_dict[file_name] = {}
            link_dict[file_name]['path']  = path 
            link_dict[file_name]['type']  = content_t
            link_dict[file_name]['sha']   = sha
         
        link_names = sorted(link_names)
        
    return link_dict, link_names
 
