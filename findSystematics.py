#! /usr/bin/env python

import sys
from ROOT import *
import math

gROOT.Macro("~/rootlogon.C")
gStyle.SetOptStat(0)

from optparse import OptionParser
parser = OptionParser()
parser.add_option('--var', metavar='T', type='string', action='store',
                  default='/sig/st',
                  dest='var',
                  help='variable to plot'
)
parser.add_option('--lep', metavar='T', type='string', action='store',
                  default='mu',
                  dest='lep',
                  help='mu or el'
)
parser.add_option('--path', metavar='T', type='string', action='store',
                  default='/uscms_data/d3/tmitchel/76X_test/CMSSW_7_6_5/src/Analysis/VLQAna/test/Macro/Histograms/withSystematics/electrons/',
                  dest='path',
                  help='path to root files'
)
(options,args) = parser.parse_args()
var = options.var
lep = options.lep
Path = options.path

PatH = '/uscms_data/d3/tmitchel/76X_test/CMSSW_7_6_5/src/Analysis/VLQAna/test/Macro/sys/electrons/'

if lep == 'mu':
    title = '#mu#mu'
    f_data = TFile(Path+'muons.root')
    Lep = 'Mu'
elif lep == 'el':
    title = '#e#e'
    f_data = TFile(Path+'electrons.root')
    Lep = 'El'
else:
    sys.exit('Wrong z decay mode')

f_ttbar = TFile(Path+'ttbar.root')
f_DY100to200 = TFile(Path+'dy_ht100-200.root')
f_DY200to400 = TFile(Path+'dy_ht200-400.root')
f_DY400to600 = TFile(Path+'dy_ht400-600.root')
f_DY600toInf = TFile(Path+'dy_ht600-Inf.root')
f_ZZto2 = TFile(Path+'ZZto2.root')
f_ZZto4 = TFile(Path+'ZZto4.root')
f_WW = TFile(Path+'WW.root')
f_WZto2 = TFile(Path+'WZto2.root')
f_WZto3 = TFile(Path+'WZto3.root')
f_bprime800 = TFile(Path+'bprime800.root')
f_bprime1000 = TFile(Path+'bprime1000.root')
f_bprime1200 = TFile(Path+'bprime1200.root')
f_tprime800 = TFile(Path+'tprime800.root')
f_tprime1000 = TFile(Path+'tprime1000.root')
f_tprime1200 = TFile(Path+'tprime1200.root')

f_ttbarUP = TFile(PatH+'/btag/'+Lep+'_ttbar_'+var.split('/')[2]+'_'+'BTagSFup'+'.root')
f_ttbarDOWN = TFile(PatH+'/btag/'+Lep+'_ttbar_'+var.split('/')[2]+'_'+'BTagSFdown'+'.root')
f_DY100to200UP = TFile(PatH+'/btag/'+Lep+'_dy_ht100-200_'+var.split('/')[2]+'_'+'BTagSFup'+'.root')
f_DY100to200DOWN = TFile(PatH+'/btag/'+Lep+'_dy_ht100-200_'+var.split('/')[2]+'_'+'BTagSFdown'+'.root')
f_DY200to400UP = TFile(PatH+'/btag/'+Lep+'_dy_ht200-400_'+var.split('/')[2]+'_'+'BTagSFup'+'.root')
f_DY200to400DOWN = TFile(PatH+'/btag/'+Lep+'_dy_ht200-400_'+var.split('/')[2]+'_'+'BTagSFdown'+'.root')
f_DY400to600UP = TFile(PatH+'/btag/'+Lep+'_dy_ht400-600_'+var.split('/')[2]+'_'+'BTagSFup'+'.root')
f_DY400to600DOWN = TFile(PatH+'/btag/'+Lep+'_dy_ht400-600_'+var.split('/')[2]+'_'+'BTagSFdown'+'.root')
f_DY600toInfUP = TFile(PatH+'/btag/'+Lep+'_dy_ht600-Inf_'+var.split('/')[2]+'_'+'BTagSFup'+'.root')
f_DY600toInfDOWN = TFile(PatH+'/btag/'+Lep+'_dy_ht600-Inf_'+var.split('/')[2]+'_'+'BTagSFdown'+'.root')
f_ZZto2UP = TFile(PatH+'/btag/'+Lep+'_ZZto2_'+var.split('/')[2]+'_'+'BTagSFup'+'.root')
f_ZZto2DOWN = TFile(PatH+'/btag/'+Lep+'_ZZto2_'+var.split('/')[2]+'_'+'BTagSFdown'+'.root')
f_ZZto4UP = TFile(PatH+'/btag/'+Lep+'_ZZto4_'+var.split('/')[2]+'_'+'BTagSFup'+'.root')
f_ZZto4DOWN = TFile(PatH+'/btag/'+Lep+'_ZZto4_'+var.split('/')[2]+'_'+'BTagSFdown'+'.root')
f_WWUP = TFile(PatH+'/btag/'+Lep+'_WW_'+var.split('/')[2]+'_'+'BTagSFup'+'.root')
f_WWDOWN = TFile(PatH+'/btag/'+Lep+'_WW_'+var.split('/')[2]+'_'+'BTagSFdown'+'.root')
f_WZto2UP = TFile(PatH+'/btag/'+Lep+'_WZto2_'+var.split('/')[2]+'_'+'BTagSFup'+'.root')
f_WZto2DOWN = TFile(PatH+'/btag/'+Lep+'_WZto2_'+var.split('/')[2]+'_'+'BTagSFdown'+'.root')
f_WZto3UP = TFile(PatH+'/btag/'+Lep+'_WZto3_'+var.split('/')[2]+'_'+'BTagSFup'+'.root')
f_WZto3DOWN = TFile(PatH+'/btag/'+Lep+'_WZto3_'+var.split('/')[2]+'_'+'BTagSFdown'+'.root')

fileList = []
fileList.append(f_ttbar)
fileList.append(f_DY100to200)
fileList.append(f_DY200to400)
fileList.append(f_DY400to600)
fileList.append(f_DY600toInf)
fileList.append(f_ZZto2)
fileList.append(f_ZZto4)
fileList.append(f_WW)
fileList.append(f_WZto2)
fileList.append(f_WZto3)
fileList.append(f_bprime800)
fileList.append(f_bprime1000)
fileList.append(f_bprime1200)
fileList.append(f_tprime800)
fileList.append(f_tprime1000)
fileList.append(f_tprime1200)

btagList = []
btagList.append(f_DY100to200UP)
btagList.append(f_DY100to200DOWN)
btagList.append(f_DY200to400UP)
btagList.append(f_DY200to400DOWN)
btagList.append(f_DY400to600UP)
btagList.append(f_DY400to600DOWN)
btagList.append(f_DY600toInfUP)
btagList.append(f_DY600toInfDOWN)
btagList.append(f_ttbarUP)
btagList.append(f_ttbarDOWN)
btagList.append(f_ZZto2UP)
btagList.append(f_ZZto2DOWN)
btagList.append(f_ZZto4UP)
btagList.append(f_ZZto4DOWN)
btagList.append(f_WWUP)
btagList.append(f_WWDOWN)
btagList.append(f_WZto2UP)
btagList.append(f_WZto2DOWN)
btagList.append(f_WZto3UP)
btagList.append(f_WZto3DOWN)


xs = [ 831.76, 147.4 * 1.23, 40.99 * 1.23, 5.678 * 1.23, 2.198 * 1.23, .564, 3.22, 12.178, 4.42965, 1.212, 1, 1, 1, 1, 1, 1]
num = [187626200, 2655294, 962195, 1069003, 1031103, 8719200, 31394787, 1965200, 2000000, 10747136, 831200./9., 822800./9, 830400./9., 788200./9., 818600./9., 817800./9.]

f = TFile('sys/'+var.split('/')[2]+'.root', 'RECREATE')

name = str(var.split('/')[2])
h_dy_up = f_DY100to200UP.Get(name).Clone()
h_dy_dn = f_DY100to200DOWN.Get(name).Clone()
h_vv_up = f_ZZto4UP.Get(name).Clone()
h_vv_dn = f_ZZto4DOWN.Get(name).Clone()
h_ttbar_up = f_ttbarUP.Get(name).Clone()
h_ttbar_dn = f_ttbarDOWN.Get(name).Clone()

h_dy_up.Reset()
h_dy_dn.Reset()
h_vv_up.Reset()
h_vv_dn.Reset()
h_ttbar_up.Reset()
h_ttbar_dn.Reset()

h_dy_up.SetName('di'+lep+'__DY__bTag__plus')
h_dy_dn.SetName('di'+lep+'__DY__bTag__minus')
h_ttbar_up.SetName('di'+lep+'__Top__bTag__plus')
h_ttbar_dn.SetName('di'+lep+'__Top__bTag__minus')
h_vv_up.SetName('di'+lep+'__VV__bTag__plus')
h_vv_dn.SetName('di'+lep+'__VV__bTag__minus')
    
j = 0
for fileName in btagList:
    hist = fileName.Get(name).Clone()
    if j >= 0 and j <= 1:
        hist.Scale(xs[1]*2200/num[1])
    elif j >=2 and j <= 3: 
        hist.Scale(xs[2]*2200/num[2])
    if j >= 4 and j <= 5:
        hist.Scale(xs[3]*2200/num[3])
    elif j >=6 and j <= 7: 
        hist.Scale(xs[4]*2200/num[4])
    elif j >= 8 and j <= 9:
        hist.Scale(xs[0]*2200/num[0])
    elif j >= 10 and j <= 11:
        hist.Scale(xs[5]*2200/num[5])
    elif j >=12 and j <= 13: 
        hist.Scale(xs[6]*2200/num[6])
    elif j >= 14 and j <= 15:
        hist.Scale(xs[7]*2200/num[7])
    elif j >=16 and j <= 17: 
        hist.Scale(xs[8]*2200/num[8])
    elif j >=18 and j <= 19: 
        hist.Scale(xs[9]*2200/num[9])

    if j >= 0 and j <= 7 and j % 2 == 0:
        h_dy_up.Add(hist)
    if j >= 0 and j <= 7 and j % 2 != 0:
        h_dy_dn.Add(hist)
    if j >= 8 and j <= 9 and j % 2 == 0:
        h_ttbar_up.Add(hist)
    if j >= 8 and j <= 9 and j % 2 != 0:
        h_ttbar_dn.Add(hist)
    if j >= 10 and j <= 19 and j % 2 == 0:
        h_vv_up.Add(hist)
    if j >= 10 and j <= 19 and j % 2 != 0:
        h_vv_dn.Add(hist)
    j+=1

h_dy_up.Write()
h_dy_dn.Write()
h_ttbar_up.Write()
h_ttbar_dn.Write()
h_vv_up.Write()
h_vv_dn.Write()

systList = ['Jer', 'Jec', 'Pileup']

for syst in systList:
    sysList = ['', syst+'Up', syst+'Down']
    sysName = ['', '__'+syst+'__plus','__'+ syst+'__minus']
    meh = 0
    for shift in sysList:
        name = str('ana'+shift+var)
        h_dy = f_DY100to200.Get(name).Clone()
        h_vv = f_ZZto4.Get(name).Clone()
        h_ttbar = f_ttbar.Get(name).Clone()
        
        h_dy.Reset()
        h_vv.Reset() 
        h_ttbar.Reset()

        i = 0
        for fileName in fileList:
            if i >= 10:
                break
            hist = fileName.Get(name).Clone()
            hist.Scale(xs[i] * 2200 / num[i])
            if i >= 1 and i <= 4 :
                h_dy.Add(hist)
            elif i >= 5 and i <= 9:
                h_vv.Add(hist)
            elif i == 0:
                h_ttbar = hist
            i += 1
                
        h_vv.SetName('di'+lep+'__VV'+sysName[meh])
        h_dy.SetName('di'+lep+'__DY'+sysName[meh])
        h_ttbar.SetName('di'+lep+'__Top'+sysName[meh])
        if (shift != ''):
            h_vv.Write()
            h_dy.Write()
            h_ttbar.Write()
        elif (shift == '' and syst == 'Jer'):
            h_vv.Write()
            h_dy.Write()
            h_ttbar.Write()
        meh += 1

names = str('ana'+var)

h_bprime800 = f_bprime800.Get(names).Clone()
h_bprime1000 = f_bprime1000.Get(names).Clone()
h_bprime1200 = f_bprime1200.Get(names).Clone()
h_tprime800 = f_tprime800.Get(names).Clone()
h_tprime1000 = f_tprime1000.Get(names).Clone()
h_tprime1200 = f_tprime1200.Get(names).Clone()

channels =['Z', 'H']
for channel in channels:
    h_bprime800.Reset()
    h_bprime1000.Reset()
    h_bprime1200.Reset()
    h_tprime800.Reset()
    h_tprime1000.Reset()
    h_tprime1200.Reset()
    ii = 0
    for fileName in fileList:
        if ii >= 10:
            if channel == 'Z':
                namess = str('ana'+var)
            elif channel == 'H':
                namess = str('anaH'+var)
            hist = fileName.Get(namess).Clone()
            hist.Scale(xs[i] * 2200 / num[i])
            if ii ==10:
                h_bprime800.Add(hist)
            elif  ii == 11:
                h_bprime1000.Add(hist)
            elif ii == 12:
                h_bprime1200.Add(hist)
            elif ii == 13:
                h_tprime800.Add(hist)
            elif ii == 14:
                h_tprime1000.Add(hist)
            elif ii == 15:
                h_tprime1200.Add(hist)
        ii += 1
    h_bprime800.SetName("di"+lep+"__BB_bZb"+channel+"_M800")
    h_bprime1000.SetName("di"+lep+"__BB_bZb"+channel+"_M1000")
    h_bprime1200.SetName("di"+lep+"__BB_bZb"+channel+"_M1200")
    h_tprime800.SetName("di"+lep+"__TT_tZt"+channel+"_M800")
    h_tprime1000.SetName("di"+lep+"__TT_tZt"+channel+"_M1000")
    h_tprime1200.SetName("di"+lep+"__TT_tZt"+channel+"_M1200")

    h_bprime800.Write()
    h_bprime1000.Write()
    h_bprime1200.Write()
    h_tprime800.Write()
    h_tprime1000.Write()
    h_tprime1200.Write()

h_data = f_data.Get("ana"+var)
h_data.SetName("di"+lep+"__DATA")
h_data.Write()
print ('file: sys/'+var.split('/')[2]+'.root has been written')
f.Close()
        




