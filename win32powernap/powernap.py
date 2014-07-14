from monitors import wininput
import time

class PowerNap:

    def __init__(self, conf):
    	self.monitors = [wininput.InputMonitor()]
    	self.actions = []
    	self.conf = conf
    	self.inactive_for = 0
    	self.idle = False

    def run(self):

    	while True:
    		all_inactive = True
    		for monitor in self.monitors:
    			all_inactive = not monitor.active() and all_inactive
    		if not all_inactive:
    			self.idle = False
    			self.inactive_for = 0
    		else:
    			if self.inactive_for >= self.conf['idle_interval'] and not self.idle:
    				self.idle = True
    				for action in self.actions:
    					action.take()
    			self.inactive_for += self.conf['check_interval']
    		print 'Inactive for %d' % self.inactive_for
    		time.sleep(self.conf['check_interval'])



