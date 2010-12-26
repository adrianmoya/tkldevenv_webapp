from django.shortcuts import render_to_response 
from django.http import HttpResponseRedirect
from django.template import RequestContext
from subprocess import Popen, PIPE
import os.path
from tkldevenv_webapp.utils import list_output_isos
import glob

def output_index(request):
        isolist = list_output_isos()
        return render_to_response('output/isos.html',{"isolist": isolist})

