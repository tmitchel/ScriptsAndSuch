#!/usr/bin/env python 
from __future__ import print_function
import ROOT, sys
import itertools

class ak4Class:
    def __init__(self, p4, CSV):
        self.p4 = p4
        self.CSV = CSV

class ak8Class:
    def __init__(self, p4, softDrop, pruned, tau3, tau2, tau1, subjetCSV):
        self.p4 = p4
        self.softDrop = softDrop
        self.pruned = pruned
        self.tau3 = tau3
        self.tau2 = tau2
        self.tau1 = tau1
        self.subjetCSV = subjetCSV

class met:
    def __init__(self, Pt, Px, Py):
        self.Pt = Pt
        self.Px = Px
        self.Py = Py
    
def read(fileName, nFile):
    tree = ROOT.TChain("Events")
    for i in range(1, nFile+1):
        tree.AddFile(fileName+'/skim_'+str(i)+'.root')

    i=0
    elCont = []
    muCont = []
    ak4Cont = []
    ak8Cont = []
    metCont = []
    bTagCont = []
    ZtagCont = []
    HtagCont = []
    evtwt = []

    for event in tree:

        i+=1
        elE = []
        muE = []
        ak4E = []
        ak8E = []
        bTagE = []
        ZtagE = []
        HtagE = []
        elPt = []
        muPt = []
        ak4Pt = []
        ak8Pt = []
        bTagPt = []
        ZtagPt= []
        HtagPt = []
        elEta = []
        muEta = []
        ak4Eta = []
        ak8Eta = []
        bTagEta = []
        ZtagEta = []
        HtagEta = []
        elPhi = []
        muPhi = []
        ak4Phi = []
        ak8Phi = []
        bTagPhi = []
        ZtagPhi = []
        HtagPhi = []
        ak4CSV = []
        ak8softDrop = []
        ak8pruned = []
        ak8tau3 = []
        ak8tau2 = []
        ak8tau1 = []
        ak8subjetCSV = []
        el = []
        mu = []
        ak4 = []
        ak8 = []
        bTag = []
        Ztag = []
        Htag = []

        metPt = event.GetLeaf("floats_metFull_metFullPt_b2gEDMNtuples.obj").GetValue(0)
        metPx = event.GetLeaf("floats_metFull_metFullPx_b2gEDMNtuples.obj").GetValue(0)
        metPy = event.GetLeaf("floats_metFull_metFullPy_b2gEDMNtuples.obj").GetValue(0)
        
        metHolder = met(metPt, metPx, metPy)

        for entry in range(0, 2):
            elE.append(event.GetLeaf("floats_electrons_elE_b2gEDMNtuples.obj").GetValue(entry) )
            muE.append(event.GetLeaf("floats_muons_muE_b2gEDMNtuples.obj").GetValue(entry) )
            ak8E.append(event.GetLeaf("floats_jetsAK8CHS_jetAK8CHSE_b2gEDMNtuples.obj").GetValue(entry) )
            elPt.append(event.GetLeaf("floats_electrons_elPt_b2gEDMNtuples.obj").GetValue(entry) )
            muPt.append(event.GetLeaf("floats_muons_muPt_b2gEDMNtuples.obj").GetValue(entry) )
            ak8Pt.append(event.GetLeaf("floats_jetsAK8CHS_jetAK8CHSPt_b2gEDMNtuples.obj").GetValue(entry) )
            elEta.append(event.GetLeaf("floats_electrons_elEta_b2gEDMNtuples.obj").GetValue(entry) )
            muEta.append(event.GetLeaf("floats_muons_muEta_b2gEDMNtuples.obj").GetValue(entry) )
            ak8Eta.append(event.GetLeaf("floats_jetsAK8CHS_jetAK8CHSEta_b2gEDMNtuples.obj").GetValue(entry) )
            elPhi.append(event.GetLeaf("floats_electrons_elPhi_b2gEDMNtuples.obj").GetValue(entry) )
            muPhi.append(event.GetLeaf("floats_muons_muPhi_b2gEDMNtuples.obj").GetValue(entry) )
            ak8Phi.append(event.GetLeaf("floats_jetsAK8CHS_jetAK8CHSPhi_b2gEDMNtuples.obj").GetValue(entry) ) 
            ak8softDrop.append(event.GetLeaf("floats_jetsAK8CHS_jetAK8CHSsoftDropMass_b2gEDMNtuples.obj").GetValue(entry) )
            ak8pruned.append(event.GetLeaf("floats_jetsAK8CHS_jetAK8CHSprunedMass_b2gEDMNtuples.obj").GetValue(entry) )
            ak8tau3.append(event.GetLeaf("floats_jetsAK8CHS_jetAK8CHStau3_b2gEDMNtuples.obj").GetValue(entry) )
            ak8tau2.append(event.GetLeaf("floats_jetsAK8CHS_jetAK8CHStau2_b2gEDMNtuples.obj").GetValue(entry) )
            ak8tau1.append(event.GetLeaf("floats_jetsAK8CHS_jetAK8CHStau1_b2gEDMNtuples.obj").GetValue(entry) )
            ak8subjetCSV.append(event.GetLeaf("floats_jetsAK8CHS_jetAK8CHSCSVv2_b2gEDMNtuples.obj").GetValue(entry) )
            

            elP4 = ROOT.TLorentzVector()
            elP4.SetPtEtaPhiE(elPt[entry], elEta[entry], elPhi[entry], elE[entry])
            muP4 = ROOT.TLorentzVector()
            muP4.SetPtEtaPhiE(muPt[entry], muEta[entry], muPhi[entry], muE[entry])
            ak8P4 = ROOT.TLorentzVector()
            ak8P4.SetPtEtaPhiE(ak8Pt[entry], ak8Eta[entry], ak8Phi[entry], ak8E[entry])
            ak8Holder = ak8Class(ak8P4, ak8softDrop[entry], ak8pruned[entry], ak8tau3[entry], ak8tau2[entry], ak8tau1[entry], ak8subjetCSV[entry])
            

            el.append(elP4)
            mu.append(muP4)
            ak8.append(ak8Holder)
            
        for entry in range(0, 5):
            ak4E.append(event.GetLeaf("floats_jetsAK4CHS_jetAK4CHSE_b2gEDMNtuples.obj").GetValue(entry) )
            ak4Pt.append(event.GetLeaf("floats_jetsAK4CHS_jetAK4CHSPt_b2gEDMNtuples.obj").GetValue(entry) )
            ak4Eta.append(event.GetLeaf("floats_jetsAK4CHS_jetAK4CHSEta_b2gEDMNtuples.obj").GetValue(entry) )
            ak4Phi.append(event.GetLeaf("floats_jetsAK4CHS_jetAK4CHSPhi_b2gEDMNtuples.obj").GetValue(entry) )
            ak4CSV.append(event.GetLeaf("floats_jetsAK4CHS_jetAK4CHSCSVv2_b2gEDMNtuples.obj").GetValue(entry) )

            ak4P4 = ROOT.TLorentzVector()
            ak4P4.SetPtEtaPhiE(ak4Pt[entry], ak4Eta[entry], ak4Phi[entry], ak4E[entry])
            ak4Holder = ak4Class(ak4P4, ak4CSV[entry])
            ak4.append(ak4Holder)

        elCont.append(el)
        muCont.append(mu)
        ak4Cont.append(ak4)
        ak8Cont.append(ak8)
        metCont.append(metHolder)
        evtwt.append(event.GetLeaf("double_ana_PreWeight_OS2LAna.obj").GetValue(entry) )
            
        size = str(tree.GetEntries())

        if i != tree.GetEntries():
            print(str(i)+'/'+size, end='\r')
        else:
            print(str(i)+'/'+size)

    print( 'All variables loaded.')
    return [elCont, muCont, ak4Cont, ak8Cont, metCont, evtwt]

def jetTags(tagType, jetColl):
    CSVv2L = 0.460
    CSVv2M = 0.800
    CSVv2T = 0.935
    jets = []

    for jet in jetColl:

        if tagType == 'b':
            if jet.p4.Pt() < 30:
                continue
            if abs(jet.p4.Eta()) > 2.4:
                continue
            if jet.CSV < CSVv2M:
                continue
            else:
                jets.append(jet)

        if tagType != 'b':
            if jet.tau2 != 0:
                jettau3Bytau2 = jet.tau3 / jet.tau2
                if jet.tau1 != 0:
                    jettau2Bytau1 = jet.tau2 / jet.tau1
            
            if tagType == 'top':
                if jet.p4.Pt() < 500:
                    continue
                if jettau3Bytau2 < 0.0 or jettau3Bytau2 > 0.46:
                    continue
                if jet.softDrop < 105 or jet.softDrop > 210:
                    continue
                if jet.subjetHighestCSV < CSVv2L:
                    continue
                else:
                    jets.append(jet)

            if tagType == 'H':
                if jet.p4.Pt() < 300:
                    continue
                if jet.jettau3Bytau2 < 0.0 or jet.jettau3Bytau2 > 1.0:
                    continue
                if jet.softDrop < 105 or jet.softDrop > 135:
                    continue
                if jet.subjetCSV < CSVv2L:
                    continue

            if tagType == 'Z':
                if jet.p4.Pt() < 300:
                    continue
                if jettau3Bytau2 < 0.0 or jettau3Bytau2 > 1.0:
                    continue
                if jet.softDrop < 70 or jet.softDrop > 110:
                    continue
                else:
                    jets.append(jet)
        
    return(jets)

def tagger(collSize, jets, tagType):
    if tagType == 'H' or tagType == 'Z':
        permer = [1, 1]
        n = 2
    elif tagType == 't':
        permer = [1, 1, 1]
        n = 3
    for i in range(0, collSize-n):
        permer.append(0)
    perm = list(itertools.permutations(permer, collSize))
    mass = 0.0
    C = []
    D = []
    toFill = []
    fullInfo = []
    jetinfo = ROOT.TLorentzVector()
    for per in perm:
        for i in per:
            if i == 1:
                jetinfo += jets[i].p4
                fullInfo.append(jets[i])
                C.append(jetinfo)
        if tagType == 'H':
            if fullInfo[0].CSV > 0.800 and fullInfo[0].p4.Pt() > 50 or fullInfo[1].CSV > 0.800 and fullInfo[1].p4.Pt() > 50:
                D.append(C[n-1])
        else:
            D.append(C[n-1])
        C = []
        jetinfo = ROOT.TLorentzVector()
    for j in range(0, len(D)):
        if tagType == 'Z':
            if D[j].Pt() > 100. and D[j].Mag() >= 70. and D[j].Mag() <= 120:
                zp4 = D[j]
                toFill.append(zp4)
        elif tagType == 'H':
            if D[j].Pt() > 100. and D[j].Mag() >= 80. and D[j].Mag() <= 160:
                hp4 = D[j]
                toFill.append(hp4)
        elif tagType == 't':
            if D[j].Pt() > 100. and D[j].Mag() >= 120. and D[j].Mag() <= 240:
                tp4 = D[j]
                toFill.append(tp4)
    return(toFill)


        
            

