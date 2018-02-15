
#!/usr/bin/env python

from optparse import OptionParser
from pprint import pprint
import math

##########################
## set up option parser ##
##########################
parser = OptionParser()
parser.add_option('-v', '--var', action='store',
                  dest='var', default='st_bZ_boost',
                  help='name of variable to plot'
                  )
parser.add_option('-o', '--output', action='store',
                  dest='outname', default='output',
                  help='name of output file'
                  )
parser.add_option('-r', '--rebin', action='store',
                  dest='rebin', default='1', type=int,
                  help='rebin the distribution'
                  )
parser.add_option('-l', '--lepton', action='store',
                  dest='lepton', default='dimu',
                  help='lepton channel to plot'
                  )
parser.add_option('-s', '--syst', action='store_true',
                  dest='syst', default=False,
                  help='run systematics'
                  )
parser.add_option('-g', '--signal', action='store',
                  dest='signal', default='1200_bZbZ',
                  help='channel and mass point of signal'
                  )
parser.add_option('--verbose', action='store_true',
                  dest='verbose', default=False,
                  help='run in verbose mode'
                  )
parser.add_option('-p', '--printCount', action='store_true',
                  dest='printCount', default=False,
                  help='print event yields with uncertainty'
                  )
parser.add_option('-t', '--scaleTop', action='store',
                  dest='scaleTop', default=1, type=float,
                  help='amount to scale top of canvas'
                  )
(options, args) = parser.parse_args()

######################################################
## do some configuring and make some easy variables ##
######################################################
from ROOT import *
gStyle.SetOptStat(0)

var = options.var
outname = options.outname
rebin = options.rebin
lepton = options.lepton
prefix = ''
signal = options.signal
verbose = options.verbose

print var

if 'boost' in var:
    prefix = options.lepton+'_Boost'
elif 'resReco' in var:
    prefix = options.lepton+'_Res'
elif 'st_' in var:
    prefix = options.lepton+'_ST'

lepname = ''
if 'dimu' in lepton:
    lepname = '#mu^{#pm}#mu^{#mp}'
elif 'diel' in lepton:
    lepname = 'e^{#pm}e^{#mp}'
elif 'dil' in lepton:
    prefix = prefix.replace('_', '')
    if '1b' in var:
        prefix = 'b1_'+prefix
    elif '2b' in var:
        prefix = 'b2_'+prefix
    elif 'boost' in var:
        prefix = 'b12_'+prefix

title = ''
if 'Reco' in var:
    title = 'M_{#chi^{2}} [GeV]'
elif 'st_':
    title = 'S_{T} [GeV]'

def getPoissonUnc(n,weight):
    alpha = 1 - 0.6827
    if n==0: l = 0
    else: l = Math.gamma_quantile(alpha/2,n,1.)
    u = Math.gamma_quantile_c(alpha/2,n+1,1) ;
    #print 'lower quant', l, 'nominal', n, 'high quant', u
    if n > 0:
        l_err = (n-l); u_err = (u-n);
    else: l_err = l; u_err = u
    #if n < 3.0: l_err = l_err*weight; u_err = u_err*weight
    #print 'lower error', l_err, 'nominal', n, 'high error', u_err
    return (l_err*weight, u_err*weight)

#####################################################
## format TCanvas for plotting histogram with pull ##
#####################################################
def formatCanvas(can):
    gStyle.SetOptStat(0)
    # gStyle.SetNdivisions(405, "x")
    can.Draw()
    can.Divide(1, 2)

    pad1 = can.cd(1)
    pad1.cd()
    pad1.SetPad(0, .3, 1, 1)
    pad1.SetTopMargin(.1)
    pad1.SetBottomMargin(0.02)
    # pad1.SetLogy()
    pad1.SetTickx(1)
    pad1.SetTicky(1)

    pad2 = can.cd(2)
    pad2.SetPad(0, 0, 1, .3)
    pad2.SetTopMargin(0.06)
    pad2.SetBottomMargin(0.35)
    pad2.SetTickx(1)
    pad2.SetTicky(1)

    can.cd(1)

##################################################################
## filter for choosing how to fill dictionary of all histograms ##
##################################################################
def passed(name, lep, syst=None):
    if syst == None:    
        if 'BpBp' not in name and lep in name and not ('plus' in name or 'minus' in name):
            return True
    elif syst != None:
        if 'BpBp' not in name and syst in name and lep in name:
            return True
    return False

#########################################################################
## format data, THStack, and stat. unc. histograms and return as tuple ##
#########################################################################
def formatHistograms(samples):
    stack = THStack()
    data = None 
    stat = samples['nominal'][0].Clone()
    stat.Reset()
    stat.SetBinErrorOption(TH1.kPoisson)
    for ihist in samples['nominal']:
        ihist.SetBinErrorOption(TH1.kPoisson)
        if 'DATA' in ihist.GetName():
            ihist.SetLineColor(kBlack)
            ihist.SetFillColor(0)
            ihist.SetMarkerStyle(20)
            data = ihist.Clone()
            continue
        elif 'DY' in ihist.GetName():
            ihist.SetLineColor(90)
            ihist.SetFillColor(90)
        elif 'Top' in ihist.GetName():
            ihist.SetLineColor(8)
            ihist.SetFillColor(8)
        elif 'VV' in ihist.GetName():
            ihist.SetLineColor(kBlue)
            ihist.SetFillColor(kBlue)
        stack.Add(ihist)
        stat.Add(ihist)

    stat.ClearUnderflowAndOverflow()
    stat.SetMarkerStyle(0)
    stat.SetLineWidth(2)
    stat.SetFillColor(14)
    stat.SetLineColor(0)
    stat.SetFillStyle(3004)
    stat.SetFillColor(kBlack)

    return data, stack, stat

###########################################################
## read shape templates and format syst. unc. histograms ##
##  returns list of histograms for each syst along with  ##
##          a total up and total down histogram          ##
###########################################################
def formatSystematics(samples, stat):
    ## hard coded norm. systematics
    lumi_err = 0.026
    id_err   = 0.03
    trig_err = 0.01
    dy_err   = 0.15
    vv_err   = 0.15
    top_err  = 0.15

    ## make list of histogram clones for each systematic
    hists = []
    for ikey in samples.keys():
        if ikey == 'nominal' or len(samples[ikey]) == 0:
            continue
        temp_up = samples[ikey][0].Clone()
        temp_dn = samples[ikey][0].Clone()
        temp_up.Reset()
        temp_dn.Reset()
        temp_up.SetName(ikey+'__plus')
        temp_dn.SetName(ikey+'__minus')
        hists.append(temp_up)
        hists.append(temp_dn)
    
    total_dn = hists[0].Clone()
    total_dn.Reset()
    total_up = stat.Clone()

    if options.printCount:
        dy_plus   = total_up.Clone()
        dy_minus  = total_up.Clone()
        top_plus  = total_up.Clone()
        top_minus = total_up.Clone()
        vv_plus   = total_up.Clone()
        vv_minus  = total_up.Clone()

        dy_fin = samples['nominal'][2].Clone()
        top_fin = samples['nominal'][1].Clone()
        vv_fin = samples['nominal'][0].Clone()

    if verbose:
        pprint(samples)

    for ibin in range(hists[0].GetNbinsX()):
        sumUp2 = 0; sumDown2 = 0
        sumDYUp2 = 0; sumDYDown2 = 0
        sumTopUp2 = 0; sumTopDown2 = 0
        sumVVUp2 = 0; sumVVDown2 = 0
        for ihist in hists: ## loop through all systematic uncertainties
            # print ihist.GetName()
            sumUp = 0; sumDown = 0
            contentUp = 0; contentDown = 0
            dyUp = 0; dyDown = 0
            topUp = 0; topDown = 0
            vvUp = 0; vvDown = 0
            if 'minus' in ihist.GetName():
                continue
            for syst in samples[ihist.GetName().split('__')[0]]: ## loop through samples for a single systematic
                if 'pdf' in syst.GetName() or 'scale' in syst.GetName():
                    vvUp = samples['nominal'][0].GetBinContent(ibin+1)
                    vvDown = samples['nominal'][0].GetBinContent(ibin+1)

                if 'plus' in syst.GetName():
                    contentUp += syst.GetBinContent(ibin+1)
                    if 'DY' in syst.GetName():
                        dyUp = syst.GetBinContent(ibin+1)
                    if 'Top' in syst.GetName():
                        topUp = syst.GetBinContent(ibin+1)
                    if 'VV' in syst.GetName():
                        vvUp = syst.GetBinContent(ibin+1)
                elif 'minus' in syst.GetName():
                    contentDown += syst.GetBinContent(ibin+1)
                    if 'DY' in syst.GetName():
                        dyDown = syst.GetBinContent(ibin+1)
                    if 'Top' in syst.GetName():
                        topDown = syst.GetBinContent(ibin+1)
                    if 'VV' in syst.GetName():
                        vvDown = syst.GetBinContent(ibin+1)
                else:
                    print syst.GetName()

            if 'pdf' in ihist.GetName() or 'scale' in ihist.GetName():
                contentUp += samples['nominal'][0].GetBinContent(ibin+1)
                contentDown += samples['nominal'][0].GetBinContent(ibin+1)

            sumUp = max(abs(contentUp - stat.GetBinContent(ibin+1)), abs(contentDown - stat.GetBinContent(ibin+1))) ## max diff. in this bin
            sumUp2 += pow(sumUp, 2)

            if verbose:
                print 'sys: {0:5}, max up = {1:5.2f}, max dn = {2:5.2f}'.format(ihist.GetName(), sumUp, sumDown)

            if options.printCount:
                sumDYUp2    += pow(max(abs(dyUp  - samples['nominal'][2].GetBinContent(ibin+1)), abs(dyDown  - samples['nominal'][2].GetBinContent(ibin+1))), 2)
                sumTopUp2   += pow(max(abs(topUp - samples['nominal'][1].GetBinContent(ibin+1)), abs(topDown - samples['nominal'][1].GetBinContent(ibin+1))), 2)
                sumVVUp2    += pow(max(abs(vvUp  - samples['nominal'][0].GetBinContent(ibin+1)), abs(vvDown  - samples['nominal'][0].GetBinContent(ibin+1))), 2)

        if verbose:
            print 'total unc up = {0:5.2f}, total unc dn = {1:5.2f},'.format(TMath.Sqrt(sumUp2), TMath.Sqrt(sumDown2))

        iDY, statDY  = samples['nominal'][2].GetBinContent(ibin+1), samples['nominal'][2].GetBinErrorUp(ibin+1)
        iTop, statTop  = samples['nominal'][1].GetBinContent(ibin+1), samples['nominal'][1].GetBinErrorUp(ibin+1)
        iVV, statVV  = samples['nominal'][0].GetBinContent(ibin+1), samples['nominal'][0].GetBinErrorUp(ibin+1)

        ## add normalization uncertainty per bin
        norm_unc = pow(lumi_err, 2)+pow(id_err, 2)+pow(trig_err, 2)\
                   +pow(iDY*dy_err, 2)+pow(iTop*top_err, 2)+pow(iVV*vv_err, 2)\
                   +pow(statDY, 2)+pow(statTop, 2)+pow(statVV, 2)
        sumUp2 += norm_unc

        ## set content of total syst. histograms
        total_up.SetBinError(ibin+1, TMath.Sqrt(sumUp2))

        if options.printCount:
            dy_unc  = pow(lumi_err, 2)+pow(id_err, 2)+pow(trig_err, 2)+pow(iDY*dy_err, 2)+pow(statDY, 2)
            top_unc = pow(lumi_err, 2)+pow(id_err, 2)+pow(trig_err, 2)+pow(iTop*top_err, 2)+pow(statTop, 2)
            vv_unc  = pow(lumi_err, 2)+pow(id_err, 2)+pow(trig_err, 2)+pow(iVV*vv_err, 2)+pow(statVV, 2)
            sumDYUp2    += dy_unc
            sumTopUp2   += top_unc
            sumVVUp2    += vv_unc

            dy_fin.SetBinError(ibin+1, TMath.Sqrt(sumDYUp2))
            top_fin.SetBinError(ibin+1, TMath.Sqrt(sumTopUp2))
            vv_fin.SetBinError(ibin+1, TMath.Sqrt(sumVVUp2))

    if options.printCount:
        err = Double(0.)
        print 'dy count %2.2f +/- %2.2f' % (dy_fin.IntegralAndError(0, dy_fin.GetNbinsX(), err), err)
        print 'top count %2.2f +/- %2.2f' % (top_fin.IntegralAndError(0, top_fin.GetNbinsX(), err), err)
        print 'vv count %2.2f +/- %2.2f' % (vv_fin.IntegralAndError(0, vv_fin.GetNbinsX(), err), err)

        data_err = Double(0.)
        print 'data count %2.2f +/- %2.2f' % (data_hist.IntegralAndError(0, data_hist.GetNbinsX(), data_err), data_err)
        # for ibin in range(data_hist.GetNbinsX()+1):
            # data_err += pow(data_hist.GetBinErrorUp(ibin),2)

        # print 'data count %2.2f +/- %2.2f' % (data_hist.Integral(), TMath.Sqrt(data_err))

    return hists, total_up, total_dn

## input file
if 'dil' in lepton:
    fin = TFile('templates/template_'+var+'.root', 'read')
else:
    fin = TFile('templates/EMu_'+var+'.root', 'read')

## add systematics to all histogram dictionary if flagged
if options.syst:
    systematics_set = set(ikey.GetName().split('__')[2] for ikey in fin.GetListOfKeys() if 'plus' in ikey.GetName() or 'minus' in ikey.GetName())
    systematics = list(systematics_set)
    allHist = {systematic: [fin.Get(ihist.GetName()).Clone() for ihist in fin.GetListOfKeys() if passed(ihist.GetName(), lepton, systematic)] for systematic in systematics}
else:
    allHist = {}

## put nominal histograms in all histogram dictionary
allHist['nominal'] = [fin.Get(ihist.GetName()).Clone() for ihist in fin.GetListOfKeys() if passed(ihist.GetName(), lepton)]
allHist['nominal'] = sorted(allHist['nominal'], key=lambda hist: hist.Integral()) ## sort histograms based on integral

data_hist, bkg_stack, stat = formatHistograms(allHist) ## do general formatting on data, stack, stat. unc. histos
if options.syst:
    syst_plot, final_err, fullDn = formatSystematics(allHist, stat) ## do general formatting on syst. plots if flagged

## create and format the canvas
can = TCanvas('can', 'can', 800, 600)
formatCanvas(can)

## get the signal histogram
sig_hist = fin.Get(prefix+'__BpBp'+signal).Clone()
sig_hist.SetBinErrorOption(TH1.kPoisson)
if lepton == 'dil':
    sig_hist.Scale(0.044)
else:
    sig_hist.Scale(0.044*10) ## scaled for 10x cross section of 1000 GeV for now (need to generalize)

scaled_sig = sig_hist.Clone()
scaled_sig.Scale(.1)
###############################
## Print total bkg/sig error ##
###############################
full_err, sig_err = Double(0.), Double(0.)
print 'total bkg %2.2f +/- %2.2f' % (final_err.IntegralAndError(0, final_err.GetNbinsX()+1, full_err), full_err)
print 'signal %2.2f +/- %2.2f' % (scaled_sig.IntegralAndError(0, scaled_sig.GetNbinsX()+1, sig_err), sig_err)
print ''

####################################
## format the last few histograms ##
## (stack, signal and final unc.) ##
####################################    
bkg_stack.SetMaximum(bkg_stack.GetMaximum()*options.scaleTop)
bkg_stack.SetMinimum(0)
bkg_stack.Draw('hist')
if  'Reco' in var:
    bkg_stack.GetXaxis().SetRangeUser(0, 2500)
    if 'dil' in lepton:
        # pass
        bkg_stack.GetXaxis().SetRangeUser(102, 1638)
else:
    bkg_stack.GetXaxis().SetRangeUser(1000, 4000)
bkg_stack.GetXaxis().SetLabelSize(0)
bkg_stack.GetYaxis().SetTitle('Events / Bin')
bkg_stack.GetYaxis().SetTitleFont(42)
bkg_stack.GetYaxis().SetTitleSize(.05)
bkg_stack.GetYaxis().SetTitleOffset(.72)

sig_hist.SetFillColor(0)
sig_hist.SetLineWidth(2)
sig_hist.SetLineColor(kCyan)
# sig_hist.GetXaxis().SetRangeUser(1000, 3800)

final_err.SetMarkerStyle(0)
final_err.SetLineWidth(2)
final_err.SetFillColor(kRed)
final_err.SetLineColor(0)
final_err.SetFillStyle(3005)
# final_err.GetXaxis().SetRangeUser(1000, 3800)

#########################
## draw the histograms ##
#########################
final_err.Draw('same e2')
stat.Draw('same e2')
sig_hist.Draw('same hist')
data_hist.Draw('le1p0 same')

###################
## create legend ##
###################
leg = TLegend(0.5,0.42,0.88,0.88)
leg.SetTextSize(0.045)
leg.SetLineColor(0)
leg.SetFillColor(0)
leg.AddEntry(data_hist, "35.9 fb^{-1} Data", 'lep')
leg.AddEntry(allHist['nominal'][2], "Drell-Yan", "f")
leg.AddEntry(allHist['nominal'][1], 't#bar{t}', 'f')
leg.AddEntry(allHist['nominal'][0], 'Diboson', 'f')
leg.AddEntry(stat, 'Background Stat. Uncertainty', 'f')
leg.AddEntry(final_err, 'Total Uncertainty', 'f')
leg.AddEntry(sig_hist, 'Bprime Mass 1000 GeV', 'l')
leg.AddEntry('', 'Signal cross section x10', '')
leg.Draw()

can.cd(2)

###########################
## create pull histogram ##
###########################
pull = data_hist.Clone()
pull.Add(stat, -1)
for ibin in range(pull.GetNbinsX()+1):
    pullContent = pull.GetBinContent(ibin)
    uncertainty = math.sqrt(pow(final_err.GetBinErrorUp(ibin), 2)+pow(data_hist.GetBinErrorUp(ibin), 2))
    if uncertainty > 0:
        pull.SetBinContent(ibin, pullContent / uncertainty)
    else:
        pull.SetBinContent(ibin, 0)

###########################
## format pull histogram ##
###########################
pull.SetTitle('')
pull.SetMaximum(2.8)
pull.SetMinimum(-2.8)
pull.SetFillColor(kGray+1)
pull.SetLineColor(kGray+1)
pull.GetXaxis().SetTitle(title)
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

left = 1000
right = 4000
if 'dil' in options.lepton:
    rightline = right+800
else:
    rightline = right

pull.GetXaxis().SetRangeUser(left, rightline)
pull.Draw('hist')

############################
## draw +/- 2 sigma lines ##
############################ 
line1 = TLine(left, 2., rightline, 2.)
line1.SetLineWidth(1)
line1.SetLineStyle(7)
line1.SetLineColor(kBlack)
line1.Draw() 

line2 = TLine(left, -2., rightline, -2.)
line2.SetLineWidth(1)
line2.SetLineStyle(7)
line2.SetLineColor(kBlack)
line2.Draw() 

can.cd(1)

#############################
## draw graphics on canvas ##
#############################
ll = TLatex()
ll.SetNDC(kTRUE)
ll.SetTextSize(0.06)
ll.SetTextFont(42)
ll.DrawLatex(0.69,0.92, "35.9 fb^{-1} (13 TeV)");

cms = TLatex()
cms.SetNDC(kTRUE)
cms.SetTextFont(61)
cms.SetTextSize(0.08)
cms.DrawLatex(0.20, 0.80,"CMS")

sel = TLatex()
sel.SetNDC(kTRUE)
sel.SetTextSize(0.065)

chan = TLatex()
chan.SetNDC(kTRUE)
chan.SetTextSize(.1)
chan.DrawLatex(0.77, 0.78, lepname)

prel = TLatex()
prel.SetNDC(kTRUE)
prel.SetTextFont(52)
prel.SetTextSize(0.08)
prel.DrawLatex(0.29,0.80,"Preliminary")

################
## output pdf ##
################
can.SaveAs(lepton+'_'+var+'_prefit.pdf')
