#!/user/bin/env pythong

import sys
import os
import subprocess
from ROOT import *
from array import array

gROOT.Macro("~/rootlogon.C")
gStyle.SetOptStat(0)

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--Path", type='string', action='store',
                  default='Histograms/withSystematics/electrons/',
                  dest='Path',
                  help='Path to root files'
)
parser.add_option("--var", type='string', action='store',
                  default='ht',
                  dest='var',
                  help='var to add'
)
(options,args) = parser.parse_args()
Path = options.Path
var = options.var
toHere='/uscms_data/d3/tmitchel/76X_test/CMSSW_7_6_5/src/Analysis/VLQAna/test/Macro/'

f_DY100to200 = TFile(toHere+Path+'dy_ht100-200.root')
f_DY200to400 = TFile(toHere+Path+'dy_ht200-400.root')
f_DY400to600 = TFile(toHere+Path+'dy_ht400-600.root')
f_DY600toInf = TFile(toHere+Path+'dy_ht600-Inf.root')
f_ttbar = TFile(toHere+Path+'ttbar.root')
f_ZZTo2L2Nu     = TFile(toHere+Path+'ZZto2.root')
f_WZTo2L2Q      = TFile(toHere+Path+'WZto2.root')
f_WWTo2L2Nu   = TFile(toHere+Path+'WW.root')
f_WZTo3LNu      = TFile(toHere+Path+'WZto3.root')
f_ZZTo4L            = TFile(toHere+Path+'ZZto4.root')

f_DY = [f_DY100to200, f_DY200to400, f_DY400to600, f_DY600toInf]
f_VV = [f_ZZTo2L2Nu, f_WZTo2L2Q, f_WWTo2L2Nu, f_WZTo3LNu, f_ZZTo4L]

gSF = 1.0
Top_xs            = 831.76  *gSF
dy_xs = [147.4 * 1.23, 40.99 * 1.23, 5.678 * 1.23, 2.198 * 1.23]
# DY100to200_xs     = 147.4   *gSF *1.23
# DY200to400_xs     = 40.99   *gSF *1.23
# DY400to600_xs     = 5.678   *gSF *1.23
# DY600toInf_xs     = 2.198   *gSF *1.23
vv_xs = [.564, 3.22, 12.178, 4.42965, 1.212]
# ZZTo2L2Nu_xs      = 0.564   *gSF
# WZTo2L2Q_xs       = 3.22    *gSF
# WWTo2L2Nu_xs      = 12.178  *gSF
# WZTo3LNu_xs =   4.42965 * gSF
# ZZTo4L_xs          = 1.212 * gSF

Top_num          =  187626200.
dy_num = [2655294, 962195, 1069003, 1031103]
vv_num = [8719200, 31394787, 1965200, 2000000, 10747136]
# DY100to200_num   =  2655294.
# DY200to400_num   =  962195.
# DY400to600_num   =  1069003.
# DY600toInf_num   =  1031103.
# ZZTo2L2Nu_num    =  8719200.
# WZTo2L2Q_num     =  31394787.
# WWTo2L2Nu_num    =  1965200.
# WZTo3LNu_num = 2000000.
# ZZTo4L_num          =10747136.

h_dy = f_DY100to200.Get(var).Clone()
h_dy.Reset()
i = 0
for f_dy in f_DY:
    dy = f_dy.Get(var)
    dy.Sumw2()
    dy.Scale(dy_xs[i] * 2200. / dy_num[i])
    h_dy.Add(dy)
    i += 1
    
h_vv = f_ZZTo4L.Get(var).Clone()
h_vv.Reset()
ii = 0
for f_vv in f_VV:
    vv = f_vv.Get(var)
    vv.Sumw2()
    vv.Scale(vv_xs[ii] * 2200. / vv_num[ii])
    print vv_xs[ii] * 2200. / vv_num[ii]
    print ii
    ii += 1

h_ttbar = f_ttbar.Get(var)
h_ttbar.Sumw2()
h_ttbar.Scale(Top_xs * 2200. / Top_num)

h_bkg = h_ttbar.Clone()
h_bkg.Reset()
h_bkg.Add(h_dy)
h_bkg.Add(h_ttbar)
h_bkg.Add(h_vv)

h_bkg.Draw()

#name = var.split('/')[2]
h_bkg.SaveAs(var.split('/')[1]+'_'+var.split('/')[3]+'.root')
