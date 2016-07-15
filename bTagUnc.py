#! /usr/bin/env python

import sys
from ROOT import gROOT, gStyle, sqrt, Double
from ROOT import TFile, TIter, TH1F, TDirectory, TMath, TCanvas, TLegend
gROOT.Macro("~/rootlogon.C")
gStyle.SetOptStat(0)

var = st

path = '/uscms_data/d3/tmitchel/76X_test/CMSSW_7_6_5/src/Analysis/VLQAna/test/Macro/Histograms/withSystematics/muons/'

f_ttbar = TFile(path+'ttbar.root')

h_nom = f_ttbar.Get('ana/sig/'+var).Clone()
h_bUp = f_ttbar.Get('anabcUp/sig/'+var).Clone()
h_bDown = f_ttbar.Get('anabcDown/sig/'+var).Clone()
h_lUp = f_ttbar.Get('analightUp/sig/'+var).Clone()
h_lDown = f_ttbar.Get('analightDown/sig/'+var).Clone()

h_dn_hf_diff = h_bUp.Clone()
h_dn_lf_diff = h_bDown.Clone()
h_up_hf_diff = h_lUp.Clone()
h_up_lf_diff = h_lDown.Clone()
h_dn_hf_diff.Add(h_bUp, -1)
h_dn_lf_diff.Add(h_bDown, -1)
h_up_hf_diff.Add(h_lUp, -1)
h_up_lf_diff.Add(h_lDown, -1)

hs_dn_new = hist_dn_hf[i].Clone()
hs_dn_new.Reset()
hs_dn_new.SetDirectory(0)
hs_up_new = hist_up_hf[i].Clone()
hs_up_new.Reset()
hs_up_new.SetDirectory(0)

for ibin in range(0, nbins+1):
    sumErrUp2 = 0
    sumErrDn2 = 0

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

hist_up_new.insert(i,hs_up_new)
hist_dn_new.insert(i,hs_dn_new)

###write two output root file:
f_dn = TFile(path+var+"_BTagSFdown.root", "RECREATE")
f_dn.cd()
hist_dn_new.Write()
f_dn.Close()

f_up = TFile(path+var+"_BTagSFup.root", "RECREATE")
f_up.cd()
hist_up_new.Write()
f_up.Close()

    
# for i in range(0, len(h_nom)):
    
#     hs_dn_new = hist_dn_hf[i].Clone()
#     hs_dn_new.Reset()
#     hs_dn_new.SetDirectory(0)
#     hs_up_new = hist_up_hf[i].Clone()
#     hs_up_new.Reset()
#     hs_up_new.SetDirectory(0)

    
    
