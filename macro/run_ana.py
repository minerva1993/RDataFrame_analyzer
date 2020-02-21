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

#ROOT.ROOT.EnableImplicitMT(4)
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

    hists = []
    #Open dataframe and create output root file
    d = load_file( get_file_list(rootDir[options.year], folder_to_process), default_branch )
    out = TFile.Open( os.path.join(outDir, 'hist_' + folder_to_process.replace('_','')) + postfix + syst_ext + '.root', 'RECREATE' )
    print "Creating " + os.path.join(outDir, 'hist_' + folder_to_process.replace('_','')) + postfix + syst_ext + '.root'

    #Cut flow, lepton first
    d = d.Define('lep_sel', '(channel == 0 && lepton_pt > 30 && abs(lepton_eta) <= 2.4) ||\
                             (channel == 1 && lepton_pt > 30 && abs(lepton_eta) <= 2.4)').Filter('lep_sel > 0')

    #Jec/jer
    d = d.Define('jet_pt_jerc', jec_str)
    #tmp = ROOT.vector("string")()
    #tmp.push_back('jet_pt_jerc')
    #pp = d.Display(tmp)
    #pp.Print()

    d = d.Define('njet_jerc', 'Sum(jet_pt_jerc > 30 && abs(jet_eta) < 2.4)')\
         .Define('nbjet_jerc', 'Sum(jet_pt_jerc > 30 && abs(jet_eta) < 2.4 && jet_deepCSV > ' + b_tagging(options.year) + ')')

    #Run on step0 first
    lepton_dict = lepton_sel(options.year)
    for l_key, l_value in lepton_dict.items():
      hist_dict = histos(l_key, 0, syst_ext)

      for h_key, h_value in hist_dict.items():
        h = d.Filter(l_value).Histo1D(h_value, h_key)
        hists.append(h)

    #Baseline jet selection to shorten time
    d = d.Filter('njet_jerc >= 3 && nbjet_jerc >= 2')

    cut_dict = cut_flow(b_tagging(options.year))
    for c_key, c_value in cut_dict.items():

      lepton_dict = lepton_sel(options.year)
      for l_key, l_value in lepton_dict.items():
        hist_dict = histos(l_key, c_key, syst_ext)

        for h_key, h_value in hist_dict.items():
          h = d.Filter(l_value + c_value, c_key).Histo1D(h_value, h_key)
          hists.append(h)

    for hist in hists:
      hist.Write()

    out.Close()

print(process.memory_info()[0]/(1024.0*1024)) #rss only
print(process.cpu_times())
