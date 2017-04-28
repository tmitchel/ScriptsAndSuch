#!/usr/bin/env python
from __future__ import print_function 
from FWCore.ParameterSet.VarParsing import VarParsing
from readTree import *
from chi2 import *

options = VarParsing('analysis')
options.register('fileName', 'os2lanady_p4Tree.root',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 'file name to run on'
)
options.register('n', '5',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 'number of files'
)
options.register('sample', 'ttbar',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 'sample name'
)
options.parseArguments()

fout = ROOT.TFile(options.sample+'.root', 'RECREATE')
hresReco = ROOT.TH1F('resReco', 'mass reco', 200, 0., 3000.)
hboostReco = ROOT.TH1F('boostReco', 'mass reco', 200, 0., 3000.)
hmergeReco = ROOT.TH1F('mergeReco', 'mass reco', 200, 0., 3000.)
hcomboReco = ROOT.TH1F('comboReco', 'mass reco', 200, 0., 3000.)
hresST = ROOT.TH1F('resST', 'st', 200, 0., 5000.)
hboostST = ROOT.TH1F('boostST', 'st', 200, 0., 5000.)
hmergeST = ROOT.TH1F('mergeST', 'st', 200, 0., 5000.)
hcomboST = ROOT.TH1F('comboST', 'st', 200, 0., 5000.)
hdilep = ROOT.TH1F('dilep', 'dilepton mass', 40, 0., 120.)

reader = read(options.fileName, options.n)
elCont = reader[0]
muCont = reader[1]
ak4Cont = reader[2]
ak8Cont = reader[3]
met = reader[4]
evtwtCont = reader[5]
#bTag = reader[5]
#Ztag = reader[6]
#Htag = reader[7]

fout.cd()

for event in range(0, len(evtwtCont)):

    if event % 1000 == 0:
        print(str("%.0f" % (event/float(len(evtwtCont)) * 100)) +'% complete')
    
    evtwt = evtwtCont[event]
    ST = 0.0
    for mu in muCont[event]:
        ST += mu.Pt()
    for ak4 in ak4Cont[event]:
        ST += ak4.p4.Pt()
    for ak8 in ak8Cont[event]:
        ST += ak8.p4.Pt()
    ST += met[event].Pt
    
    bTag = jetTags('b', ak4Cont[event]) 

    if ak4Cont[event][0].p4.Pt() < 100:
        continue
    if ak4Cont[event][1].p4.Pt() < 50:
        continue
    if len(bTag) < 1:
        continue
    if ST < 1000:
        continue

    Ztag = jetTags('Z', ak8Cont[event])

    hdilep.Fill((muCont[event][0]+muCont[event][1]).M())
    
    resRec = [9999, -1]
    if len(ak4Cont[event]) > 3:
        resRec = doResolvedReco(ak4Cont[event], 91.2, muCont[event][0]+muCont[event][1], 150)
        hresReco.Fill(resRec[1], evtwt)
        hresST.Fill(ST, evtwt)

    boostRec = [9999, -1]
    if len(Ztag) > 0:
        boostRec = doBoostedReco(ak4Cont[event], Ztag[0], 91.2, muCont[event][0]+muCont[event][1], 150)
        hboostReco.Fill(boostRec[1], evtwt)
        hboostST.Fill(ST, evtwt)

    mergeRec = [9999, -1]
    for ak4 in ak4Cont[event]:
        if ak4.p4.M() > 70 and ak4.p4.M() < 110  and ak4.p4.Pt() > 300:
            mergeRec = doBoostedReco(ak4Cont[event], ak4, 91.2, muCont[event][0]+muCont[event][1], 150)
            hmergeReco.Fill(mergeRec[1], evtwt)
            hmergeST.Fill(ST, evtwt)
    
    if resRec[0] < boostRec[0] and resRec[0] < mergeRec[0]:
        hcomboReco.Fill(resRec[1], evtwt)
        hcomboST.Fill(ST, evtwt)
    elif boostRec[0] < resRec[0] and boostRec[0] < mergeRec[0]:
        hcomboReco.Fill(boostRec[1], evtwt)
        hcomboST.Fill(ST, evtwt)
    else:
        hcomboReco.Fill(mergeRec[1], evtwt)
        hcomboST.Fill(ST, evtwt)

fout.Write()
fout.Close()
