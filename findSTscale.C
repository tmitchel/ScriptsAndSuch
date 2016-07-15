void findSTscale(){
  TFile* dataFile = new TFile("Data.root");
  TFile* stFile = new TFile("st_bkg.root");
  TH1F* data = (TH1F*)dataFile->Get("ana/sig/st");
  TH1F* st = (TH1F*)stFile->Get("total bkg");
  TH1F* divided = (TH1F*)data->Clone();
  divided->Divide(data, st);
  divided->Draw();
}
