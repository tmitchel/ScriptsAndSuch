void toPlot(){
	TFile* f0 = new TFile("BprimeFile.root");
	TFile* f1 = new TFile("DY_ht.root");
	TDirectory* dir0 = (TDirectory*)f0->Get("anaBoosted");
	TDirectory* dir1 = (TDirectory*)f1->Get("anaBoosted");
	hist0 = (TH1F*)dir0->Get("chi2_chi");
	hist1 = (TH1F*)dir1->Get("chi2_chi");
	hist0->SetLineColor(kBlue);
	hist0->SetFillColor(kBlue);
	hist0->SetTitle(":chi^{2} Comparison");
	hist0->GetXaxis()->SetTitle(":chi^{2}");
	hist0->GetYaxis()->SetTitle("# of Events");
	hist1->SetFillColor(kRed);
	hist1->SetLineColor(kRed);
	hist0->DrawNormalized("Hist");
	hist1->DrawNormalized("Hist same");
	
}