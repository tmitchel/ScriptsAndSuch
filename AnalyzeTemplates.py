#! /usr/bin/env python

# Import everything from ROOT
from ROOT import *
gROOT.Macro("rootlogon.C")
import math
import array


# ===============
# options
# ===============
from optparse import OptionParser
parser = OptionParser()

parser.add_option('--file', metavar='T', type='string', action='store',
				  default='',
				  dest='file',
				  help='file name')
(options,args) = parser.parse_args()
# ==========end: options =============

f = TFile(options.file)

hists = []
for key in f.GetListOfKeys():
	hists.append(key.GetName())

for hist in hists :
	h = f.Get(hist)
	print h.GetName(), ":     %5.2f" % h.Integral()

