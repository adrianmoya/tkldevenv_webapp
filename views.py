from django.shortcuts import render_to_response 
import os
import time

def main(request):
  projectlist=[]
  for name in os.listdir('/srv/tklpatch/projects/'):
    if os.path.isdir(os.path.join('/srv/tklpatch/projects/', name)):
      mtime = lastupdated(name)
      projectlist.append({'name': name, 'mtime': mtime})
  return render_to_response('tkldevenv.html', {'projectlist': projectlist}) 

def lastupdated(filename):
  try:
    mtime = time.strftime("%m/%d/%Y %I:%M:%S %p",time.localtime(os.path.getmtime('/srv/tklpatch/patches/'+filename)))
  except:
    mtime = "Never"
  return mtime
