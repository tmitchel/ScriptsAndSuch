import ROOT as root
from glob import glob
from optparse import OptionParser
parser = OptionParser()

## Add command line options
parser.add_option('--input', '-i', action='store',
                  dest='input', default='inputDirectory',
                  help='path to input'
                  )
parser.add_option('--var', '-v', action='store',
                  dest='var', default='resReco_bZ_1b',
                  help='variable to run systematics on'
                  )
parser.add_option('--lep', '-l', action='store',
                  dest='lep', default='dimu',
                  help='muons or electrons'
                  )
(options, args) = parser.parse_args()

## Create output file

var_prefix = ''
var_suffix = ''

if 'res' in options.var:
  var_prefix = options.lep+'_Res__'
elif 'boost' in options.var:
  var_prefix = options.lep+'_Boost__'

# if '1b' in options.var:
#   var_suffix = '_1b'
# elif '2b' in options.var:
#   var_suffix = '_2b'

nom_suffix = var_suffix.split('_')[0]

samples = {
  'ttbar': ['Top', 891.76],
  'dy_pt100to250': ['DY', 83.12],
  'dy_pt250to400': ['DY', 3.047],
  'dy_pt400to650': ['DY', .3921],
  'dy_pt650toInf': ['DY', .03636],
  'WW': ['VV', 118.7],
  'WZ': ['VV', 46.74],
  'ZZ': ['VV', 16.91],
  'bprime800_bZbZ': ['BpBp800_bZbZ', 1.],
  'bprime900_bZbZ': ['BpBp900_bZbZ', 1.],
  'bprime1000_bZbZ': ['BpBp1000_bZbZ', 1.],
  'bprime1100_bZbZ': ['BpBp1100_bZbZ', 1.],
  'bprime1200_bZbZ': ['BpBp1200_bZbZ', 1.],
  'bprime1300_bZbZ': ['BpBp1300_bZbZ', 1.],
  'bprime1400_bZbZ': ['BpBp1400_bZbZ', 1.],
  'bprime1500_bZbZ': ['BpBp1500_bZbZ', 1.],
  'bprime1700_bZbZ': ['BpBp1700_bZbZ', 1.],
  'bprime1800_bZbZ': ['BpBp1800_bZbZ', 1.],
  'bprime800_bZbH': ['BpBp800_bZbH', 1.],
  'bprime900_bZbH': ['BpBp900_bZbH', 1.],
  'bprime1000_bZbH': ['BpBp1000_bZbH', 1.],
  'bprime1100_bZbH': ['BpBp1100_bZbH', 1.],
  'bprime1200_bZbH': ['BpBp1200_bZbH', 1.],
  'bprime1300_bZbH': ['BpBp1300_bZbH', 1.],
  'bprime1400_bZbH': ['BpBp1400_bZbH', 1.],
  'bprime1500_bZbH': ['BpBp1500_bZbH', 1.],
  'bprime1700_bZbH': ['BpBp1700_bZbH', 1.],
  'bprime1800_bZbH': ['BpBp1800_bZbH', 1.],
  'bprime800_bHbH': ['BpBp800_bHbH', 1.],
  'bprime900_bHbH': ['BpBp900_bHbH', 1.],
  'bprime1000_bHbH': ['BpBp1000_bHbH', 1.],
  'bprime1100_bHbH': ['BpBp1100_bHbH', 1.],
  'bprime1200_bHbH': ['BpBp1200_bHbH', 1.],
  'bprime1300_bHbH': ['BpBp1300_bHbH', 1.],
  'bprime1400_bHbH': ['BpBp1400_bHbH', 1.],
  'bprime1500_bHbH': ['BpBp1500_bHbH', 1.],
  'bprime1700_bHbH': ['BpBp1700_bHbH', 1.],
  'bprime1800_bHbH': ['BpBp1800_bHbH', 1.],
}

lumi = 35900.

fin = root.TFile(options.input+'/bprime800_bZbZ.root', 'read')
directory_list = [key.GetName() for key in fin.GetListOfKeys()]
fin.Close()
file_list = [file_name for file_name in glob(options.input+'/*.root')]
pdfscale_list = [file_name for file_name in glob('pdfscale/*.root')]
btag_list = [file_name for file_name in glob('btag/*.root')]

for file_name in file_list:
  fin = root.TFile(file_name, 'read')
  sample_name = file_name.split('/')[1].split('.')[0]
  if 'bprime' in file_name:
    samples[sample_name].append(fin.Get('ana/signalEvts').GetBinContent(1))
  else:
    samples[sample_name].append(fin.Get('allEvents/hEventCount_nowt').GetBinContent(1))


fout = root.TFile('allsyst_'+options.lep+'_'+options.var+'.root', 'recreate')

for directory_name in directory_list:

  if not 'reco' in directory_name:
    continue

  if 'bc' in directory_name or 'light' in directory_name:
    continue

  syst = (directory_name.lower()).split('reco')[1]

  dy_hist = root.TH1D(var_prefix+'DY'+var_suffix+'__'+syst, 'DY', 1000, 0., 3000.)
  vv_hist = root.TH1D(var_prefix+'VV'+var_suffix+'__'+syst, 'VV', 1000, 0., 3000.)

  for file_name in file_list:
    if not '.root' in file_name:
      continue

    fin = root.TFile(file_name, 'read')
    directory = fin.Get(directory_name)
    hist = directory.Get(options.var).Clone()
    sample_name = file_name.split('/')[1].split('.')[0]


    name = samples[sample_name][0]
    xs = samples[sample_name][1]
    nevts = samples[sample_name][2]

    hist.Scale(xs * lumi / nevts)

    if not 'BpBp' in name:
      var_suffix = ''

    if 'DY' in name:
      dy_hist.Add(hist)
    elif 'VV' in name:
      vv_hist.Add(hist)
    else:
      hist.SetName(var_prefix+name+var_suffix+'__'+syst)
      if 'DYSF__minus' in directory_name:
        hist2 = hist.Clone()
        hist2.SetName(var_prefix+name+var_suffix+'__dysf__plus')
        fout.cd()
        hist2.Write()
      fout.cd()
      hist.Write()

  fout.cd()
  dy_hist.Write()
  
  fout.cd()
  vv_hist.Write() 

fout.cd()
      
dy_nom = root.TH1D(var_prefix+'DY'+nom_suffix, 'DY', 1000, 0., 3000.)
vv_nom = root.TH1D(var_prefix+'VV'+nom_suffix, 'VV', 1000, 0., 3000.)

for file_name in file_list:
  fin = root.TFile(file_name, 'read')
  directory = fin.Get('massReco')
  hist = directory.Get(options.var).Clone()
  sample_name = file_name.split('/')[1].split('.')[0]

  name = samples[sample_name][0]
  xs = samples[sample_name][1]
  nevts = samples[sample_name][2]  

  hist.Scale(xs * lumi / nevts)

  if not 'BpBp' in name:
    nom_suffix = ''

  if 'DY' in name:
    dy_nom.Add(hist)
  elif 'VV' in name:
    vv_nom.Add(hist)
  else:
    hist.SetName(var_prefix+name+nom_suffix)
    fout.cd()
    hist.Write()

fout.cd()
dy_nom.Write()
vv_nom.Write()

dy_pdfUp = root.TH1D(var_prefix+'DY'+var_suffix+'__pdf__plus', 'DY', 1000, 0., 3000.)
dy_pdfDn = root.TH1D(var_prefix+'DY'+var_suffix+'__pdf__minus', 'DY', 1000, 0., 3000.)
dy_scaleUp = root.TH1D(var_prefix+'DY'+var_suffix+'__scale__plus', 'DY', 1000, 0., 3000.)
dy_scaleDn = root.TH1D(var_prefix+'DY'+var_suffix+'__scale__minus', 'DY', 1000, 0., 3000.)

for file_name in pdfscale_list:
  if options.var not in file_name:
    continue
  fin = root.TFile(file_name, 'read')
  pdfUp = fin.Get(options.var+'__pdf__plus').Clone()
  pdfDn = fin.Get(options.var+'__pdf__minus').Clone()

  scaleUp = fin.Get(options.var+'__scale__plus').Clone()
  scaleDn = fin.Get(options.var+'__scale__minus').Clone()

  sample_name = file_name.split('/')[1].split('.')[0].split('pdfscale_')[1].split(options.var+'_')[1]
  name = samples[sample_name][0]
  xs = samples[sample_name][1]
  nevts = samples[sample_name][2]

  pdfUp.Scale(xs * lumi / nevts)
  pdfDn.Scale(xs * lumi / nevts)
  scaleUp.Scale(xs * lumi / nevts)
  scaleDn.Scale(xs * lumi / nevts)

  if not 'BpBp' in name:
    var_suffix = ''

  if 'DY' in name:
    dy_pdfUp.Add(pdfUp)
    dy_pdfDn.Add(pdfDn)
    dy_scaleUp.Add(scaleUp)
    dy_scaleDn.Add(scaleDn)
  else:
    pdfUp.SetName(var_prefix+name+var_suffix+'__pdf__plus')
    pdfDn.SetName(var_prefix+name+var_suffix+'__pdf__minus')
    scaleUp.SetName(var_prefix+name+var_suffix+'__scale__plus')
    scaleDn.SetName(var_prefix+name+var_suffix+'__scale__minus')
    fout.cd()
    pdfUp.Write()
    pdfDn.Write()
    scaleUp.Write()
    scaleDn.Write()

fout.cd()

dy_btagUp = root.TH1D(var_prefix+'DY'+var_suffix+'__BTag__plus', 'DY', 1000, 0., 3000.)
dy_btagDn = root.TH1D(var_prefix+'DY'+var_suffix+'__BTag__minus', 'DY', 1000, 0., 3000.)
vv_btagUp = root.TH1D(var_prefix+'VV'+var_suffix+'__BTag__plus', 'VV', 1000, 0., 3000.)
vv_btagDn = root.TH1D(var_prefix+'VV'+var_suffix+'__BTag__minus', 'VV', 1000, 0., 3000.)

for file_name in btag_list:
  if options.var not in file_name:
    continue
  fin = root.TFile(file_name, 'read')
  btagUp = fin.Get(options.var+'__BTagSF__plus').Clone()
  btagDn = fin.Get(options.var+'__BTagSF__minus').Clone()

  sample_name = file_name.split('/')[1].split('.')[0].split('_BTagSF')[0].split('_'+options.var)[0]
  name = samples[sample_name][0]
  xs = samples[sample_name][1]
  nevts = samples[sample_name][2]

  btagUp.Scale(xs * lumi / nevts)
  btagDn.Scale(xs * lumi / nevts)

  if not 'BpBp' in name:
    var_suffix = ''

  if 'DY' in name:
    dy_btagUp.Add(btagUp)
    dy_btagDn.Add(btagDn)
  elif 'VV' in name:
    vv_btagUp.Add(btagUp)
    vv_btagDn.Add(btagDn)
  else:
    btagUp.SetName(var_prefix+name+var_suffix+'__BTag__plus')
    btagDn.SetName(var_prefix+name+var_suffix+'__BTag__minus')
    fout.cd()
    btagUp.Write()
    btagDn.Write()



fout.cd()
dy_pdfUp.Write()
dy_pdfDn.Write()
dy_scaleUp.Write()
dy_scaleDn.Write()
dy_btagUp.Write()
dy_btagDn.Write()
vv_btagUp.Write()
vv_btagDn.Write()

dy_dyhist2 = fout.Get(var_prefix+'DY__dysf__minus').Clone()
dy_dyhist2.SetName(var_prefix+'DY__dysf__plus')
dy_dyhist2.Write()

vv_dyhist2 = fout.Get(var_prefix+'VV__dysf__minus').Clone()
vv_dyhist2.SetName(var_prefix+'VV__dysf__plus')
vv_dyhist2.Write()

fout.Close()





