import collections

def cut_flow(bdiscr):

  b_discr = str(bdiscr)
  d = collections.OrderedDict()
  d['1'] = ' && njet_jerc == 3'
  d['2'] = ' && njet_jerc == 3 && nbjet_jerc == 2'
  d['3'] = ' && njet_jerc == 3 && nbjet_jerc == 3'
  d['4'] = ' && njet_jerc >= 3 && nbjet_jerc >= 2'
  d['5'] = ' && njet_jerc >= 4'
  d['6'] = ' && njet_jerc >= 4 && nbjet_jerc == 2'
  d['7'] = ' && njet_jerc >= 4 && nbjet_jerc == 3'
  d['8'] = ' && njet_jerc >= 4 && nbjet_jerc == 4'

  return d


def lepton_sel(year):

  d = collections.OrderedDict()
  d['0'] = 'channel == 0'
  d['1'] = 'channel == 1'
  d['2'] = 'lep_sel > 0'

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

  return str(bWP_M)
