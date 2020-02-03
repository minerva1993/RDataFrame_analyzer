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

for folder_to_process in list_to_process:
  if folder_to_process != "TT_powheg_ttbb": continue
  d = load_file( get_file_list(rootDir[options.year], folder_to_process), default_branch )
  out = TFile.Open( os.path.join(outDir, folder_to_process)+'.root', 'RECREATE' )

  cut_dict = cut_flow()
  #print(d)
  for c_key, c_value in cut_dict.items():
    if c_key != '0': continue
    d.Filter(c_value, c_key)

    hist_dict = histos(0, c_key, '')

    for h_key, h_value in hist_dict.items():
      h = d.Histo1D(h_value, h_key)
      h.Write()

  out.Close()

print(process.memory_info()[0]/(1024.0*1024)) #rss only
print(process.cpu_times())
