import os
import json
import base64
import codecs
import pprint
import subprocess

from flask import Blueprint, render_template, url_for

from pages.page import Page

class Writing(Page):
    def __init__(self, *args, **kwargs):
        self.root = ''
        self.tree = {'/writing':
                        {'item_dict':{}
                        }
                    }

        self.base_info = {'image_path'  : 'images/writing.jpg',
                          'title'       : 'Writing',
                          'sub_title'   : 'By David Kooi and Others',
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
    pprint.PrettyPrinter(indent=1).pprint(Writing.tree['/writing']['item_dict'])
    
    link_dict, link_names= GetLinkDict("/writing")
    #print(link_dict)
   
    # Get file items
    item_dict = Writing.tree['/writing']['item_dict']
    item_names = []

    # Add latest update file
    item_dict['-> latest_update <-'] = {}
    item_dict['-> latest_update <-']['path'] = "/writing/latest_update.txt"
    item_names = ['-> latest_update <-']
    
    Writing.base_info['content_type'] = 'links'
    Writing.base_info['item_dict']    = item_dict
    Writing.base_info['item_names']   = item_names
    Writing.base_info['link_dict']    = link_dict
    Writing.base_info['link_names']   = link_names

    return render_template('left_image.html', **Writing.base_info) 


@Writing.route('/writing/<path:file_path>')
def ContentView(file_path):
    
    #print("FILEPATH {}".format(file_path))
    file_root   = os.path.join('/writing', file_path) 
    folder_root = os.path.dirname(file_root) 
    file_name   = os.path.basename(file_root)

    if('.' in file_name): # File has extension: treat as file 

        if('latest_update' in file_name):
            info = ""
            with open("static/text/latest_update.txt", "r") as f:
                info = f.read()
        else:
            # Get folder items to get file url
            item_dict = Writing.tree[folder_root]['item_dict']
            print(item_dict)
            url = item_dict[file_name]['url']

            info = GetBlobFromGithub(url, file_path) 

        # Set page info
        Writing.base_info['content_type']  = 'text'
        Writing.base_info['info']          = info
        Writing.base_info['sub_title']     = file_name


    else: # Treat as folder
        
        link_dict, link_names = GetLinkDict(file_root) # Get file name
        #print("AS FOLDER")
        #print(link_dict)

        # Get file items
        item_dict = Writing.tree[file_root]['item_dict']
        item_names = [name for name in item_dict]
        item_names = sorted(item_names)
        print(item_names)

        # Set page info
        Writing.base_info['content_type'] = 'links'
        Writing.base_info['item_dict']    = item_dict
        Writing.base_info['item_names']   = item_names
        Writing.base_info['link_dict']    = link_dict
        Writing.base_info['link_names']   = link_names
        Writing.base_info['sub_title']    = file_name 


    return render_template('left_image.html', **Writing.base_info)





def GetLatestCommitSha(file_list):
    """
    Return the latest commit SHA.
    Also, add the status and filename of all changed files.
    """
    cmd = "curl  \"https://api.github.com/repos/david-kooi/writing/commits\""
    output = subprocess.check_output(cmd, shell=True)
    output = output.decode("utf-8")
    #print("OUTPUT: {}".format(output))
    
    sha = json.loads(output)[0]['sha']

    cmd = cmd + "/" + sha 
    output = subprocess.check_output(cmd, shell=True)
    output = output.decode("utf-8")
    
    output = json.loads(output)
     
    file_blob = output['files']
    for g_file in file_blob:
        action    = g_file['status']
        file_name = g_file['filename']
        file_list.append((action, file_name)) 


    date = output['commit']['author']['date'][0:9] 
    
    return date, sha  

def GetBlobFromGithub(url, file_path):
    cmd = "curl {}".format(url)
    output = subprocess.check_output(cmd, shell=True)
    output = output.decode('utf-8')
    content = json.loads(output)['content']
    content = base64.b64decode(content)
    try:
        content = content.decode('utf-8')
    except UnicodeDecodeError:
        content = GetDecodeErrorMessage(file_path)
        LogDecodeError(file_path)
    
    return content 

def GetDecodeErrorMessage(file_path):
    return "Rtf continues it's vengance. We've experienced a decode error." 

def LogDecodeError(file_path):
    #TODO
    pass

def WriteLatestUpdate(date, file_list):

    with open("static/text/latest_update.txt", "w") as f: 
        f.write("Last updated: {}\n\n".format(date))
        for action, filename in file_list:
            f.write("{}: {}\n".format(action.title(), filename))


def SetTreeFromRoot():

    file_list = []
    date, sha = GetLatestCommitSha(file_list)

    WriteLatestUpdate(date, file_list)

    cmd = "curl  \"https://api.github.com/repos/david-kooi/writing/git/trees/"\
                 "{}\"?recursive=1".format(sha)
    output = subprocess.check_output(cmd, shell=True)
    output = output.decode('utf-8') 


    tree_list = json.loads(output)['tree'] # Tree is a list of dictionaries

    for item in tree_list: 
        file_name = os.path.basename(item['path'])
        if(file_name[0] == '.'):
            continue

        # Add /writing to the path
        root = os.path.join('/writing', item['path'])
       
        if(item['type'] == 'tree'):
            Writing.tree[root] = {}
            Writing.tree[root]['tree'] = item
            Writing.tree[root]['item_dict'] = {}

        elif(item['type'] == 'blob'): 
            file_root = os.path.dirname(root)
            file_name = root.split('/')[-1]

            # Add /writing to the path
            item['path'] = root

            Writing.tree[file_root]['item_dict'][file_name] = item



def GetLinkDict(base_path):
 
    link_names = []
    link_dict  = {}


    # Collect from Writing.tree 
 

    base_path_tokens = base_path.split('/')
    for item_path in Writing.tree:
        item_path_tokens = item_path.split('/')

        
        # Get item if item_path is 1 deeper than base_path
        if(len(item_path_tokens) == len(base_path_tokens) + 1):
            # Check if item_path continues from base_path
            if(item_path_tokens[-2] == base_path_tokens[-1]): 

                
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
 
import os
