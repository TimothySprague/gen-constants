import sys

from .main import main

sys.exit(main(sys.argv[1:] or None))
