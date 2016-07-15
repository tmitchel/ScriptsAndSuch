#! /usr/bin/env python

import sys
from ROOT import gROOT, gStyle, sqrt, Double
from ROOT import TFile, TIter, TH1F, TDirectory, TMath, TCanvas, TLegend
gROOT.Macro("~/rootlogon.C")
gStyle.SetOptStat(0)

runEle = False
#ht = 'ht'
#ht = 'ht0t'
#ht = 'ht1t'
ht = 'ht2t'

if runEle:
    p = 'Jun15Plots/eleAug04/'
    ch = 'ele'
else:
    p = 'Jun15PlotsMu/muAug04/'
    ch = 'mu'

    
def getHisto(file, histList):
    nextKey = TIter( file.GetListOfKeys() )
    for key in nextKey:
        #print key.GetName()
        #print file.Get(key.GetName()).Integral()
        histList.append(file.Get(key.GetName()))
    return histList

f_nom   = TFile(p+ht+'_nominal_'+ch+'.root')
f_dn_hf = TFile(p+ht+'_BTagSFdownHF_'+ch+'.root')
f_dn_lf = TFile(p+ht+'_BTagSFdownLF_'+ch+'.root')
f_up_hf = TFile(p+ht+'_BTagSFupHF_'+ch+'.root')
f_up_lf = TFile(p+ht+'_BTagSFupLF_'+ch+'.root')

hist_nom = []
hist_dn_new = []
hist_up_new = []
hist_dn_hf = []
hist_dn_lf = []
hist_up_hf = []
hist_up_lf = []


getHisto(f_nom, hist_nom)
getHisto(f_dn_hf, hist_dn_hf)
getHisto(f_dn_lf, hist_dn_lf)
getHisto(f_up_hf, hist_up_hf)
getHisto(f_up_lf, hist_up_lf)

#position 7 is Top, rest of the histograms have no variation
nbins = hist_nom[7].GetNbinsX()
for i in range(0, len(hist_nom)):

    hs_dn_new = hist_dn_hf[i].Clone()
    hs_dn_new.Reset()
    hs_dn_new.SetDirectory(0)
    hs_up_new = hist_up_hf[i].Clone()
    hs_up_new.Reset()
    hs_up_new.SetDirectory(0)

    h_dn_hf_diff = hist_dn_hf[i].Clone()
    h_dn_lf_diff = hist_dn_lf[i].Clone()
    h_up_hf_diff = hist_up_hf[i].Clone()
    h_up_lf_diff = hist_up_lf[i].Clone()
    h_dn_hf_diff.Add(hist_nom[i], -1)
    h_dn_lf_diff.Add(hist_nom[i], -1)
    h_up_hf_diff.Add(hist_nom[i], -1)
    h_up_lf_diff.Add(hist_nom[i], -1)

    for ibin in range(0,nbins+1) :
        sumErrUp2 = 0
        sumErrDn2 = 0
        
        var_dn_hf = h_dn_hf_diff.GetBinContent(ibin+1)
        var_dn_lf = h_dn_lf_diff.GetBinContent(ibin+1)
        var_up_hf = h_up_hf_diff.GetBinContent(ibin+1)
        var_up_lf = h_up_lf_diff.GetBinContent(ibin+1)

        # <--------------------------- added by Dinko
        # add the hf and lf variations in quadrature
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

        hs_up_new.SetBinContent(ibin+1, hist_nom[i].GetBinContent(ibin+1) + bin_up_var)
        hs_dn_new.SetBinContent(ibin+1, hist_nom[i].GetBinContent(ibin+1) - bin_dn_var)
        
        #print 'nominal', hist_nom[i].GetBinContent(ibin+1)
        
        # <--------------------------- added by Dinko
    print ' cycle done -----------'
    hist_up_new.insert(i,hs_up_new)
    hist_dn_new.insert(i,hs_dn_new)
    
#print 'top nominal= ', hist_nom[7].Integral()
#print 'top up', hist_up_new[7].Integral()
#print 'top dn', hist_dn_new[7].Integral()

###write two output root file:
f_dn = TFile(p+ht+"_BTagSFdown_"+ch+".root", "RECREATE")
f_dn.cd()
for i in range(0, len(hist_nom)):
    hist_dn_new[i].Write()
    if i == 7: print 'top dn', hist_dn_new[i].Integral()
f_dn.Close()

f_up = TFile(p+ht+"_BTagSFup_"+ch+".root", "RECREATE")
f_up.cd()
for i in range(0, len(hist_nom)):
    hist_up_new[i].Write()
f_up.Close()

#####plot up/down variation for new and old treatment of uncertainties
##hist_dn[7].SetTitle("Btag Down Uncertainties; H_{T} (GeV) ;")
##hist_dn_new[7].SetLineColor(4)
##hist_dn[7].SetLineColor(2)
##leg = TLegend(0.4, 0.4, 0.9, 0.9)
##leg.SetBorderSize(0)
##leg.SetFillColor(0)

##hist_up[7].SetTitle("Btag Up Uncertainties; H_{T} (GeV) ;")
##hist_up_new[7].SetLineColor(4)
##hist_up[7].SetLineColor(2)
##leg2 = TLegend(0.4, 0.4, 0.9, 0.9)
##leg2.SetBorderSize(0)
##leg2.SetFillColor(0)


##c1 = TCanvas('c1', 'c1', 800, 600)
##c1.Divide(2,1)
##c1.cd(1)

##leg.AddEntry(hist_dn_new[7], 'HF/LF Coherent down', 'l')
##leg.AddEntry(hist_dn[7], 'HF/LF Indepentent down', 'l')

##hist_dn_new[7].Draw("hist")
##hist_dn[7].Draw("same, hist")
##leg.Draw("same")

##c1.cd(2)

##leg2.AddEntry(hist_up_new[7], 'HF/LF Coherent up', 'l')
##leg2.AddEntry(hist_up[7], 'HF/LF Independent up', 'l')

##hist_up_new[7].Draw("hist")
##hist_up[7].Draw("same, hist")
##leg2.Draw("same")






raw_input("hold on")
