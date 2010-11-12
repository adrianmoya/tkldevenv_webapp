from django.shortcuts import render_to_response 
import os
from tkldevenv.utils import lastupdated

def projects_index(request):
    projectlist=[]
    for name in os.listdir('/srv/tklpatch/projects/'):
        dirname = os.path.join('/srv/tklpatch/projects/', name)
        if os.path.isdir(dirname):
            mtime = lastupdated(dirname)
            projectlist.append({'name': name, 'mtime': mtime})
    return render_to_response('projects/projects.html', {'projectlist': projectlist}) 
