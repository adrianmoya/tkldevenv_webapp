from subprocess import Popen, PIPE

def is_running(process):
   processes = Popen(['ps', 'xa', '-o','args'], stdout=PIPE)
   running = Popen(['grep',process], stdin=processes.stdout, stdout=PIPE).communicate()[0]
   if running.find(process+' ') >= 0:
      return running
   return ''

