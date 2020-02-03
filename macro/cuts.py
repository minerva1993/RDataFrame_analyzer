import collections

def cut_flow(bdiscr):

  b_discr = str(bdiscr)
  d = collections.OrderedDict()
  d['0'] = ''
  d['1'] = ' && Sum(jet_pt_jerc > 30 && abs(jet_eta) < 2.4) == 3'
  d['2'] = ' && Sum(jet_pt_jerc > 30 && abs(jet_eta) < 2.4) == 3\
             && Sum(jet_pt_jerc > 30 && abs(jet_eta) < 2.4 && jet_deepCSV > ' + b_discr + ') == 2'
  d['3'] = ' && Sum(jet_pt_jerc > 30 && abs(jet_eta) < 2.4) == 3\
             && Sum(jet_pt_jerc > 30 && abs(jet_eta) < 2.4 && jet_deepCSV > ' + b_discr + ') == 3'
  d['4'] = ' && Sum(jet_pt_jerc > 30 && abs(jet_eta) < 2.4) >= 3\
             && Sum(jet_pt_jerc > 30 && abs(jet_eta) < 2.4 && jet_deepCSV > ' + b_discr + ') >= 2'
  d['5'] = ' && Sum(jet_pt_jerc > 30 && abs(jet_eta) < 2.4) >= 4'
  d['6'] = ' && Sum(jet_pt_jerc > 30 && abs(jet_eta) < 2.4) >= 4\
             && Sum(jet_pt_jerc > 30 && abs(jet_eta) < 2.4 && jet_deepCSV > ' + b_discr + ') == 2'
  d['7'] = ' && Sum(jet_pt_jerc > 30 && abs(jet_eta) < 2.4) >= 4\
             && Sum(jet_pt_jerc > 30 && abs(jet_eta) < 2.4 && jet_deepCSV > ' + b_discr + ') == 3'
  d['8'] = ' && Sum(jet_pt_jerc > 30 && abs(jet_eta) < 2.4) >= 4\
             && Sum(jet_pt_jerc > 30 && abs(jet_eta) < 2.4 && jet_deepCSV > ' + b_discr + ') == 4'

  return d


def lepton_sel(year):

  d = collections.OrderedDict()
  if year >= 2017:
    d['0'] = '(channel == 0 && lepton_pt > 30 && abs(lepton_eta) <= 2.4)'
    d['1'] = '(channel == 1 && lepton_pt > 30 && abs(lepton_eta) <= 2.4)'
    d['2'] = '((channel == 0 && lepton_pt > 30 && abs(lepton_eta) <= 2.4)\
             || (channel == 1 && lepton_pt > 30 && abs(lepton_eta) <= 2.4))'

    return d


def b_tagging(year):

  if year == 2017:
    bWP_M = 0.4941
    bWP_T = 0.8001
    cvsbWP_M = 0.28
    cvslWP_M = 0.15

  elif year == 2018:
    bWP_M = 0.4184
    bWP_T = 0.7527
    cvsbWP_M = 0.29
    cvslWP_M = 0.137

  else:
    bWP_M = 0.0
    bWP_T = 0.0
    cvsbWP_M = 0.0
    cvslWP_M = 0.0

  return bWP_M
