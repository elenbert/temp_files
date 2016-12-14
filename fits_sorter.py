#!/bin/python

import os
import shutil
from astropy.io import fits

def copyifnotexists(what_desc, src_dir, src_file, dst_dir):
	if not os.path.isfile(dst_dir + "/" + src_file):
		print "Copying " + what_desc + " file " + src_file + " to " + dst_dir + "\n"
		shutil.copy2(src_dir + src_file, dst_dir)
	else:
		print "File " + src_file + " already exists in " + dst_dir + "  Skipping...\n"

for fitsfile in os.listdir("./CMR-AZT8/ALL/"):
	if fitsfile.endswith(".fit"):
		print "Working file: " + fitsfile

		hdulist = fits.open("./CMR-AZT8/ALL/" + fitsfile)

		objectname = hdulist[0].header['OBJECT']

		targetpath = "./CMR-AZT8/filtered/" + objectname

		if not os.path.exists(targetpath):
			os.makedirs(targetpath)

		if "flat" in objectname:
			copyifnotexists("FLAT FIELD", "./CMR-AZT8/ALL/", fitsfile, targetpath)
			continue

		if "dark" in objectname:
			copyifnotexists("DARK", "./CMR-AZT8/ALL/", fitsfile, targetpath)
			continue

		if "bias" in objectname:
			copyifnotexists("BIAS", "./CMR-AZT8/ALL/", fitsfile, targetpath)
			continue

		filtername = "NO FILTER"

		try:
			filtername = hdulist[0].header['FILTER']
		except:
			''' just skip errors with such stragne files and put them to separate directory "NO FILTER"  '''
			pass

		hdulist.close()

		print "\tObject: " + objectname
		print "\tFilter: " + filtername

		extended_targetpath = targetpath + "/" + filtername

		if not os.path.exists(extended_targetpath):
			os.makedirs(extended_targetpath)

		copyifnotexists(objectname, "./CMR-AZT8/ALL/", fitsfile, extended_targetpath)


