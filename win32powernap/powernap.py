from monitors import wininput
from actions import novacpu
import time
import logging

class PowerNap:

    def __init__(self, conf):
        logging.basicConfig(level=logging.DEBUG, 
                            format='%(asctime)s %(levelname)s %(message)s',
                            filename=conf['log_file'])
        self.monitors = [wininput.InputMonitor()]
        self.actions = [novacpu.ManageNovaComputeAction()]
        self.conf = conf
        self.inactive_for = 0
        self.idle = False

    def run(self):

        while True:
            all_inactive = True
            for monitor in self.monitors:
                all_inactive = not monitor.active() and all_inactive
            if not all_inactive:
                if self.idle:
                    logging.info('Monitors are no longer idle. Calling bringup().')
                    for action in self.actions:
                        try:
                            action.bringup(self.conf)
                        except Exception, e:
                            logging.exception(e)
                        
                self.idle = False
                self.inactive_for = 0
            else:
                if self.inactive_for >= int(self.conf['idle_interval']) and not self.idle:
                    self.idle = True
                    logging.info('Monitors are idle. Calling takedown().')
                    for action in self.actions:
                        try:
                            action.takedown(self.conf)
                        except Exception, e:
                            logging.exception(e)
                self.inactive_for += int(self.conf['check_interval'])
            time.sleep(int(self.conf['check_interval']))