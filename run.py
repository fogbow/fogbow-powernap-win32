from win32powernap import powernap
from ConfigParser import ConfigParser
import sys

config = ConfigParser()
config.read(sys.argv[1])

pnap = powernap.PowerNap(dict(config.items('GENERAL')))
pnap.run()
