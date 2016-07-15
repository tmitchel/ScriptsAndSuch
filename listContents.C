void listContents(){
	TDirectory* dir = (TDirectory*)_file0->Get("ana");
	TH1F* cutflow = (TH1F*)ana->Get("cutflow");
	for (int i = 0; i < 12; i++){
		std::cout << cutflow->GetBinContent(i) << std::endl;
	}
}