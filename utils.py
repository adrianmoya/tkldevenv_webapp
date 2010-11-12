from subprocess import Popen, PIPE
import glob
import time
import os.path

def is_running(process):
    processes = Popen(['ps', 'xa', '-o','args'], stdout=PIPE)
    running = Popen(['grep',process], stdin=processes.stdout, stdout=PIPE).communicate()[0]
    if running.find(process+' ') >= 0:
        return running
    return ''

def list_images():
    baseimages = glob.glob("/srv/tklpatch/base-images/*.iso")
    baseimages = [x.replace('/srv/tklpatch/base-images/','') for x in baseimages]
    return baseimages

def list_patches():
    patches = glob.glob("/srv/tklpatch/patches/*")
    patches = [x.replace('/srv/tklpatch/patches/','') for x in patches]
    return patches

def lastupdated(filename):
    try:
        mtime = time.strftime("%m/%d/%Y %I:%M:%S %p",time.localtime(os.path.getmtime(filename)))
    except:
       mtime = "Not available"
    return mtime
