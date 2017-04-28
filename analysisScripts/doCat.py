#!/usr/bin/env python
from FWCore.ParameterSet.VarParsing import VarParsing
from readTree import *
from declareCat import *
from ROOT import *
options = VarParsing('analysis')
options.register('fileName', 'os2lana_skim.root',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 'file name to run on'
)
options.parseArguments()

reader = read(options.fileName)
elCont = reader[0]
muCont = reader[1]
ak4Cont = reader[2]
ak8Cont = reader[3]
met = reader[4]

#fout = ROOT.TFile.Open('cat.root')
#fout.cd()

for event in range(0, len(elCont)):
    evtwt = 1.0
    ST = 0.0
    for mu in muCont[event]:
        ST += mu.Pt()
    for ak4 in ak4Cont[event]:
        ST += ak4.p4.Pt()
    for ak8 in ak8Cont[event]:
        ST += ak8.p4.Pt()
    ST += met[event].Pt

    b = jetTags('b', ak4Cont[event])

    if ak4Cont[event][0].p4.Pt() < 100:
        continue
    if ak4Cont[event][1].p4.Pt() < 50:
        continue
    if len(b) < 1:
        continue
    if ST < 1000:
        continue

    for jet in ak4Cont[event]:
        if jet.p4.M() >= 80 and jet.p4.M() <= 160 and jet.p4.Pt() > 450 and jet.CSV > 0.800:
            h = TLorentzVector()
            h = jet.p4
            HB.append(h)
        if jet.p4.M() >= 70 and jet.p4.M() <= 120 and jet.p4.Pt() > 300:
            zb = TLorentzVector()
            zb = jet.p4
            ZB.append(zb)
        if jet.p4.M() >= 140 and jet.p4.M() <= 200 and jet.p4.Pt() > 600:
            d = TLorentzVector()
            d = jet.p4
            D.append(d)
        if jet.p4.Pt() > 100. and jet.p4.Mag() >= 60. and jet.p4.Mag() <=140:
            W.append(jet)
        else:
            B.append(jet)

    H = tagger(len(ak4Cont[event]), ak4Cont[event], 'H')
    Z = tagger(len(ak4Cont[event]), ak4Cont[event], 'Z')
    top = tagger(len(ak4Cont[event]), ak4Cont[event], 't')

    for wcan in range(0, len(W)):
        for bcan in range(0, len(B)):
            bc1 = TLorentzVector()
            bc1 = W[wcan].p4 + B[bcan].p4
            if bc1.Mag() >= 120 and bc1.Mag() <= 240 and bc1.Pt() >= 150:
                BC.append(bc1)

    # for HBcan in HB:
    #     H_mass_b_sig.Fill(HBcan.M(), evtwt)
    #     H_Pt_b_sig.Fill(HBcan.Pt(), evtwt)
    # nHcandidatejets_b_sig.Fill(len(HB), evtwt)

    # for Hcan in H:
    #     H_mass_nb_sig.Fill(Hcan.M(), evtwt)
    #     H_Pt_nb_sig.Fill(Hcan.Pt(), evtwt)
    # nHcandidatejets_nb_sig.Fill(len(H), evtwt)

    nHcandidates = 0.0
    nHcandidates1 = 0.0
    if len(HB) > 0 or len(H) > 0:
        nHcandidates = len(HB) + len(H)
    #     nHcandidatejets_sig.Fill(nHcandidates, evtwt)
    nHcandidates1 = len(HB) + len(H)
    # nHcandidatejets1_sig.Fill(nHcandidates1, evtwt)

    # for ZBcan in range(0, len(ZB)):
    #     Z_mass_b_sig.Fill(ZB[ZBcan].M(), evtwt)
    #     Z_Pt_b_sig.Fill(ZB[ZBcan].Pt(), evtwt)
    # nzcandidatejets_b_sig.Fill(len(Z), evtwt)

    nzcandidates = 0.0
    nzcandidates1 = 0.0
    if len(ZB) > 0 or len(Z) > 0:
        nzcandidates = len(ZB) + len(Z)
    #     nzcandidatejets_tot_sig.Fill(nzcandidates, evtwt)
    nzcandidates1 = len(ZB) + len(Z)
    # nzcandidatejets1_tot_sig.Fill(nzcandidates1, evtwt)

    # for Dcan in D:
    #     top_mass_d_sig.Fill(Dcan.M(), evtwt)
    #     top_Pt_d_sig.Fill(Dcan.Pt(), evtwt)
    # ntopcandidatejets_d_sig.Fill(len(D), evtwt)

    # for Wcan in range(0, len(W)):
    #     W_mass_bc_sig.Fill(W[Wcan].p4.M(), evtwt)
    #     W_Pt_bc_sig.Fill(W[Wcan].p4.Pt(), evtwt)
    # nWcandidatejets_bc_sig.Fill(len(W), evtwt)

    # for Bcan in range(0, len(b)):
    #     lightjet_mass_bc_sig.Fill(b[Bcan].p4.M(), evtwt)
    # nlightjetcandidatejets_bc_sig.Fill(len(b), evtwt)

    # for BCcan in range(0, len(BC)):
    #     top_mass_bc_sig.Fill(BC[BCcan].M(), evtwt)
    #     top_Pt_bc_sig.Fill(BC[BCcan].Pt(), evtwt)
    # ntopcandidatejets_bc_sig.Fill(len(top), evtwt)

    # for topcan in range(0, len(top)):
    #     top_mass_a_sig.Fill(top[topcan].M(), evtwt)
    #     top_Pt_a_sig.Fill(top[topcan].Pt(), evtwt)
    # ntopcandidatejets_a_sig.Fill(len(top), evtwt)

    ntopcandidates = 0.0
    ntopcandidates1 = 0.0
    if len(b) == 1:
        cutflow3.Fill(2, evtwt)
        st_sig1b.Fill(ST, evtwt)

    if len(b) > 1:
        cutflow1.Fill(3, evtwt)
        st_sig2b.Fill(ST, evtwt)

    if ntopcandidates > 0 and nzcandidates > 0:
        st_sigT1Z1.Fill(ST, evtwt)
        cutflow3.Fill(4, evtwt)
        if nHcandidates > 0:
            st_sigT1Z1H1.Fill(ST, evtwt)
            cutflow3.Fill(4, evtwt)
            if len(b) == 1:
                cutflow4.Fill(1, evtwt)
                st_sigT1Z1H1bz.Fill(ST, evtwt)
            elif len(b) > 1:
                cutflow4.Fill(2, evtwt)
                st_sigT1Z1H1b2.Fill(ST, evtwt)
        elif nHcandidates == 0:
            st_sigT1Z1H0.Fill(ST, evtwt)
            cutflow3.Fill(9, evtwt)
            if len(b) == 1:
                cutflow4.Fill(3, evtwt)
                st_sigT1Z1H0b1.Fill(ST, evtwt)
            elif len(b) > 1:
                cutflow.Fill(4, evtwt)
                st_sigT1Z1H0b2.Fill(ST, evtwt)

    if ntopcandidates == 0 and nzcandidates > 0:
        st_sigT0Z1.Fill(ST, evtwt)
        cutflow3.Fill(5, evtwt)
        if nHcandidates > 0:
            st_sigT1Z1H1.Fill(ST, evtwt)
            cutflow3.Fill(10, evtwt)
            if len(b) == 1:
                cutflow4.Fill(5, evtwt)
                st_sigT1Z1H1b1.Fill(ST, evtwt)
            elif len(b) > 1:
                cutflow4.Fill(6, evtwt)
                st_sigT1Z1H1b2.Fill(ST, evtwt)
        elif nHcandidates == 0:
            st_sigT1Z1H0.Fill(ST, evtwt)
            cutflow3.Fill(11, evtwt)
            if len(b) == 1:
                cutflow4.Fill(7, evtwt)
                st_sigT1Z1H0b1.Fill(ST, evtwt)
            elif len(b) > 1:
                cutflow4.Fill(8, evtwt)
                st_sigT1Z1H0b2.Fill(ST, evtwt)

    if ntopcandidates > 0 and nzcandidates==0:
        st_sigT1Z0.Fill(ST,evtwt)
        cutflow3.Fill(6, evtwt)
        if nHcandidates > 0:
            st_sigT1Z1H1.Fill(ST,evtwt)
            cutflow3.Fill(12, evtwt) 
            if len(b) == 1:
                cutflow4.Fill(9, evtwt)
                st_sigT1Z1H1b1.Fill(ST, evtwt)
            elif len(b) > 1:
                cutflow4.Fill(10, evtwt) 
                st_sigT1Z1H1b2.Fill(ST, evtwt) 
        elif nHcandidates == 0:
            st_sigT1Z1H0.Fill(ST,evtwt)
            cutflow3.Fill(13, evtwt)
            if len(b) == 1:
                cutflow4.Fill(11, evtwt)
                st_sigT1Z1H0b1.Fill(ST, evtwt)
            elif len(b) > 1:
                cutflow.Fill(12, evtwt)
                st_sigT1Z1H0b2.Fill(ST, evtwt)
                             
    if ntopcandidates == 0 and nzcandidates == 0:
        st_sigT0Z0.Fill(ST,evtwt)
        cutflow3.Fill(7, evtwt)
        if nHcandidates > 0:
            st_sigT1Z1H1.Fill(ST,evtwt)
            cutflow3.Fill(14, evtwt)
            if len(b) == 1:
                cutflow4.Fill(13, evtwt)
                st_sigT1Z1H1b1.Fill(ST, evtwt)
            elif len(b) > 1:
                cutflow4.Fill(14, evtwt)
                st_sigT1Z1H1b2.Fill(ST, evtwt)
        elif nHcandidates == 0:
            st_sigT1Z1H0.Fill(ST,evtwt)
            cutflow3.Fill(15, evtwt)
            if len(b) == 1:
                cutflow4.Fill(15, evtwt)
                st_sigT1Z1H0b1.Fill(ST, evtwt)
            elif len(b) > 1:
                cutflow4.Fill(16, evtwt)
                st_sigT1Z1H0b2.Fill(ST, evtwt)
  
  
fout.Write()
fout.Close()                


    
