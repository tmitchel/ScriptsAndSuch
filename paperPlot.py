import ROOT
from optparse import OptionParser
from glob import glob
from math import sqrt
from array import array

##########################
## Set up option parser ##
##########################

parser = OptionParser()
parser.add_option('--inDir', '-d', action='store',
                  dest='inDir', default='ana/pre',
                  help='TDirectory where histogram is stored'
                  )
parser.add_option('--var', '-v', action='store',
                  dest='var', default='st_pre',
                  help='variable to plot'
                  )
parser.add_option('--outName', '-o', action='store',
                  dest='outName', default='output',
                  help='name of output file'
                  )
parser.add_option('--signals', '-s', action='store',
                  dest='signals', default='',
                  help='list of signal samples to plot (separated by commas)'
                  )
parser.add_option('--rebin', '-r', action='store',
                  dest='rebin', default=1,
                  help='amount to rebin'
                  )
parser.add_option('--drawData', '-D', action='store_true',
                  dest='drawData', default=False,
                  help='Draw data only unless signal region plot'
                  )
parser.add_option('--title', '-t', action='store',
                  dest='title', default="S_{T} [GeV]",
                  help='title of plot'
                  )
parser.add_option('--input' , '-I', action='store',
                  dest='input', default='Zmumu/',
                  help='path to input files'
                  )

(options, args) = parser.parse_args()

#############################################################
## Prepare some variables and things for convenience later ##
#############################################################

inDir = options.inDir
var = options.var
outName = options.outName
rebin = int(options.rebin)
drawData = options.drawData
signals = [signal for signal in (options.signals).split(',')]

files = [ifile for ifile in glob(options.input+'*.root')]
ROOT.gStyle.SetOptStat(0)

lumi = 35900.
samples = {
  'ttbar': ['Top', 891.76],
  'dy_pt100to250': ['DY', 83.12],
  'dy_pt250to400': ['DY', 3.047],
  'dy_pt400to650': ['DY', .3921],
  'dy_pt650toInf': ['DY', .03636],
  'WW': ['VV', 118.7],
  'WZ': ['VV', 46.74],
  'ZZ': ['VV', 16.91],
  'bprime800_bZbZ': ['BpBp800_bZbZ', 0.196],
  'bprime900_bZbZ': ['BpBp900_bZbZ', 1.],
  'bprime1000_bZbZ': ['BpBp1000_bZbZ', 0.044],
  'bprime1100_bZbZ': ['BpBp1100_bZbZ', 1.],
  'bprime1200_bZbZ': ['BpBp1200_bZbZ', 0.0118],
  'bprime1300_bZbZ': ['BpBp1300_bZbZ', 1.],
  'bprime1400_bZbZ': ['BpBp1400_bZbZ', 1.],
  'bprime1500_bZbZ': ['BpBp1500_bZbZ', 1.],
  'bprime1700_bZbZ': ['BpBp1700_bZbZ', 1.],
  'bprime1800_bZbZ': ['BpBp1800_bZbZ', 1.],
  'bprime800_bZbH': ['BpBp800_bZbH', 0.196],
  'bprime900_bZbH': ['BpBp900_bZbH', 1.],
  'bprime1000_bZbH': ['BpBp1000_bZbH', 0.044],
  'bprime1100_bZbH': ['BpBp1100_bZbH', 1.],
  'bprime1200_bZbH': ['BpBp1200_bZbH', 0.0118],
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

#################################
## Define functions to be used ##
##################################

## function to return True if key(hist) is for a signal histogram
def signal(hist):
  if 'DY' in hist or 'Top' in hist or 'VV' in hist or 'Data' in hist:
    return False
  else:
    return True

## define function to get number of generated events
def getNevts(fin, name):
  if 'BpBp' in name or 'TpTp' in name:
    return fin.Get('ana/signalEvts').GetBinContent(1)
  else:
    return fin.Get('allEvents/hEventCount_nowt').GetBinContent(1)

## function to do all formatting for histograms
def formatHistograms(templates):
  seenSignal = 0

  templates['DY'].SetLineColor(90)
  templates['DY'].SetFillColor(90)

  templates['VV'].SetLineColor(ROOT.kBlue)
  templates['VV'].SetFillColor(ROOT.kBlue)

  templates['Top'].SetLineColor(8)
  templates['Top'].SetFillColor(8)

  if not drawData:
    templates['Data'].Scale(0)
  templates['Data'].SetLineColor(ROOT.kBlack)
  templates['Data'].SetFillColor(0)
  templates['Data'].SetBinErrorOption(ROOT.TH1.kPoisson)
  templates['Data'].SetMarkerStyle(20)

  for hist in templates.keys():
    if not signal(hist):
      continue
    templates[hist].SetLineColor(ROOT.kRed+2*seenSignal)
    templates[hist].SetLineWidth(2)
    seenSignal += 1

###########################################################################
## get histograms from file, do scaling, add to dictionary to keep track ##
###########################################################################

fout = ROOT.TFile(outName+'.root', 'recreate')

## get formatted histgrams
tempIn = ROOT.TFile(options.input+'ttbar.root', 'read')
fout.cd()
tt_hist = tempIn.Get(inDir+'/'+var).Clone().Rebin(rebin)
dy_hist = tt_hist.Clone()
vv_hist = tt_hist.Clone()
tempIn.Close()

tt_hist.Reset()
dy_hist.Reset()
vv_hist.Reset()

templates = {}  ## dictionary to hold histograms

for ifile in files:
  sample_name = ifile.split('/')[-1].split('.')[0]

  ## skip old outputs
  if sample_name not in samples.keys():
    continue

  fin = ROOT.TFile(ifile)
  name = samples[sample_name][0]
  xs = samples[sample_name][1]
  nevts = getNevts(fin, name)
  fout.cd()

  hist = fin.Get(inDir+'/'+var).Clone()
  hist.Scale(xs * lumi / nevts)
  hist.Rebin(rebin)
  hist.GetXaxis().SetTitle('')
  hist.GetXaxis().SetRangeUser(0,2000)
  hist.GetYaxis().SetLabelColor(0)
  hist.GetYaxis().SetLabelOffset(1)

  if 'DY' in name:
    # print name, xs, nevts, xs*lumi/nevts, hist.Integral(), dy_hist.Integral()
    dy_hist.Add(hist)
  elif 'VV' in name:
    vv_hist.Add(hist)
  elif 'Top' in name:
    tt_hist.Add(hist)
  elif sample_name in signals:
    templates[name] = hist

dataIn = ROOT.TFile(options.input+'data.root', 'read')
fout.cd()
templates['Data'] = dataIn.Get(inDir+'/'+var).Clone().Rebin(rebin)
dataIn.Close()

fout.cd()
templates['Top'] = tt_hist
templates['VV'] = vv_hist
templates['DY'] = dy_hist

###############################
## Get uncertainties to plot ##
###############################

total_bkg = templates['Top'].Clone()
total_bkg.Add(templates['VV'])
total_bkg.Add(templates['DY'])
total_bkg.SetBinErrorOption(ROOT.TH1.kPoisson)
total_bkg.ClearUnderflowAndOverflow()

total_bkg.SetMarkerSize(0)
total_bkg.SetLineWidth(2)
total_bkg.SetFillColor(14)
total_bkg.SetLineColor(0)
total_bkg.SetFillStyle(3004)

#######################################
## Print out event yields for tables ##
#######################################
integralError = ROOT.Double(1000.)

for hist in templates.keys():
  templates[hist].IntegralAndError(0,3000,integralError)
  print hist, 'integral', templates[hist].Integral(), 'error', integralError

total_bkg.IntegralAndError(0,3000,integralError)
print 'total bkg', 'integral', total_bkg.Integral(), 'error', integralError

#################################
## Start formatting Canvas/Pads ##
#################################

can = ROOT.TCanvas("can", "can", 800, 600)
ROOT.gStyle.SetOptStat(0)
can.Draw()
can.Divide(1, 2)

pad1 = can.cd(1)
pad1.cd()
pad1.SetPad(0, .3, 1, 1)
pad1.SetTopMargin(.1)
pad1.SetBottomMargin(0.005)
# pad1.SetLogy()
pad1.SetTickx(1)
pad1.SetTicky(1)

pad2 = can.cd(2)
pad2.SetPad(0, 0, 1, .3)
pad2.SetTopMargin(0.005)
pad2.SetBottomMargin(0.3)
pad2.SetTickx(1)
pad2.SetTicky(1)

can.cd(1)

#####################################
## Format histograms and the stack ##
#####################################

formatHistograms(templates)

stack = ROOT.THStack("","")
stack.Add(templates['VV'])
stack.Add(templates['Top'])
stack.Add(templates['DY'])
stack.Draw('hist')
stack.GetXaxis().SetRange(0,2000)
stack.GetYaxis().SetTitle('Events / Bin')
stack.GetYaxis().SetTitleFont(42)
stack.GetYaxis().SetTitleSize(.05)
stack.GetYaxis().SetTitleOffset(1)
stack.GetYaxis().SetLabelFont(42)
stack.GetYaxis().SetLabelSize(.07)
pad1.Modified()

#######################
## Draw LateX things ##
#######################

cms = ROOT.TLatex()
cms.SetNDC(ROOT.kTRUE)
# cms.SetTextFont(61)
cms.SetTextSize(0.08)
cms.SetLineWidth(2)
cms.DrawLatex(0.15, .8,"CMS")

ll = ROOT.TLatex()
ll.SetNDC(ROOT.kTRUE)
ll.SetTextSize(0.06)
ll.SetTextFont(42)
ll.SetLineWidth(2)
ll.DrawLatex(0.685,0.92, "35.9 fb^{-1} (13 TeV)")

# prel = ROOT.TLatex()
# prel.SetNDC(ROOT.kTRUE)
# prel.SetTextFont(52)
# prel.SetTextSize(0.08)
# prel.DrawLatex(0.235,0.80,"Preliminary")

#######################
## Format the legend ##
#######################

leg = ROOT.TLegend(0.5,0.55,0.88,0.88)
leg.SetTextSize(0.045)
leg.SetLineColor(0)
leg.SetFillColor(0)
leg.SetHeader('B prime Mass Reconstruction')
leg.AddEntry(templates['DY'], "Drell-Yan", "f")
leg.AddEntry(templates['Top'], 't#bar{t}', 'f')
leg.AddEntry(templates['VV'], 'Diboson', 'f')
leg.AddEntry(total_bkg, 'Background Stat. Uncertainty', 'f')
for hist in templates.keys():
  if 'BpBp' in hist:
    histName = 'Bprime Mass '+(hist.split('BpBp')[1].split('_')[0])+ ' GeV'
    leg.AddEntry(templates[hist], histName, 'l')
  elif 'TpTp' in hist:
    histName = 'Tprime Mass '+(hist.split('TpTp')[1].split('_')[0])+ ' GeV'
    leg.AddEntry(templates[hist], histName, 'l')
leg.AddEntry('', 'Signal cross section = 1 pb', '')
leg.Draw('same')

####################################################################
## Make sure there is enough room at the top for the legend/"CMS" ##
####################################################################

bkg_max = total_bkg.GetMaximum()
new_max = total_bkg.GetMaximum()

for hist in templates.keys():
  if signal(hist):
    if templates[hist].GetMaximum() > bkg_max:
      new_max = templates[hist].GetMaximum()

    templates[hist].Draw('same hist')

templates['Data'].GetXaxis().SetRange(0,2000)
templates['Data'].Draw('same ep0')
total_bkg.GetXaxis().SetRange(0,2000)
total_bkg.Draw('same e2')

stack.SetMaximum(new_max+.2*new_max)
stack.SetMinimum(0.1)
pad1.Modified()

can.cd(2)

#############################################
## Set up the pull plot in the bottom pane ##
#############################################

pull = templates['Data'].Clone()
pull.Add(total_bkg, -1)
for ibin in range(pull.GetNbinsX()+1):
  pullContent = pull.GetBinContent(ibin)
  if not drawData:
    pullContent = 0
  dataUnc = templates['Data'].GetBinErrorUp(ibin)
  if dataUnc > 0:
    pull.SetBinContent(ibin, pullContent / dataUnc)
  else:
    pull.SetBinContent(ibin, 0)

pull.SetTitle('')
pull.SetMaximum(2.8)
pull.SetMinimum(-2.8)
pull.SetFillColor(ROOT.kBlack)
pull.GetXaxis().SetTitle(options.title)
pull.GetXaxis().SetTitleSize(0.15)
pull.GetXaxis().SetTitleOffset(0.8)
pull.GetXaxis().SetLabelFont(42)
pull.GetXaxis().SetLabelSize(.1)

pull.GetYaxis().SetTitle('#frac{Data - Bkg.}{Total unc.}')
pull.GetYaxis().SetTitleSize(0.12)
pull.GetYaxis().SetTitleFont(42)
pull.GetYaxis().SetTitleOffset(.32)
pull.GetYaxis().SetLabelSize(.17)
pull.GetYaxis().SetNdivisions(505)
pull.Draw('hist')

line1 = ROOT.TLine(pull.GetBinLowEdge(1), 2., pull.GetBinLowEdge(pull.GetNbinsX()+1), 2.)
line1.SetLineWidth(1)
line1.SetLineStyle(7)
line1.SetLineColor(ROOT.kBlack)
line1.Draw() 

line2 = ROOT.TLine(pull.GetBinLowEdge(1), -2., pull.GetBinLowEdge(pull.GetNbinsX()+1), -2.)
line2.SetLineWidth(1)
line2.SetLineStyle(7)
line2.SetLineColor(ROOT.kBlack)
line2.Draw() 

#####################################
## Save the files and call it good ##
#####################################

can.SaveAs(outName+'.pdf')
can.SaveAs(outName+'.png')

print 'done'
fout.Write()
fout.Close()


