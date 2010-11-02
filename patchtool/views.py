from django.shortcuts import render_to_response 
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
import glob
from django.template import RequestContext
from subprocess import * 
from os import listdir
from tkldevenv.patchtool.utils import is_running

def patchtool_index(request):
   running = is_running('/usr/local/bin/tklpatch')
   if running:
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
   Popen(['tklpatch', baseimage, patch], cwd='/tmp') 
   return HttpResponseRedirect('../status/')

def status(request):
   running = is_running('/usr/local/bin/tklpatch')
   if running:
      status='Running'
   else:
      status='Finished'
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
   imagelist = Popen(['tklpatch-getimage','--list'],stdout=PIPE).communicate()[0]
   imagelist = imagelist.split("\n")
   imagelist.pop() #Remove empty element
   return render_to_response('patchtool/listimages.html',
     {"imagelist": imagelist}, context_instance=RequestContext(request))

def get_image(request):
   running = is_running('/usr/local/bin/tklpatch-getimage')
   if not running:
      image = request.POST['image']
      Popen(['tklpatch-getimage',image])
      status = 'Downloading'
   else:
      status = 'Busy'
      image = 'other image'
   return render_to_response('patchtool/getimage.html',
      {"status": status,
       "image": image}) 
