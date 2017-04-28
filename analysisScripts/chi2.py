#!/usr/bin/env python
import math, itertools

def resolvedChi2(jets, Leptons, bosMass, mass, pt):
    if ((jets[2].p4 + jets[3].p4).Pt() > pt and (jets[2].p4 + jets[3].p4).M() - bosMass):
        Zup = abs((jets[2].p4 + jets[3].p4).M() - bosMass)
        Zup2 = Zup * Zup
        term1 = Zup2 / (13.835*13.835)

        BHup = abs((jets[1].p4 + jets[2].p4 + jets[3].p4).M() - mass)
        BHup2 = BHup * BHup
        term2 = BHup2 / (98.435 * 98.435)

        BLup = abs((jets[0].p4 + Leptons).M() - mass)
        BLup2 = BLup * BLup
        term3 = BLup2 / (64.68 * 64.68)

        result = term1 + term2 + term3
        return(result)

    else:
        return(9999)

def boostedChi2(ak4, ak8, Leptons, bosMass, mass, pt):
    if (ak8.p4.Pt() > pt and ak8.p4.M() != ak4[0].p4.M() and ak8.p4.M() != ak4[1].p4.M() and ak4[0].p4.DeltaR(ak8.p4) > 1.):
        BHup = abs((ak8.p4 + ak4[0].p4).M() - mass)
        BHup2 = BHup * BHup
        term1 = BHup2 / (80*80)

        BLup = abs((ak4[1].p4 + Leptons).M() - mass)
        BLup2 = BLup * BLup
        term2 = BLup2 / (59*59)

        result = term1 + term2
        
        return(result)
    else:
        return(9999)

def vector_eval(vec):
    min_value = 9999.
    mass = -1
    for ind in range(0, len(vec)):
        if (vec[ind][0] < min_value):
            min_value = vec[ind][0]
            mass = vec[ind][1]
    return([min_value, mass])

def doBoostedReco(collection, tagJet,  bosMass, Leptons, pt):
    loop = 100000
    chi2_fill = [10000, 10000]
    index_array = [0, 1, 2, 3]
    index_array1 = [0, 1, 2, 3, 4]
    perm = list(itertools.permutations(index_array1, 3))

    chi2s = []
    for mass in range(0, 3000, 10):
        loop_check = 10000
        chi2_result = [9999, -1]
        if len(collection) >= 3:
            for per in perm:
                jet = []
                for i in range(0, 3):
                    jet.append(collection[per[i]])
            
                loop = boostedChi2(jet, tagJet, Leptons, bosMass, mass, pt)
                if loop < loop_check:
                    loop_check = loop
                    chi2_result[0] = loop_check
                    chi2_result[1] = mass
            chi2s.append(chi2_result)
    chi2_fill = vector_eval(chi2s)
        
    return(chi2_fill)

def doResolvedReco(collection, bosMass, Leptons, pt):
    loop = 100000
    chi2_fill = [10000, 10000]
    index_array = [0, 1, 2, 3, 4]
    index_array1 = [0, 1, 2, 3]
    perm = list(itertools.permutations(index_array1, 4))
  
    chi2s = []
    for mass in range(0, 3000, 10):
        loop_check = 10000
        chi2_result = [9999, -1]
        if len(collection) == 4:
            for per in perm:
                jet = []
                for i in range(0, 4):
                    jet.append(collection[per[i]])

                loop = resolvedChi2(jet, Leptons, bosMass, mass, pt)
                if loop < loop_check:
                    loop_check = loop
                    chi2_result[0] = loop_check
                    chi2_result[1] = mass
            chi2s.append(chi2_result)
        if len(collection) == 5:
            for per in perm:
                jet = []
                for i in range(0, 4):
                    jet.append(collection[per[i]])
                
                loop  = resolvedChi2(jet, Leptons, bosMass, mass, pt)
                if loop < loop_check:
                    loop_check = loop
                    chi2_result[0] = loop_check
                    chi2_result[1] = mass
            chi2s.append(chi2_result)
    chi2_fill = vector_eval(chi2s)
    return(chi2_fill)
