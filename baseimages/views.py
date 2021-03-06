from django.shortcuts import render_to_response 
from django.http import HttpResponseRedirect
from django.conf import settings
from django.template import RequestContext
from subprocess import Popen, PIPE
import os.path
from tkldevenv_webapp.utils import is_running, list_images
import glob
from tkldevenv_webapp.utils import UploadFileForm
from tkldevenv_webapp.settings import TKLPATCH_BASEIMAGES_ROOT
from django import forms
from tkldevenv_webapp.utils import handle_upload_file

def images_index(request):
    baseimagelist = list_images()
    return render_to_response('baseimages/baseimages.html',{"baseimagelist": baseimagelist})

def available_images(request):
    running = is_running('/usr/local/bin/tklpatch-getimage') 
    if len(running) > 0:
        return HttpResponseRedirect('/baseimages/getimage/')
    if os.path.exists(settings.TKLPATCH_BASEIMAGES_FILE):
        imagelist = Popen(['tklpatch-getimage','--list'],stdout=PIPE).communicate()[0]
        imagelist = imagelist.split("\n")
        imagelist.pop() #Remove empty element
        baseimagelist = list_images()
        for x in baseimagelist:
            image = x[:-4]
            try:
                imagelist.remove(image)
            except:
                pass
    else:
        imagelist = ''
    return render_to_response('baseimages/listimages.html',{"imagelist": imagelist}, context_instance=RequestContext(request))

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
            return HttpResponseRedirect('/baseimages')
    return render_to_response('baseimages/getimage.html',{"image": image, "message": message})

def refresh_list(request):
    running = is_running('/usr/local/bin/tklpatch-getimage') 
    if len(running) > 0:
        return HttpResponseRedirect('/baseimages/getimage/')
    Popen(['tklpatch-getimage','--update']).wait()
    return HttpResponseRedirect('/baseimages/listimages')

def baseimage_upload(request):
    messages = ""
    if request.method == 'POST':
        form = UploadBaseimageForm(request.POST, request.FILES)   
        if form.is_valid():
            file = request.FILES['file']
            filename = str(file.name)
            baseimagedir = TKLPATCH_BASEIMAGES_ROOT
            if os.path.exists("%s%s" % (baseimagedir, filename)):
                messages = "The image already exists"
            else:
                try:
                    handle_upload_file(request.FILES['file'],baseimagedir)
                except:
                    messages = "There was an error uploading the image file"
                    raise
                else:
                    messages = "Base image %s uploaded successfully" % (filename)
    else:
        form = UploadBaseimageForm()
    return render_to_response("baseimages/upload.html",{"form": form, "messages": messages}, context_instance=RequestContext(request))


class UploadBaseimageForm(UploadFileForm):
    def clean_file(self):
        data = self.cleaned_data['file']
        filename = str(data.name)
        if not filename.endswith(".iso"):
            raise forms.ValidationError("The file is not an iso file!")
        return data
