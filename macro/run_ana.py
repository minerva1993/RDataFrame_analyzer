from ROOT import *
import ROOT
import os
import argparse, psutil

from analysis_helper import *
from datasets import *
from histos import *
from cuts import *

parser = argparse.ArgumentParser(description='Options for analyzer')
parser.add_argument('--year', '-Y', action='store', type=int, default=2017, help='Set year')
options = parser.parse_args()

process = psutil.Process(os.getpid())

ROOT.ROOT.EnableImplicitMT(4)
gROOT.SetBatch()

rootDir = {2017:'/data/users/minerva1993/ntuple/V9_6/200101/production',
           2018:'/data/users/minerva1993/ntuple/V10_3/200101/production'}
outDir = '../output/' + str(options.year)

default_branch = ['channel','lepton_pt']
list_to_process = dataset(options.year)

syst1 = ['','jecup','jecdown','jerup','jerdown']
syst2 = ['TuneCP5up','TuneCP5down','hdampup','hdampdown'] #external sample

for folder_to_process in list_to_process:
  if folder_to_process != "TT_powheg_ttbb": continue
  d = load_file( get_file_list(rootDir[options.year], folder_to_process), default_branch )

  #Deal with JER/C, Hdamp, Tune systematics
  loc_str = os.path.join(rootDir[options.year], folder_to_process)
  for syst_ext in syst1 + syst2:
    if ('Run201' in loc_str) and syst_ext != '': continue
    elif (syst_ext in syst2) and not (syst_ext in loc_str): continue
    elif (syst_ext in syst1) and any(tmp in loc_str for tmp in syst2): continue
    else:
      #plotIt convention
      if (syst_ext in syst2): name = folder_to_process.replace('_' + syst_ext,'')

    if syst_ext == "": postfix = ""
    else:              postfix = "__"

    #JER/C treatment
    jec_str = ''
    if   syst_ext == 'jecup'  : jec_str = 'jet_pt * jet_JER_Nom * jet_JES_Up'
    elif syst_ext == 'jecdown': jec_str = 'jet_pt * jet_JER_Nom * jet_JES_Down'
    elif syst_ext == 'jerup'  : jec_str = 'jet_pt * jet_JER_Up'
    elif syst_ext == 'jerdown': jec_str = 'jet_pt * jet_JER_Down'
    else:                       jec_str = 'jet_pt * jet_JER_Nom'

    #Create output root file
    out = TFile.Open( os.path.join(outDir, folder_to_process) + postfix + syst_ext + '.root', 'RECREATE' )

    #Cut flow, lepton first
    lepton_dict = lepton_sel(options.year)
    for l_key, l_value in lepton_dict.items():

      #Be careful of the working point!
      cut_dict = cut_flow(b_tagging(options.year))
      #print(d)

      for c_key, c_value in cut_dict.items():
        hist_dict = histos(l_key, c_key, '')

        for h_key, h_value in hist_dict.items():
          h = d.Define('jet_pt_jerc', jec_str).Filter(l_value + c_value, c_key).Histo1D(h_value, h_key)
          h.Write()

    out.Close()

print(process.memory_info()[0]/(1024.0*1024)) #rss only
print(process.cpu_times())
