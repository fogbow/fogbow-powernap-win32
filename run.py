from win32powernap import powernap

conf = {'check_interval': 5, 'idle_interval': 30}

pnap = powernap.PowerNap(conf)
pnap.run()