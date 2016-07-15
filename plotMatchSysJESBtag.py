#! /usr/bin/env python

# Import everything from ROOT
import sys
from ROOT import *
from setTDRStyle import *
#setTDRStyle()
gROOT.Macro("~/rootlogon.C")
gStyle.SetOptStat(0)
#gStyle.SetTitleFillColor(10)
#gStyle.SetTitleBorderSize(0)
#gStyle.SetOptStat(000000)
# =============== 
# options
# ===============
from optparse import OptionParser
parser = OptionParser()	  				  				  					  			  					  				  
parser.add_option('--var', metavar='T', type='string', action='store',
                  default='ht',
                  dest='var',
                  help='variable to plot')
parser.add_option('--runEle', action='store_true',
                  default=True,
                  help='run on electron selections')
(options,args) = parser.parse_args()
# ==========end: options =============
var = options.var
runEle = options.runEle

if runEle:
        Path  ='/Users/skhalil/Desktop/BPrime/8TeV/Analysis/Python/Apr26Plots/eleMET20Apr26/'
        title = "#it{e + jets}"
	dist = 'ele'
else:
        Path  ='/Users/skhalil/Desktop/BPrime/8TeV/Analysis/Python/Apr26PlotsMu/muMET20Apr26/'
        title = "#it{#mu +jets}"
	dist = 'mu'

f_nom       = TFile(Path+var+'_nominal_.root')
f_nomup     = TFile(Path+var+'_nominal_PUup.root')
f_nomdn     = TFile(Path+var+'_nominal_PUdn.root')
f_nomVup    = TFile(Path+var+'_nominal_VSFup.root')
f_nomVdn    = TFile(Path+var+'_nominal_VSFdn.root')
f_JESup   = TFile(Path+var+'_JESup_.root')
f_JESdn   = TFile(Path+var+'_JESdown_.root')
f_JERup   = TFile(Path+var+'_JERup_.root')
f_JERdn   = TFile(Path+var+'_JERdown_.root')
f_BTagSFup   = TFile(Path+var+'_BTagSFup_.root')
f_BTagSFdn   = TFile(Path+var+'_BTagSFdown_.root')

leg = TLegend(0.60, 0.60, 0.88, 0.88)
leg.SetBorderSize(0)
leg.SetFillColor(0)

leg2 = TLegend(0.60, 0.60, 0.88, 0.88)
leg2.SetBorderSize(0)
leg2.SetFillColor(0)

leg3 = TLegend(0.60, 0.60, 0.88, 0.88)
leg3.SetBorderSize(0)
leg3.SetFillColor(0)

leg4 = TLegend(0.60, 0.60, 0.88, 0.88)
leg4.SetBorderSize(0)
leg4.SetFillColor(0)

leg5 = TLegend(0.60, 0.60, 0.88, 0.88)
leg5.SetBorderSize(0)
leg5.SetFillColor(0)

h_data_nom = f_nom.Get('data_'+var+'_nominal') 
h_nom = f_nom.Get('totalMC_'+var+'_nominal')
h_nomup = f_nomup.Get('totalMC_'+var+'_PUUp')
h_nomdn = f_nomdn.Get('totalMC_'+var+'_PUDown')
h_nomVup = f_nomVup.Get('totalMC_'+var+'_VSFUp')
h_nomVdn = f_nomVdn.Get('totalMC_'+var+'_VSFDown')
h_JESup = f_JESup.Get('totalMC_'+var+'_JESUp')
h_JESdn = f_JESdn.Get('totalMC_'+var+'_JESDown')
h_JERup = f_JERup.Get('totalMC_'+var+'_JERUp')
h_JERdn = f_JERdn.Get('totalMC_'+var+'_JERDown')
h_BTagSFup = f_BTagSFup.Get('totalMC_'+var+'_btagUp')
h_BTagSFdn = f_BTagSFdn.Get('totalMC_'+var+'_btagDown')

htitle = ''
if var == 'njets':
    htitle = 'N_{jets}'
elif var == 'ht':
    htitle = 'H_{T} (GeV)' 

h_nomup.SetTitle("Pileup, "+title+";"+htitle) 
h_nomdn.SetTitle("Pileup, "+title+";"+htitle)
h_nomVup.SetTitle("VTagSF, "+title+";"+htitle)
h_nomVdn.SetTitle("VTagSF, "+title+";"+htitle)
h_JESup.SetTitle("JES, "+title+";"+htitle)
h_JESdn.SetTitle("JES, "+title+";"+htitle)
h_JERup.SetTitle("JER, "+title+";"+htitle)
h_JERdn.SetTitle("JER, "+title+";"+htitle)
h_BTagSFup.SetTitle("BTagSF, "+title+";"+htitle)
h_BTagSFdn.SetTitle("BTagSF, "+title+";"+htitle)

###style
h_data_nom.SetMarkerStyle(8)
h_nom.SetLineColor(2)
h_nomup.SetLineColor(4)
h_nomVup.SetLineColor(4)
h_JERup.SetLineColor(4)
h_JESup.SetLineColor(4)
h_BTagSFup.SetLineColor(4)
h_nomdn.SetLineColor(8)
h_nomVdn.SetLineColor(8)
h_JESdn.SetLineColor(8)
h_JERdn.SetLineColor(8)
h_BTagSFdn.SetLineColor(8)
h_nom.SetLineWidth(2)
h_nomup.SetLineWidth(2)
h_nomdn.SetLineWidth(2)
h_nomVup.SetLineWidth(2)
h_nomVdn.SetLineWidth(2)
h_JESup.SetLineWidth(2)
h_JESdn.SetLineWidth(2)
h_JERup.SetLineWidth(2)
h_JERdn.SetLineWidth(2)
h_BTagSFup.SetLineWidth(2)
h_BTagSFdn.SetLineWidth(2)

c1 = TCanvas('c1', 'c1', 600, 600)

#leg.AddEntry(h_data_nom, 'Data', 'p')
leg.AddEntry(h_nom, 'default', 'l')
leg.AddEntry(h_JESup, 'JES up', 'l')
leg.AddEntry(h_JESdn, 'JES down', 'l')

h_data_nom.SetTitle("JES, "+title+";"+htitle)
h_nom.SetTitle("JES, "+title+";"+htitle)
#h_data_nom.Draw('hist,e')
h_JESup.Draw('hist')
h_nom.Draw('hist same')
h_JESdn.Draw('hist same')
h_JESup.Draw('hist same')
    
leg.Draw()

delta_accp_up  = ((h_nom.Integral()-h_JESup.Integral())/h_nom.Integral())*100
delta_accp_dn  = ((h_nom.Integral()-h_JESdn.Integral())/h_nom.Integral())*100
print '_____#Delta A; >=4j,>=1t_____'
print 'Delta_A_JESup = {0:3.1f} %, Delta_A_JESdn = {1:3.1f} %, Ave = {2:3.1f}%'.format(
    delta_accp_up, delta_accp_dn, (fabs(delta_accp_up)+fabs(delta_accp_dn))/2)

#c1.Print('/Users/skhalil/Desktop/FigAN/sys_JES_'+var+'_'+dist+'.gif', 'gif')
c1.Print('/Users/skhalil/Desktop/FigAN/sys_JES_'+var+'_'+dist+'.pdf', 'pdf')
###========
c2 = TCanvas('c2', 'c2', 600, 600)

#leg2.AddEntry(h_data_nom, 'Data', 'p')
leg2.AddEntry(h_nom, 'default', 'l')
leg2.AddEntry(h_BTagSFup, 'BTagSF up', 'l')
leg2.AddEntry(h_BTagSFdn, 'BTagSF down', 'l')

h_data_nom.SetTitle("BTagSF, "+title+";"+htitle)
h_nom.SetTitle("BTagSF, "+title+";"+htitle)
#h_data_nom.Draw('hist,e')
h_BTagSFdn.Draw('hist')
h_nom.Draw('hist same')
h_BTagSFup.Draw('hist same')   

leg2.Draw()

delta_accp_up  = ((h_nom.Integral()-h_BTagSFup.Integral())/h_nom.Integral())*100
delta_accp_dn  = ((h_nom.Integral()-h_BTagSFdn.Integral())/h_nom.Integral())*100
print '_____#Delta A; >=4j,>=1t_____'
print 'Delta_A_BTagSFup = {0:3.1f} %, Delta_A_BTagSFdn = {1:3.1f} %, Ave = {2:3.1f}%'.format(
    delta_accp_up, delta_accp_dn, (fabs(delta_accp_up)+fabs(delta_accp_dn))/2)

#c2.Print('/Users/skhalil/Desktop/FigAN/sys_btag_'+var+'_'+dist+'.gif', 'gif')
c2.Print('/Users/skhalil/Desktop/FigAN/sys_btag_'+var+'_'+dist+'.pdf', 'pdf')

#================
c3 = TCanvas('c3', 'c3', 600, 600)

#leg3.AddEntry(h_data_nom, 'Data', 'p')
leg3.AddEntry(h_nom, 'default', 'l')
leg3.AddEntry(h_JERdn, 'JER down', 'l')
leg3.AddEntry(h_JERup, 'JER up', 'l')

h_data_nom.SetTitle("JER, "+title+";"+htitle)
h_nom.SetTitle("JER, "+title+";"+htitle)
#h_data_nom.Draw('hist,e')
h_JERdn.Draw('hist')
h_nom.Draw('hist same')
h_JERup.Draw('hist same')

leg3.Draw()

delta_accp_up  = ((h_nom.Integral()-h_JERup.Integral())/h_nom.Integral())*100
delta_accp_dn  = ((h_nom.Integral()-h_JERdn.Integral())/h_nom.Integral())*100
print '_____#Delta A; >=4j,>=1t_____'
print 'Delta_A_JERup = {0:3.1f} %, Delta_A_JERdn = {1:3.1f} %, Ave = {2:3.1f}%'.format(
    delta_accp_up, delta_accp_dn, (fabs(delta_accp_up)+fabs(delta_accp_dn))/2)

#c3.Print('/Users/skhalil/Desktop/FigAN/sys_JER_'+var+'_'+dist+'.gif', 'gif')
c3.Print('/Users/skhalil/Desktop/FigAN/sys_JER_'+var+'_'+dist+'.pdf', 'pdf')

c4 = TCanvas('c4', 'c4', 600, 600)

#leg4.AddEntry(h_data_nom, 'Data', 'p')
leg4.AddEntry(h_nom, 'default', 'l')
leg4.AddEntry(h_nomup, 'PU up', 'l')
leg4.AddEntry(h_nomdn, 'PU down', 'l')

h_data_nom.SetTitle("PU, "+title+";"+htitle)
h_nom.SetTitle("PU, "+title+";"+htitle)
#h_data_nom.Draw('hist,e')
h_nomdn.Draw('hist')
h_nom.Draw('hist same')
h_nomup.Draw('hist same')

leg4.Draw()

delta_accp_up  = ((h_nom.Integral()-h_nomup.Integral())/h_nom.Integral())*100
delta_accp_dn  = ((h_nom.Integral()-h_nomdn.Integral())/h_nom.Integral())*100
print '_____#Delta A; >=4j,>=1t_____'
print 'Delta_A_PUup = {0:3.1f} %, Delta_A_PUdn = {1:3.1f} %, Ave = {2:3.1f}%'.format(
    delta_accp_up, delta_accp_dn, (fabs(delta_accp_up)+fabs(delta_accp_dn))/2)

#c4.Print('/Users/skhalil/Desktop/FigAN/sys_PU_'+var+'_'+dist+'.gif', 'gif')
c4.Print('/Users/skhalil/Desktop/FigAN/sys_PU_'+var+'_'+dist+'.pdf', 'pdf')

c5 = TCanvas('c5', 'c5', 600, 600)

#leg5.AddEntry(h_data_nom, 'Data', 'p')
leg5.AddEntry(h_nom, 'default', 'l')
leg5.AddEntry(h_nomup, 'VTagSF up', 'l')
leg5.AddEntry(h_nomdn, 'VTagSF down', 'l')

h_data_nom.SetTitle("VTagSF, "+title+";"+htitle)
h_nom.SetTitle("VTagSF, "+title+";"+htitle)
#h_data_nom.Draw('hist,e')
h_nomVdn.Draw('hist ')
h_nom.Draw('hist same')
h_nomVup.Draw('hist same')

leg5.Draw()

delta_accp_up  = ((h_nom.Integral()-h_nomVup.Integral())/h_nom.Integral())*100
delta_accp_dn  = ((h_nom.Integral()-h_nomVdn.Integral())/h_nom.Integral())*100
print '_____#Delta A; >=4j,>=1t_____'
print 'Delta_A_VTagup = {0:3.1f} %, Delta_A_VTagdn = {1:3.1f} %, Ave = {2:3.1f}%'.format(
    delta_accp_up, delta_accp_dn, (fabs(delta_accp_up)+fabs(delta_accp_dn))/2)

#c5.Print('/Users/skhalil/Desktop/FigAN/sys_VTagSF_'+var+'_'+dist+'.gif', 'gif')
c5.Print('/Users/skhalil/Desktop/FigAN/sys_VTagSF_'+var+'_'+dist+'.pdf', 'pdf')

raw_input("hold on")

