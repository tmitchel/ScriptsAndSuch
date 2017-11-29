#! /usr/bin/env python

# Import everything from ROOT
from ROOT import *
import math
import array

# ===============
# options
# ===============
#from optparse import OptionParser
#parser = OptionParser()
#
#parser.add_option('--file', metavar='T', type='string', action='store',
#				  default='',
#				  dest='file',
#				  help='file name')
#(options,args) = parser.parse_args()
# ==========end: options =============


files = ["Zmumu/dimu_templates/allsyst_dimu_boostReco_bZ.root","Zelel/diel_templates/allsyst_diel_boostReco_bZ.root"]
		 
#newf = ["templates.root"]

newname = "templates/EMu_bZ_boost.root"
newf = TFile(newname,"recreate")
newf.Close()
#new_hists = []

for file in files :
	f = TFile(file)
	hists = []
	for key in f.GetListOfKeys():
		hists.append(key.GetName())
	nf = TFile(newname,"update")
	for hist in hists :
		h = f.Get(hist)
		print h.GetName(), ":     %5.2f" % h.Integral()
		h.Write()
	nf.Close()


