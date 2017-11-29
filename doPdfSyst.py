#!/bin/env/usr python

import ROOT as r
from glob import glob
from optparse import OptionParser

parser = OptionParser()
parser.add_option('--inFile', '-i', type='string', action='store',
                  dest='inFile', default='bprime800_bZ',
                  help='name of directory to read'
                  )
parser.add_option('--outFile', '-o', type='string', action='store',
                  dest='outFile', default='output_pdf'
                  )
parser.add_option('--var', '-v', type='string', action='store',
                  dest='var', default='resReco_bH_1b',
                  help='variable to run pdf systematics on'
                  )
(options,args) = parser.parse_args()

fin = r.TFile('inputDirectory/'+options.inFile+'.root', 'READ')
ana = fin.Get('ana')
reco = fin.Get('massReco')

# print fin.GetName()

pre_pdfs, var_pdfs, pre_scales,  var_scales = [], [], [], []

## Read histograms into lists for pdf and scale and their corrections
for key in ana.GetListOfKeys():
  if 'pre_pdf' in key.GetName() and not (key.GetName() == 'pre_pdf' or key.GetName() == 'post_pdf'):
    pre_pdfs.append(key.GetName()) 
  elif 'pre_scale' in key.GetName() and not '5' in key.GetName() and not '9' in key.GetName():
    pre_scales.append(key.GetName())
for key in reco.GetListOfKeys():
  if options.var+'_pdf' in key.GetName():
    var_pdfs.append(key.GetName())
  elif options.var+'_scale' in key.GetName() and not '5' in key.GetName() and not '9' in key.GetName():
    var_scales.append(key.GetName())

# print var_pdfs[0]

tempHist = reco.Get(var_pdfs[0]).Clone()
nBins = tempHist.GetNbinsX()

pdfNom = reco.Get(var_pdfs[0]).Clone()
pdfUp = tempHist.Clone()
pdfDn = tempHist.Clone()

scaleNom = reco.Get(var_scales[0]).Clone()
scaleUp = tempHist.Clone()
scaleDn = tempHist.Clone()

## Find correction factor for pdfs using quantiles
pre_pdf_content = [ana.Get(pre_pdf).Integral() for pre_pdf in pre_pdfs]
pdfCorrUp = ana.Get(pre_pdfs[0]).Integral() / sorted(pre_pdf_content)[83]
pdfCorrDn = ana.Get(pre_pdfs[0]).Integral() / sorted(pre_pdf_content)[15]

## Find correction factor for scales using largest variations 
pre_scale_content = [ana.Get(pre_scale).GetBinContent(1) for pre_scale in pre_scales]
scaleCorrUp = ana.Get(pre_scales[0]).Integral() / max(pre_scale_content)
scaleCorrDn = ana.Get(pre_scales[0]).Integral() / min(pre_scale_content)

## Per bin, find an up and down shift
for ibin in range( nBins ):
  st_pdf_content    = [[reco.Get(var_pdf).GetBinContent(ibin), reco.Get(var_pdf).GetBinError(ibin)]    for var_pdf    in var_pdfs]
  st_scale_content  = [[reco.Get(var_scale).GetBinContent(ibin), reco.Get(var_scale).GetBinError(ibin)]  for var_scale  in var_scales]

  ## Fill new pdf histograms with up and down shifted weights
  pdfUp.SetBinContent(ibin, sorted(st_pdf_content)[83][0])
  pdfDn.SetBinContent(ibin, sorted(st_pdf_content)[15][0])
  pdfUp.SetBinError(ibin, sorted(st_pdf_content)[83][1])
  pdfDn.SetBinError(ibin, sorted(st_pdf_content)[15][1])

  ## Fill new scale histograms with max variation weights
  scaleUp.SetBinContent(ibin, max(st_scale_content)[0])
  scaleDn.SetBinContent(ibin, min(st_scale_content)[0])
  scaleUp.SetBinError(ibin, max(st_scale_content)[1])
  scaleDn.SetBinError(ibin, min(st_scale_content)[1])

## Scale signal histograms to account for acceptance only
if 'bprime' in options.inFile or 'tprime' in options.inFile:
  pdfUp.Scale(pdfCorrUp)
  pdfDn.Scale(pdfCorrDn)

  scaleUp.Scale(scaleCorrUp)
  scaleDn.Scale(scaleCorrDn)

# if pdfUp.Integral() > 0:
#   pdfUp.Scale(pdfNom.Integral() / pdfUp.Integral())
# if pdfDn.Integral() > 0:
#   pdfDn.Scale(pdfNom.Integral() / pdfDn.Integral())

# if scaleUp.Integral() > 0:
#   scaleUp.Scale(scaleNom.Integral() / scaleUp.Integral())
# if scaleDn.Integral() > 0:
#   scaleDn.Scale(scaleNom.Integral() / scaleDn.Integral())

pdfUp.SetName(options.var+'__pdf__plus')
pdfDn.SetName(options.var+'__pdf__minus')

scaleUp.SetName(options.var+'__scale__plus')
scaleDn.SetName(options.var+'__scale__minus')

fout = r.TFile('pdfscale/'+options.outFile+'_'+options.var+'_'+options.inFile+'.root', 'recreate')
fout.cd()

pdfUpOut = pdfUp.Clone()
pdfDnOut = pdfDn.Clone()

scaleUpOut = scaleUp.Clone()
scaleDnOut = scaleDn.Clone()

fout.Write()
fout.Close()

