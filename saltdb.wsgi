#!/usr/bin/env python

import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/opt/saltdb/")

from app import app as application
