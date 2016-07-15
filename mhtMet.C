void mhtMet(){
  
  int gSF = 1;
  int lumi = 2263;
  
  TFile* dy100_200f = new TFile("dy_ht100-200.root");
  TFile* dy200_400f = new TFile("dy_ht200-400.root");
  TFile* dy400_600f = new TFile("dy_ht400-600.root");
  TFile* dy600_Inff = new TFile("dy_ht600-Inf.root");
  TFile* ttbarf = new TFile("ttbar.root");
  TFile* WWf = new TFile("WW.root");
  TFile* WZto2f = new TFile("WZto2.root");
  TFile* WZto3f = new TFile("WZto3.root");
  TFile* ZZto2f = new TFile("ZZto2.root");
  TFile* ZZto4f = new TFile("ZZto4.root");
  TFile* muonsf = new TFile("muons.root");
  
  TH2F* dy_ht100_200 = (TH2F*)dy100_200f->Get("ana/pt_eta_c_all");
  TH2F* dy_ht200_400 = (TH2F*)dy200_400f->Get("ana/pt_eta_c_all");
  TH2F* dy_ht400_600 = (TH2F*)dy400_600f->Get("ana/pt_eta_c_all");
  TH2F* dy_ht600_Inf = (TH2F*)dy600_Inff->Get("ana/pt_eta_c_all");
  TH2F* ttbar = (TH2F*)ttbarf->Get("ana/pt_eta_c_all");
  TH2F* WW = (TH2F*)WWf->Get("ana/pt_eta_c_all");
  TH2F* WZto2 = (TH2F*)WZto2f->Get("ana/pt_eta_c_all");
  TH2F* WZto3 = (TH2F*)WZto3f->Get("ana/pt_eta_c_all");
  TH2F* ZZto2 = (TH2F*)ZZto2f->Get("ana/pt_eta_c_all");
  TH2F* ZZto4 = (TH2F*)ZZto4f->Get("ana/pt_eta_c_all");
  TH2F* muons = (TH2F*)muonsf->Get("ana/pt_eta_c_all");

  std::vector<TH2F*> histos;
  histos.push_back(dy_ht100_200);
  histos.push_back(dy_ht200_400);
  histos.push_back(dy_ht400_600);
  histos.push_back(dy_ht600_Inf);
  histos.push_back(ttbar);
  histos.push_back(WW);
  histos.push_back(WZto2);
  histos.push_back(WZto3);
  histos.push_back(ZZto2);
  histos.push_back(ZZto4);
  
  int Top_xs            = 831.76  *gSF;
  int DY100to200_xs     = 147.4   *gSF *1.23;
  int DY200to400_xs     = 40.99   *gSF *1.23;
  int DY400to600_xs     = 5.678   *gSF *1.23;
  int DY600toInf_xs     = 2.198   *gSF *1.23;
  int ZZTo2L2Nu_xs      = 0.564   *gSF;
  int WZTo2L2Q_xs       = 3.22    *gSF;
  int WWTo2L2Nu_xs      = 12.178  *gSF;
  int WZTo3LNu_xs       = 4.42965 * gSF;
  int ZZTo4L_xs         = 1.212 * gSF;
  int BpBp800_xs = 1.;

  int Top_num          =  187626200.;
  int DY100to200_num   =  2655294.;
  int DY200to400_num   =  962195.;
  int DY400to600_num   =  1069003.;
  int DY600toInf_num   =  1031103.;
  int ZZTo2L2Nu_num    =  8719200.;
  int WZTo2L2Q_num     =  31394787.;
  int WWTo2L2Nu_num    =  1965200.;
  int WZTo3LNu_num = 2000000.;
  int ZZTo4L_num          =10747136.;
  int BpBp800_num      =  831200./9.;

  std::vector<double> xs;
  xs.push_back(DY100to200_xs);
  xs.push_back(DY200to400_xs);
  xs.push_back(DY400to600_xs);
  xs.push_back(DY600toInf_xs);
  xs.push_back(Top_xs);
  xs.push_back(WWTo2L2Nu_xs);
  xs.push_back(WWTo2L2Nu_xs);
  xs.push_back(WZTo3LNu_xs);
  xs.push_back(ZZTo2L2Nu_xs);
  xs.push_back(ZZTo4L_xs);

  std::vector<double> num;
  num.push_back(DY100to200_num);
  num.push_back(DY200to400_num);
  num.push_back(DY400to600_num);
  num.push_back(DY600toInf_num);
  num.push_back(Top_num);
  num.push_back(WWTo2L2Nu_num);
  num.push_back(WWTo2L2Nu_num);
  num.push_back(WZTo3LNu_num);
  num.push_back(ZZTo2L2Nu_num);
  num.push_back(ZZTo4L_num);

  for (int i=0; i<histos.size(); i++){
    double SF;
    if (i>=0 && i<=3)
      SF = 1.23;
    else
       SF = 1.0;
    histos[i]->Scale(xs[i]*SF*lumi/num[i]);
  }

  TH2F* sum = (TH2F*)dy_ht100_200->Clone();
  for (int i=1; i<histos.size(); i++){
    //if (i != 4)
      sum->Add(histos[i]);
  }

  // TProfile* pro1 = muons->ProfileX();
  // //TProfile* pro2 = sum->ProfileX();
  // // pro1->SetMarkerColor(kBlack);
  // // pro1->SetMarkerStyle(21);
  // // pro1->SetMarkerSize(.5);
  // //pro1->Draw();
  // pro1->SetLineColor(kRed);
  // pro1->Draw("same ep");

  //gStyle->SetOptStat(0000);
  // pro1->GetXaxis()->SetRangeUser(0, 450);
  //pro1->GetYaxis()->SetRangeUser(0, 300);
  //sum->SetMarkerStyle(1);
   sum->Draw();
   sum->SaveAs("pt_eta_c_all.root");
  // gStyle->SetOptStat(0000);
  // muons->SetMarkerColor(kRed);
  // muons->SetLineColor(kRed);
  // sum->SetLineColor(kBlack);
  // muons->SetMarkerStyle(21);
  // muons->SetMarkerSize(1);
  // muons->Draw("same");
  // TLegend* leg = new TLegend(.6, .7, .9, .9);
  // leg->AddEntry(sum, "Background", "l");
  // leg->AddEntry(muons, "Data", "l");
  // leg->Draw();
  
}
