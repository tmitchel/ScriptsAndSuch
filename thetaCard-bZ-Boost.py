#! /usr/bin/env python

# Import everything from ROOT
from ROOT import *
import math
import array

categs = ["Boost"]
chans = ["diel_", "dimu_"]
samples = ["DY","Top","VV","BpBp800_bZbZ","BpBp900_bZbZ","BpBp1000_bZbZ","BpBp1100_bZbZ","BpBp1200_bZbZ","BpBp1300_bZbZ","BpBp1400_bZbZ","BpBp1500_bZbZ","BpBp1700_bZbZ","BpBp1800_bZbZ"]
systs = ["","__jer__plus","__jer__minus","__jec__plus","__jec__minus","__pileup__plus","__pileup__minus","__jmr__plus","__jmr__minus","__BTag__plus","__BTag__minus","__tau__plus","__tau__minus","__scale__plus","__scale__minus","__pdf__plus","__pdf__minus","__dysf__plus","__dysf__minus"]


f = TFile("templates/EMu_bZ_boost.root")

histos = []


for syst in systs :
  for sample in samples :
#   print chans[0]+categs[0]+"__"+sample+syst
    if ("VV__scale" in sample+syst) :
      continue
    if ("Top__dy" in sample+syst) :
      continue
    if ("VV__dy" in sample+syst) :
      continue
    if ("bZ__dy" in sample+syst) :
      continue
    if ("VV__pdf" in sample+syst) :
      continue
    h = f.Get(chans[0]+categs[0]+"__"+sample+syst)
    hist = h.Clone()
    hist.SetName("dil"+categs[0]+"__"+sample+syst)
    hist.SetTitle("dil"+categs[0]+"__"+sample+syst)
      
    h = f.Get(chans[1]+categs[0]+"__"+sample+syst)
    hist.Add(h)
    
    ##re-format hist
    hist2 = TH1D("b12_"+hist.GetName(),"b12_"+hist.GetTitle(),512,102.,1638.)
    for bin in range(1,512) :
      hist2.SetBinContent(bin,hist.GetBinContent(bin+34))
      hist2.SetBinError(bin,hist.GetBinError(bin+34))
    binC = 0.
    SqBinE = 0.
    for bin in range(546,1000) :
      binC = binC + hist.GetBinContent(bin)
      SqBinE = SqBinE + hist.GetBinError(bin)*hist.GetBinError(bin)
    hist2.SetBinContent(512,binC)
    hist2.SetBinError(512,TMath.Sqrt(SqBinE))

    hist2.Rebin(32)

    xbins = [102.]
    for i in range(1,3) :
      xbins.append(xbins[i-1]+2*96.)
    for i in range(3,6) :
      xbins.append(xbins[i-1]+96.)
    for i in range(6,11) :
      xbins.append(xbins[i-1]+2*96.)
    lowEdges = array.array('d')
    lowEdges.fromlist(xbins)
    nbins = len(xbins)-1
    hist2 = hist2.Rebin(nbins,hist2.GetName(),lowEdges)

#   xbins = [102.]
#   for i in range(1,13) :
#     xbins.append(xbins[i-1]+96.)
#   for i in range(13,15) :
#     xbins.append(xbins[i-1]+2*96.)
#   lowEdges = array.array('d')
#   lowEdges.fromlist(xbins)
#   nbins = len(xbins)-1
#   hist2 = hist2.Rebin(nbins,hist2.GetName(),lowEdges)


    histos.append(hist2)

for hist in histos :
  print hist.GetName(), ":  %5.2f" % hist.Integral()


for i in range(0,len(categs)) :
  p = i*len(samples)
  h = histos[p].Clone()
  print "Name = ", h.GetName()
  h.SetName("comb"+categs[i]+"__SM")
  h.SetTitle("comb"+categs[i]+"__SM")
  # add TTjets
  h.Add(histos[p+1])
  print h.GetName()
  # add VV
  h.Add(histos[p+2])
  print h.GetName()
  nbins = h.GetNbinsX()
  for bin in range(1, nbins+1) :
    bc = h.GetBinContent(bin)
    err = h.GetBinError(bin)
    rerr = -0.01
    if (err!=0) :
      rerr = err/bc;
    print "bin=",bin,"; rel err = %5.1f" % (100*rerr), "%"

fc = TFile("templates/bZ-boost-b12.root","recreate")
fc.cd()

for hist in histos :
  hist.Write()

h.Draw()
