from subprocess import Popen, PIPE

def is_running(process):
   processes = Popen(['ps', 'xa'], stdout=PIPE).communicate()[0]
   if processes.find(process) > 0:
      return True
   return False

