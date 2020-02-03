import collections

def cut_flow():

  d = collections.OrderedDict()
  d['0'] = 'channel >= 0'
  d['1'] = 'njets == 3'
  d['2'] = 'njets == 3 && nbjets_m == 2'
  d['3'] = 'njets == 3 && nbjets_m == 3'
  d['4'] = 'njets >= 3 && nbjets_m >= 2'
  d['5'] = 'njets >= 4'
  d['6'] = 'njets >= 4 && nbjets_m == 2'
  d['7'] = 'njets >= 4 && nbjets_m == 3'
  d['8'] = 'njets >= 4 && nbjets_m == 4'

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
