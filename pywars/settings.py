print "Settings: ",
try:
    from config.production import *
    print "PRODUCTION"
except ImportError:
    from config.development import *
    print "DEVELOPMENT"
