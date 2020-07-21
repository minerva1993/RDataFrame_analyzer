from ROOT import *
import ROOT
import os, sys, multiprocessing
import argparse, psutil

from analysis_helper import *
from datasets import *
from histos import *
from cuts import *
from systematic import *

parser = argparse.ArgumentParser(description='Options for analyzer')
parser.add_argument('--year', '-Y', action='store', type=int, default=2017, help='Set year')
options = parser.parse_args()

process = psutil.Process(os.getpid())

gROOT.SetBatch()

year = options.year
rootDir = {2017:'/data/users/minerva1993/ntuple/V9_6/200101/production',
           2018:'/data/users/minerva1993/ntuple/V10_3/200101/production'}
outDir = '../output/' + str(year)

default_branch = ['channel','lepton_pt']
list_to_process = dataset(year)

syst1 = ['','jecup','jecdown','jerup','jerdown']
syst2 = ['TuneCP5up','TuneCP5down','hdampup','hdampdown'] #external sample

#Create list of tuple (folder_to_process, syst_ext)
list_args = []
for f_tmp in list_to_process:
  if f_tmp != "TT_powheg_ttbb": continue
  for s_tmp in syst1 + syst2:
    if s_tmp != "": continue
    list_args.append((f_tmp, s_tmp))

def run_ana(tuple_args):
  folder_to_process = tuple_args[0]
  folder_to_process = folder_to_process.replace('_','')
  syst_ext = tuple_args[1]

  isData = False
  if 'Run201' in folder_to_process: isData = True

  #Deal with JER/C, Hdamp, Tune systematics
  loc_str = os.path.join(rootDir[year], folder_to_process)
  if ('Run201' in loc_str) and syst_ext != '': return
  elif (syst_ext in syst2) and not (syst_ext in loc_str): return
  elif (syst_ext in syst1) and any(tmp in loc_str for tmp in syst2): return

  if syst_ext == "": postfix = ""
  else:              postfix = "__"

  #JER/C treatment
  jerc_str = ''; met_pt_str = 'fabs(MET)'; met_phi_str = 'MET_phi'
  if syst_ext == 'jecup':
    jerc_str = ' * jet_JER_Nom * jet_JES_Up'
    met_pt_str  = 'MET_unc_x[0]*MET_unc_x[0] + MET_unc_y[0]*MET_unc_y[0]'
    met_phi_str = 'TMath::ATan(MET_unc_x[0]/MET_unc_y[0])'
  elif syst_ext == 'jecdown':
    jerc_str = ' * jet_JER_Nom * jet_JES_Down'
    met_pt_str  = 'MET_unc_x[1]*MET_unc_x[1] + MET_unc_y[1]*MET_unc_y[1]'
    met_phi_str = 'TMath::ATan(MET_unc_x[1]/MET_unc_y[1])'
  elif syst_ext == 'jerup':
    jerc_str = ' * jet_JER_Up'
    met_pt_str  = 'MET_unc_x[2]*MET_unc_x[2] + MET_unc_y[2]*MET_unc_y[2]'
    met_phi_str = 'TMath::ATan(MET_unc_x[2]/MET_unc_y[2])'
  elif syst_ext == 'jerdown':
    jerc_str = ' * jet_JER_Down'
    met_pt_str  = 'MET_unc_x[3]*MET_unc_x[3] + MET_unc_y[3]*MET_unc_y[3]'
    met_phi_str = 'TMath::ATan(MET_unc_x[3]/MET_unc_y[3])'
  elif not isData:
    jerc_str = ' * jet_JER_Nom'


  hists = []
  #Open dataframe and create output root file
  d = load_file( get_file_list(rootDir[year], tuple_args[0]), default_branch )
  out = TFile.Open( os.path.join(outDir, 'hist_' + folder_to_process.replace(syst_ext,'')) + postfix + syst_ext + '.root', 'RECREATE' )

  #Cut flow, lepton first
  d = d.Define('lep_sel', '(channel == 0 && lepton_pt > 30 && abs(lepton_eta) <= 2.4) ||\
                           (channel == 1 && lepton_pt > 30 && abs(lepton_eta) <= 2.4)').Filter('lep_sel > 0')

  #Define base weight
  d = d.Define('wrongPVrate', '{}'.format(wrongPVRate(folder_to_process, year)))\
       .Define('folder_to_process', '"' + folder_to_process + '"')\
       .Define('prefireweight_F', 'convertRVecDoubleToFloat(prefireweight)')\
       .Define('lepton_SF_F', 'fillLepSFArray(lepton_SF, channel, 12)')\
       .Define('lepton_SF_M', 'splitLepSFArray(lepton_SF, channel, 0, 12)')\
       .Define('lepton_SF_E', 'splitLepSFArray(lepton_SF, channel, 1, 12)')

  #tmp = ROOT.vector("string")()
  #tmp.push_back('lepton_SF_M')
  #tmp.push_back('lepton_SF_E')
  #tmp.push_back('channel')
  #pp = d.Display(tmp)
  #pp.Print()

  if isData: d = d.Define('EventWeight', '1')
  else:
    for i in xrange(len(syst_key_list())):
      syst_name = syst_key_list()[i]
      syst_weight_str = get_syst_weight(syst_name)
      d = d.Define('EventWeight' + syst_name, syst_weight_str)

  #Treat JER/C, MET
  d = d.Define('jet_pt_jerc', 'jet_pt' + jerc_str)\
       .Define('met_pt_jerc', met_pt_str).Define('met_phi_jerc', met_phi_str)

  d = d.Define('lepDphi', 'ROOT::VecOps::DeltaPhi(static_cast<float>(met_phi_jerc), static_cast<float>(lepton_phi))')\
       .Define('transverseM', 'transverseMass(lepton_pt, lepton_eta, lepton_phi, lepton_e, met_pt_jerc, 0, met_phi_jerc, met_pt_jerc)')

  d = d.Define('njet_jerc', 'Sum(jet_pt_jerc > 30 && abs(jet_eta) < 2.4)')\
       .Define('nbjet_jerc', 'Sum(jet_pt_jerc > 30 && abs(jet_eta) < 2.4 && jet_deepCSV > ' + b_tagging(year) + ')')

  #Run on step0
  lepton_dict = lepton_sel(year)
  for l_key, l_value in lepton_dict.items():

    for s_idx in xrange(len(syst_key_list())):
      if len(syst_ext) > 0 and s_idx > 0: continue
      syst_name = syst_key_list()[s_idx]
      wgt_str = 'EventWeight' + syst_name

      if '__mu' in syst_name and l_key == '1': wgt_str = 'EventWeight'
      if '__el' in syst_name and l_key == '0': wgt_str = 'EventWeight'
      if not any(s in folder_to_process for s in ['TTpowheg','TTLL','TTHad']):
        if any(t in syst_name for t in ['__scale','__ps','__pdf']): continue 

      hist_dict = histos(l_key, 0, postfix + syst_key_list()[s_idx])
      for h_key, h_value in hist_dict.items():

        if h_key == 'EventWeight': h = d.Filter(l_value).Histo1D(h_value, h_key)
        else: h = d.Filter(l_value).Histo1D(h_value, h_key, wgt_str)
        hists.append(h)

  #Baseline jet selection to shorten time
  d = d.Filter('njet_jerc >= 3')

  cut_dict = cut_flow()
  for c_key, c_value in cut_dict.items():
    lepton_dict = lepton_sel(year)

    for l_key, l_value in lepton_dict.items():

      for s_idx in xrange(len(syst_key_list())):
        if len(syst_ext) > 0 and s_idx > 0: continue
        syst_name = syst_key_list()[s_idx]
        wgt_str = 'EventWeight' + syst_name

        if '__mu' in syst_name and l_key == '1': wgt_str = 'EventWeight'
        if '__el' in syst_name and l_key == '0': wgt_str = 'EventWeight'
        if not any(s in folder_to_process for s in ['TTpowheg','TTLL','TTHad']):    
          if any(t in syst_name for t in ['__scale','__ps','__pdf']): continue  

        hist_dict = histos(l_key, c_key, postfix + syst_key_list()[s_idx])
        for h_key, h_value in hist_dict.items():

          if h_key == 'EventWeight': h = d.Filter(l_value + c_value, c_key).Histo1D(h_value, h_key)
          else: h = d.Filter(l_value + c_value, c_key).Histo1D(h_value, h_key, wgt_str)
          hists.append(h)

  for hist in hists:
    hist.Write()

  out.Close()
  print "Finished " + os.path.join(outDir, 'hist_' + folder_to_process.replace(syst_ext,'')) + postfix + syst_ext + '.root'

if __name__ == '__main__':
  pool = multiprocessing.Pool(10)
  pool.map(run_ana, list_args)
  pool.close()
  pool.join()
  #print "test"

print(process.memory_info()[0]/(1024.0*1024)) #rss only
print(process.cpu_times())
