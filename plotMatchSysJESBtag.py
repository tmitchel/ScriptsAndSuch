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
                  default=False,
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
        Path  ='/home/tmitchell/Documents/Systematics/muons'
        title = "#it{#mu +jets}"
	dist = 'mu'

f_nom       = TFile(Path+'ana'+var+'.root')
f_Pup     =  TFile(Path+'anaPileupUp'+var+'.root')
f_Pdn     = TFile(Path+'anaPileupDown'+var+'.root')
f_JECup   = TFile(Path+'anaJecUp'+var+'.root')
f_JECdn   = TFile(Path+'anaJecDown'+var+'.root')
f_JERup   = TFile(Path+'anaJerUp'+var+'.root')
f_JERdn   = TFile(Path+'anaJerDown'+var+'.root')
f_BTagSFup   = TFile(Path+'anabcUp'+var+'.root')
f_BTagSFdn   = TFile(Path+'anabcDown'+var+'.root')
f_lTagSFup   = TFile(Path+'analightUp'+var+'.root')
f_lTagSFdown = TFile(Path+'analightDown'+var+'.root')

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

#h_data_nom = f_nom.Get(var) 
h_nom = f_nom.Get(var)
h_Pup = f_nomup.Get(var)
h_Pdn = f_nomdn.Get(var)
h_lTagSFup = f_nomVup.Get(var)
h_lTagSFdn = f_nomVdn.Get(var)
h_JECup = f_JESup.Get(var)
h_JECdn = f_JESdn.Get(var)
h_JERup = f_JERup.Get(var)
h_JERdn = f_JERdn.Get(var)
h_BTagSFup = f_BTagSFup.Get(var)
h_BTagSFdn = f_BTagSFdn.Get(var)

htitle = ''
if var == 'njets':
    htitle = 'N_{jets}'
elif var == 'ht':
    htitle = 'H_{T} (GeV)' 

h_nomup.SetTitle("Pileup, "+title+";"+htitle) 
h_nomdn.SetTitle("Pileup, "+title+";"+htitle)
h_lTagSFup.SetTitle("lightTagSF, "+title+";"+htitle)
h_lTagSFdn.SetTitle("lightTagSF, "+title+";"+htitle)
h_JECup.SetTitle("JEC, "+title+";"+htitle)
h_JECdn.SetTitle("JEC, "+title+";"+htitle)
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
h_JECup.Draw('hist')
h_nom.Draw('hist same')
h_JECdn.Draw('hist same')
h_JECup.Draw('hist same')
    
leg.Draw()

delta_accp_up  = ((h_nom.Integral()-h_JERup.Integral())/h_nom.Integral())*100
delta_accp_dn  = ((h_nom.Integral()-h_JERdn.Integral())/h_nom.Integral())*100
print '_____#Delta A; >=4j,>=1t_____'
print 'Delta_A_JERup = {0:3.1f} %, Delta_A_JERdn = {1:3.1f} %, Ave = {2:3.1f}%'.format(
    delta_accp_up, delta_accp_dn, (fabs(delta_accp_up)+fabs(delta_accp_dn))/2)

#c1.Print('/Users/skhalil/Desktop/FigAN/sys_JES_'+var+'_'+dist+'.gif', 'gif')
c1.Print('/home/tmitchell/Documents/Systematics/muons/JEC_'+var+'_'+dist+'.pdf', 'pdf')
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
c2.Print('/home/tmitchell/Documents/Systematics/muons/btag_'+var+'_'+dist+'.pdf', 'pdf')

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
c3.Print('/home/tmitchell/Documents/Systematics/muons/JER_'+var+'_'+dist+'.pdf', 'pdf')

c4 = TCanvas('c4', 'c4', 600, 600)

#leg4.AddEntry(h_data_nom, 'Data', 'p')
leg4.AddEntry(h_nom, 'default', 'l')
leg4.AddEntry(h_Pup, 'PU up', 'l')
leg4.AddEntry(h_Pdn, 'PU down', 'l')

h_data_nom.SetTitle("PU, "+title+";"+htitle)
h_nom.SetTitle("PU, "+title+";"+htitle)
#h_data_nom.Draw('hist,e')
h_Pdn.Draw('hist')
h_nom.Draw('hist same')
h_Pup.Draw('hist same')

leg4.Draw()

delta_accp_up  = ((h_nom.Integral()-h_Pup.Integral())/h_nom.Integral())*100
delta_accp_dn  = ((h_nom.Integral()-h_Pdn.Integral())/h_nom.Integral())*100
print '_____#Delta A; >=4j,>=1t_____'
print 'Delta_A_PUup = {0:3.1f} %, Delta_A_PUdn = {1:3.1f} %, Ave = {2:3.1f}%'.format(
    delta_accp_up, delta_accp_dn, (fabs(delta_accp_up)+fabs(delta_accp_dn))/2)

#c4.Print('/Users/skhalil/Desktop/FigAN/sys_PU_'+var+'_'+dist+'.gif', 'gif')
c4.Print('/home/tmitchell/Documents/Systematics/muons/PU_'+var+'_'+dist+'.pdf', 'pdf')

c5 = TCanvas('c5', 'c5', 600, 600)

#leg5.AddEntry(h_data_nom, 'Data', 'p')
leg5.AddEntry(h_nom, 'default', 'l')
leg5.AddEntry(h_nomup, 'lightTagSF up', 'l')
leg5.AddEntry(h_nomdn, 'lightTagSF down', 'l')

h_data_nom.SetTitle("lightTagSF, "+title+";"+htitle)
h_nom.SetTitle("lightTagSF, "+title+";"+htitle)
#h_data_nom.Draw('hist,e')
h_lTagSFdn.Draw('hist ')
h_nom.Draw('hist same')
h_lTagSFup.Draw('hist same')

leg5.Draw()

delta_accp_up  = ((h_nom.Integral()-h_lTagSFup.Integral())/h_nom.Integral())*100
delta_accp_dn  = ((h_nom.Integral()-h_lTagSFdn.Integral())/h_nom.Integral())*100
print '_____#Delta A; >=4j,>=1t_____'
print 'Delta_A_lTagup = {0:3.1f} %, Delta_A_lTagdn = {1:3.1f} %, Ave = {2:3.1f}%'.format(
    delta_accp_up, delta_accp_dn, (fabs(delta_accp_up)+fabs(delta_accp_dn))/2)

#c5.Print('/Users/skhalil/Desktop/FigAN/sys_VTagSF_'+var+'_'+dist+'.gif', 'gif')
c5.Print('/home/tmitchell/Documents/Systematics/muons/lTagSF_'+var+'_'+dist+'.pdf', 'pdf')

raw_input("hold on")

