#!/usr/bin/env python3

import sys
# import osgeo_utils.gdal_pansharpen as a convenience to use as a script
from osgeo_utils.gdal_pansharpen import *  # noqa
from osgeo_utils.gdal_pansharpen import main
from osgeo.gdal import deprecation_warn


deprecation_warn('gdal_pansharpen')
sys.exit(main(sys.argv))
