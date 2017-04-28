#!/usr/bin/env python
from ROOT import *

fout = TFile("cat2.root", "RECREATE")
fout.cd()

cutflow1 = TH1F("cutflow1", "cut flow", 16, 0.5, 16.5)
cutflow3 = TH1F("cutflow3", "cut flow", 15, 0.5, 15.5)
cutflow4 = TH1F("cutflow4", "cut flow", 16, 0.5, 16.5)
H_mass_b_sig = TH1F("Hmass-boosted-sig", "M(H-boosted) [GeV]", 100, 0., 400)
H_Pt_b_sig = TH1F("HPt-boosted-sig", "Pt(H-boosted) [GeV]", 100, 0., 1200)
nHcandidatejets_b_sig = TH1F("nHcandidate-boosted-sig", "N(H jets-boosted)" , 21, -0.5, 20.5)

H_mass_nb_sig = TH1F("Hmassnb-sig", "M(H) [GeV]", 100, 0., 400)
H_Pt_nb_sig = TH1F("HPtnb-sig", "Pt(H) [GeV]", 100, 0., 1200)
nHcandidatejets_nb_sig = TH1F("nHcandidatesnb-sig", "N(H jets)" , 21, -0.5, 20.5)

nHcandidatejets_sig = TH1F("nHcandidates-tot-sig", "N(H jets)" , 21, -0.5, 20.5)
nHcandidatejets1_sig = TH1F("nHcandidates1-tot-sig", "N(H jets)" , 21, -0.5, 20.5)

Z_mass_a_sig = TH1F("Zmass-boosted-sig", "M(Z-boosted) [GeV]", 100, 0., 400)
Z_Pt_a_sig = TH1F("ZPt-boosted-sig", "Pt(Z-boosted) [GeV]", 100, 0., 1200)
nzcandidatejets_a_sig = TH1F("nzcandidate-boosted-sig", "N(Z jets-boosted)" , 21, -0.5, 20.5)

Z_mass_b_sig = TH1F("Zmass-sig", "M(Z) [GeV]", 100, 0., 400)
Z_Pt_b_sig = TH1F("ZPt-sig", "Pt(Z) [GeV]", 100, 0., 1200)
nzcandidatejets_b_sig = TH1F("nzcandidates-sig", "N(Z jets)" , 21, -0.5, 20.5)

nzcandidatejets_tot_sig = TH1F("nzcandidates-tot-sig", "N(Z jets)" , 21, -0.5, 20.5)
nzcandidatejets1_tot_sig = TH1F("nzcandidates1-tot-sig", "N(Z jets)" , 21, -0.5, 20.5)
      
top_mass_a_sig = TH1F("topmas-A-sig", "M( t quark) [GeV]", 100, 0., 400)
top_Pt_a_sig = TH1F("topPt-A-sig", "Pt( t quark) [GeV]", 100, 0., 1200)
ntopcandidatejets_a_sig = TH1F("ntopcandidate-A-sig", "N(top jets)" , 21, -0.5, 20.5)

top_mass_bc_sig = TH1F("topmass-Bc-sig", "M( t quark) [GeV]", 100, 0., 400)
top_Pt_bc_sig = TH1F("topPt-BC-sig", "Pt( t quark) [GeV]", 100, 0., 1200)
ntopcandidatejets_bc_sig = TH1F("ntopcandidate-BC-sig", "N(top jets)" , 21, -0.5, 20.5)

top_mass_d_sig = TH1F("topmass-D-sig", "M( t quark) [GeV]", 100, 0., 400)
top_Pt_d_sig = TH1F("topPt-D-sig", "Pt( t quark) [GeV]", 100, 0., 1200)
ntopcandidatejets_d_sig = TH1F("ntopcandidate-D-sig", "N(top jets)" , 21, -0.5, 20.5)

W_Pt_bc_sig = TH1F("Wpt-BC-sig", "Pt( W boson) [GeV]", 100, 0., 1200.)
W_mass_bc_sig = TH1F("Wmass-BC-sig", "M( W boson) [GeV]", 100, 0., 400)
nWcandidatejets_bc_sig = TH1F("nWcandidate-BC-sig", "N(W candidate jets)" , 21, -0.5, 20.5)

lightjet_mass_bc_sig = TH1F("lightjetmass-BC-sig", "M( light jet) [GeV]", 100, 0., 400)
nlightjetcandidatejets_bc_sig = TH1F("nlightjetcandidate-sig", "N(lightjet candidate jets)" , 21, -0.5, 20.5)

ntopcandidatejets_sig = TH1F("ntopcandidate-tot-sig", "N(top jets)" , 21, -0.5, 20.5)
ntopcandidatejets1_sig = TH1F("ntopcandidate1-tot-sig", "N(top jets)" , 21, -0.5, 20.5)

st_sig = TH1F("ST_sig", "S_{T} [Gev]" , 100,0.,3000.)

st_sig1b = TH1F("ST_sig1b", "S_{T} [Gev]" , 100,0.,3000.)
st_sig2b = TH1F("ST_sig2b", "S_{T} [Gev]" , 100,0.,3000.)

st_sigT1Z1 = TH1F("ST_sigT1Z1", "S_{T} [Gev]" , 100,0.,3000.)
st_sigT0Z1 = TH1F("ST_sigT0Z1", "S_{T} [Gev]" , 100,0.,3000.)
st_sigT1Z0 = TH1F("ST_sigT1Z0", "S_{T} [Gev]" , 100,0.,3000.)
st_sigT0Z0 = TH1F("ST_sigT0Z0", "S_{T} [Gev]" , 100,0.,3000.)

st_sigT1Z1H1 = TH1F("ST_sigT1Z1H1", "S_{T} [Gev]" , 100,0.,3000.)
st_sigT1Z1H0 = TH1F("ST_sigT1Z1H0", "S_{T} [Gev]" , 100,0.,3000.)
st_sigT0Z1H1 = TH1F("ST_sigT0Z1H1", "S_{T} [Gev]" , 100,0.,3000.)
st_sigT0Z1H0 = TH1F("ST_sigT0Z1H0", "S_{T} [Gev]" , 100,0.,3000.)
st_sigT1Z0H1 = TH1F("ST_sigT1Z0H1", "S_{T} [Gev]" , 100,0.,3000.)
st_sigT1Z0H0 = TH1F("ST_sigT1Z0H0", "S_{T} [Gev]" , 100,0.,3000.)
st_sigT0Z0H1 = TH1F("ST_sigT0Z0H1", "S_{T} [Gev]" , 100,0.,3000.)
st_sigT0Z0H0 = TH1F("ST_sigT0Z0H0", "S_{T} [Gev]" , 100,0.,3000.)


st_sigT1Z1H1b1 = TH1F("ST_sigT1Z1H1b1", "S_{T} [Gev]" , 100,0.,3000.)
st_sigT1Z1H1b2 = TH1F("ST_sigT1Z1H1b2", "S_{T} [Gev]" , 100,0.,3000.)
st_sigT1Z1H0b1 = TH1F("ST_sigT1Z1H0b1", "S_{T} [Gev]" , 100,0.,3000.)
st_sigT1Z1H0b2 = TH1F("ST_sigT1Z1H0b2", "S_{T} [Gev]" , 100,0.,3000.)
  
st_sigT0Z1H1b1 = TH1F("ST_sigT0Z1H1b1", "S_{T} [Gev]" , 100,0.,3000.)
st_sigT0Z1H1b2 = TH1F("ST_sigT0Z1H1b2", "S_{T} [Gev]" , 100,0.,3000.)
st_sigT0Z1H0b1 = TH1F("ST_sigT0Z1H0b1", "S_{T} [Gev]" , 100,0.,3000.)
st_sigT0Z1H0b2 = TH1F("ST_sigT0Z1H0b2", "S_{T} [Gev]" , 100,0.,3000.)

st_sigT1Z0H1b1 = TH1F("ST_sigT1Z0H1b1", "S_{T} [Gev]" , 100,0.,3000.)
st_sigT1Z0H1b2 = TH1F("ST_sigT1Z0H1b2", "S_{T} [Gev]" , 100,0.,3000.)
st_sigT1Z0H0b1 = TH1F("ST_sigT1Z0H0b1", "S_{T} [Gev]" , 100,0.,3000.)
st_sigT1Z0H0b2 = TH1F("ST_sigT1Z0H0b2", "S_{T} [Gev]" , 100,0.,3000.)

st_sigT0Z0H1b1 = TH1F("ST_sigT0Z0H1b1", "S_{T} [Gev]" , 100,0.,3000.)
st_sigT0Z0H1b2 = TH1F("ST_sigT0Z0H1b2", "S_{T} [Gev]" , 100,0.,3000.)
st_sigT0Z0H0b1 = TH1F("ST_sigT0Z0H0b1", "S_{T} [Gev]" , 100,0.,3000.)
st_sigT0Z0H0b2 = TH1F("ST_sigT0Z0H0b2", "S_{T} [Gev]" , 100,0.,3000.)

HB  = []
ZB  = []
D   = []
W   = []
top = []
b   = []
H   = []
B   = []
BC = []

