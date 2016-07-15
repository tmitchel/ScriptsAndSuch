void findZscale(){
  TFile* file1 = new TFile("DoubleEG_prompt.root");
  TFile* file2 = new TFile("nob_pt_zelel_cnt_bkg.root");
  TH1F* hist1 = (TH1F*)file1->Get("ana/nob_pt_zelel_cnt");
  TH1F* hist2 = (TH1F*)file2->Get("total bkg");
  TH1F* divided = (TH1F*)hist1->Clone();
  divided->Divide(hist1, hist2);
  gStyle->SetOptStat(0000);
  divided->GetYaxis()->SetTitle("Data/MC");
  divided->Draw("ep");
  divided->SaveAs("ElectronFit.root");
}
