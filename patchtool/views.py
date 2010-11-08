from django.shortcuts import render_to_response 
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
import glob
from django.template import RequestContext
from subprocess import * 
import os.path
from tkldevenv.patchtool.utils import is_running
import time

def patchtool_index(request):
   running = is_running('/usr/local/bin/tklpatch')
   if running != '':
     return HttpResponseRedirect('status/')
   baseimages = list_existing_images()
   patches = glob.glob("/srv/tklpatch/patches/*")
   patches = [x.replace('/srv/tklpatch/patches/','') for x in patches]
   return render_to_response('patchtool/index.html',
	    {"baseimages": baseimages,
	     "patches": patches,
	    }, context_instance=RequestContext(request))

def list_existing_images():
   baseimages = glob.glob("/srv/tklpatch/base-images/*.iso")
   baseimages = [x.replace('/srv/tklpatch/base-images/','') for x in baseimages]
   return baseimages

def apply_patch(request):
   baseimage = request.POST['baseimage']
   patch = request.POST['patch']
   Popen(['tklpatch', baseimage, patch], cwd='/srv/tklpatch/patched-isos') 
   time.sleep(2)
   return HttpResponseRedirect('../status/')

def status(request):
  lastpatch = last_patch_run()
  baseimage = lastpatch[0]
  patch = lastpatch[1]
  logfile = settings.TKLPATCH_LOGS_ROOT+baseimage+'-'+patch+'.log'
  log = ''
  try:
    with open(logfile, 'r') as f:
      for line in f:
        log += line
  except IOError:
    log = "Not available"
  running = is_running('/usr/local/bin/tklpatch')
  if len(running) > 0:
    status = 'Running'
  else:
    status = 'Stopped'
  return render_to_response('patchtool/status.html',
    {"baseimage": baseimage,
     "patch": patch,
     "status": status,
     "log": log,
    })

def last_patch_run():
   files = Popen(['ls', '-1t', '/var/log/tklpatch/'],stdout=PIPE,cwd='/var/log/tklpatch').communicate()[0] 
   if len(files) > 0: 
     file = files.split('\n')[0]
     if file.find('x86') > 0:
        arch = 'x86'
     else:
        arch = 'x64'
     data = file.split('-'+arch+'-')
     baseimage = data[0]+'-'+arch
     patch = data[1].split('.')[0]
   else:
     baseimage = ''
     patch = ''
   return [baseimage,patch]

def list_images(request):
   running = is_running('/usr/local/bin/tklpatch-getimage') 
   if len(running) > 0:
      return HttpResponseRedirect('/patchtool/getimage/')
   imagelist = Popen(['tklpatch-getimage','--list'],stdout=PIPE).communicate()[0]
   imagelist = imagelist.split("\n")
   imagelist.pop() #Remove empty element
   return render_to_response('patchtool/listimages.html',
     {"imagelist": imagelist}, context_instance=RequestContext(request))

def get_image(request):
  running = is_running('/usr/local/bin/tklpatch-getimage')
  message=''
  if len(running) > 0:
    image = running.split()[3]
  else:
    if request.POST.has_key('image'):
      image = request.POST['image']
      if os.path.exists('/srv/tklpatch/base-images/'+image+'.iso'):
        message = 'File '+image+'.iso already exists'
      else:
        Popen(['tklpatch-getimage',image])
    else:
      return HttpResponseRedirect('/patchtool')
  return render_to_response('patchtool/getimage.html',{"image": image, "message": message})
