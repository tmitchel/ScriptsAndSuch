#! /usr/bin/env python

import sys
#from ROOT import gROOT, gStyle, sqrt, Double
#from ROOT import TFile, TIter, TH1F, TDirectory, TMath, TCanvas, TLegend
from FWCore.ParameterSet.VarParsing import VarParsing
from ROOT import *
from math import sqrt
gROOT.Macro("~/rootlogon.C")
gStyle.SetOptStat(0)

options = VarParsing('analysis')
options.register('var', 'resReco_bZ_1b',
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    'Variable name'
    )
options.register('path', '',
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    'path to root files'
    )
options.register('fileName', 'ttbar.root',
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    'name of root file',
    )
options.parseArguments()
path = options.path
fileName = options.fileName
var = options.var

f = TFile(path+fileName)

h_nom = f.Get('massReco/'+var).Clone()
h_bUp = f.Get('recobc__plus/'+var).Clone()
h_bDown = f.Get('recobc__minus/'+var).Clone()
h_lUp = f.Get('recolight__plus/'+var).Clone()
h_lDown = f.Get('recolight__minus/'+var).Clone()

hs_dn_new = h_bDown.Clone()
hs_dn_new.Reset()
hs_dn_new.SetDirectory(0)
hs_up_new = h_bUp.Clone()
hs_up_new.Reset() 
hs_up_new.SetDirectory(0)

h_up_hf_diff = h_bUp.Clone()
h_dn_hf_diff = h_bDown.Clone()
h_up_lf_diff = h_lUp.Clone()
h_dn_lf_diff = h_lDown.Clone()
h_dn_hf_diff.Add(h_nom, -1)
h_dn_lf_diff.Add(h_nom, -1)
h_up_hf_diff.Add(h_nom, -1)
h_up_lf_diff.Add(h_nom, -1)

nbins = h_nom.GetNbinsX()
for ibin in range(0, nbins+1):

    var_dn_hf = h_dn_hf_diff.GetBinContent(ibin+1)
    var_dn_lf = h_dn_lf_diff.GetBinContent(ibin+1)
    var_up_hf = h_up_hf_diff.GetBinContent(ibin+1)
    var_up_lf = h_up_lf_diff.GetBinContent(ibin+1)

    bin_up_var_hf = max(var_dn_hf,var_up_hf) # find the largest positive bin content variation due to SFb variation (set to 0 if both negative)
    if( bin_up_var_hf < 0. ): bin_up_var_hf = 0.
    bin_dn_var_hf = min(var_dn_hf,var_up_hf) # find the largest negative bin content variation due to SFb variation (set to 0 if both positive)
    if( bin_dn_var_hf > 0. ): bin_dn_var_hf = 0.

    bin_up_var_lf = max(var_dn_lf,var_up_lf) # find the largest positive bin content variation due to SFl variation (set to 0 if both negative)
    if( bin_up_var_lf < 0. ): bin_up_var_lf = 0.
    bin_dn_var_lf = min(var_dn_lf,var_up_lf) # find the largest negative bin content variation due to SFl variation (set to 0 if both positive)
    if( bin_dn_var_lf > 0. ): bin_dn_var_lf = 0.

    bin_up_var = sqrt( bin_up_var_hf**2 + bin_up_var_lf**2 )
    bin_dn_var = sqrt( bin_dn_var_hf**2 + bin_dn_var_lf**2 )

    hs_up_new.SetBinContent(ibin+1, h_nom.GetBinContent(ibin+1) + bin_up_var)
    hs_dn_new.SetBinContent(ibin+1, h_nom.GetBinContent(ibin+1) - bin_dn_var)

print fileName
print hs_up_new.Integral(), hs_dn_new.Integral()

hs_dn_new.SetName(var+'__BTagSF__minus')
hs_up_new.SetName(var+'__BTagSF__plus')

fout = TFile(fileName.split('.')[0]+'_'+options.var+'_BTagSF.root', 'recreate')
fout.cd()
hs_up_new.Write()
hs_dn_new.Write()
fout.Close()
    

    
    
