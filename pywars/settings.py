
try:
    from config.production import *
except ImportError:
    from config.development import *
