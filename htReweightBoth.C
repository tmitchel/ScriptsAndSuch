void htReweightBoth(){
  TFile* dataFile1 = new TFile("DoubleEG-Run2015D-PromptReco.root");
  TFile* dataFile2 = new TFile("muons.root");
  TFile* bkgFile1 = new TFile("nob_ht.root");
  TFile* bkgFile2 = new TFile("nob_ht_bkg.root");
  TH1F* data1 = (TH1F*)dataFile1->Get("ana/cnt/nob_ht");
  TH1F* data2 = (TH1F*)dataFile2->Get("ana/cnt/nob_ht");
  TH1F* bkg1 = (TH1F*)bkgFile1->Get("ee__DY");
  TH1F* bkg2 = (TH1F*)bkgFile2->Get("total bkg");
  TH1F* data = (TH1F*)data1->Clone();
  data->Add(data2);
  data->Draw();
  TH1F* bkg = (TH1F*)bkg1->Clone();
  bkg->Add(bkg2);
  TH1F* ratio = (TH1F*)data->Clone();
  ratio->Divide(data, bkg);
  //ratio->SetMarkerStyle(8);
  gStyle->SetOptStat(0000);
  ratio->Draw("ep");
  // ratio->Fit("pol1");
  // ratio->SaveAs("ratio.root");
  // ratio->Print("ratio.pdf");
}
