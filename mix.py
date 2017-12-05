#!/usr/bin/env python

## import all the things ##
from ROOT import *
from optparse import OptionParser

parser = OptionParser()
parser.add_option('-w', '--tW', action='store',
                  default=0, dest='tW_br', type=float,
                  help='B->tW branching ratio'
                  )
parser.add_option('-z', '--bZ', action='store',
                  default=100, dest='bZ_br', type=float,
                  help='B->bZ branching ratio'
                  )
parser.add_option('-H', '--bH', action='store',
                  default=0, dest='bH_br', type=float,
                  help='B->bH branching ratio'
                  )
parser.add_option('-f', '--fin', action='store',
                  default='EMu_bH_boost.root', dest='fin',
                  help='name of input root file'
                  )
(options, args) = parser.parse_args()

## single B branching ratios from command line options
bZ = options.bZ_br/100.
bH = options.bH_br/100.
tW = options.tW_br/100.

## find pair-production branching ratios
bZbZ = bZ*bZ
bZbH = bZ*bH + bH*bZ
bHbH = bH*bH
bHtW = bH*tW + tW*bH
tWtW = tW*tW
bZtW = bZ*tW + tW*bZ

## map channel name to branching ratio
channels = {'bZbZ': bZbZ, 'bZbH': bZbH, 'bHbH': bHbH, 'bHtW': bHtW, 'tWtW': tWtW, 'bZtW': bZtW}

nameDict = {} ## container to hold all channels for each mass point/systematic

fin = TFile('templates/'+options.fin, 'READ') ## input file

for keyName in fin.GetListOfKeys():

    name = keyName.GetName()
    temp = fin.Get(name).Clone() ## clone to add to container

    ## find which channel the histogram belongs to
    for channel in channels.keys(): 

        ## scale the histogram by the BR then add to container
        if channel in name:
            temp.Scale(channels[channel])
            newName = name.replace(channel, '')
            nameDict.setdefault(newName, [])
            nameDict[newName].append(temp)

fout = TFile('templates/'+options.fin.split('.root')[0]+'_mixed.root', 'RECREATE')  ## output file

for name in nameDict.keys():

    temp = nameDict[name][0].Clone() ## histogram to hold the sum
    temp.Reset()

    ## add the scaled channels together to make final histogram
    for hist in nameDict[name]:
        print hist.GetName(), hist.Integral()
        temp.Add(hist)

    temp.Write()

fout.Close()
    
fin.Close()
# diel_Boost__BpBp1400_bZbZ__jec__plus