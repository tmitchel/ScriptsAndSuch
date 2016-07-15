#include "TF1.h"
#include "TH1.h"

void double_gaus(){
	TDirectory* dir0 = _file0->GetDirectory("ana/sig");
	TH1F* h0 = (TH1F*)(dir0->Get("ZJetMass"));
	Double_t par[6];
	TF1* g1 = new TF1("g1", "gaus", 50, 130);
	TF1* g2 = new TF1("g2", "gaus", 70, 120);
	TF1* total = new TF1("total", "gaus(0)+gaus(3)", 45, 130);
	total->SetLineColor(2);
	h0->Fit(g1,"");
	h0->Fit(g2, "");
	g1->GetParameters(&par[0]);
	g2->GetParameters(&par[3]);
	total->SetParameters(par);
	h0->Fit(total, "R");
}
