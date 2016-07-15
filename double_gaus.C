#include "TF1.h"
#include "TH1.h"

void double_gaus(){
	TDirectory* dir0 = _file0->GetDirectory("anaBoosted");
	TH1F* h0 = (TH1F*)(dir0->Get("chi_mass"));
	Double_t par[9];
	TF1* g1 = new TF1("g1", "gaus",500, 1500);
	TF1* g2 = new TF1("g2", "gaus", 800, 1200);
	TF1* g3 = new TF1("g3", "gaus", 925, 1075);
	TF1* total = new TF1("total", "gaus(0)+gaus(3)+gaus(6)", 950, 1050);
	total->SetLineColor(2);
	h0->Fit(g1,"R");
	h0->Fit(g2, "R+");
	h0->Fit(g3, "R+");
	g1->GetParameters(&par[0]);
	g2->GetParameters(&par[3]);
	g3->GetParameters(&par[6]);
	total->SetParameters(par);
	h0->Fit(total, "R+");
}