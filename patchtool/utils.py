from subprocess import Popen, PIPE

def is_running(process):
   processes = Popen(['ps', 'xa', '-o','args'], stdout=PIPE)
   running = Popen(['grep',process], stdin=processes.stdout, stdout=PIPE)
   if running.find(process) > 0:
      return True
   return False

