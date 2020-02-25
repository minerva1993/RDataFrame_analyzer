import ROOT

def get_syst_weight(key):

  syst_wgt_str = ''
  d = {}
  d['']              = get_base_str(key)
  d['__puup']        = get_base_str(key) + ' * PUWeight[1]'
  d['__pudown']      = get_base_str(key) + ' * PUWeight[2]'
  d['__prefireup']   = get_base_str(key) + ' * prefireweight_F[1]'
  d['__prefiredown'] = get_base_str(key) + ' * prefireweight_F[2]'
  d['__muidup']      = get_base_str(key) + ' * lepton_SF_M[1] * lepton_SF_M[3] * lepton_SF_M[6]'
  d['__muiddown']    = get_base_str(key) + ' * lepton_SF_M[2] * lepton_SF_M[3] * lepton_SF_M[6]'
  d['__elidup']      = get_base_str(key) + ' * lepton_SF_E[1] * lepton_SF_E[3] * lepton_SF_E[6] * lepton_SF_E[9]'
  d['__eliddown']    = get_base_str(key) + ' * lepton_SF_E[2] * lepton_SF_E[3] * lepton_SF_E[6] * lepton_SF_E[9]'
  d['__muisoup']     = get_base_str(key) + ' * lepton_SF_M[4] * lepton_SF_M[0] * lepton_SF_M[6]'
  d['__muisodown']   = get_base_str(key) + ' * lepton_SF_M[5] * lepton_SF_M[0] * lepton_SF_M[6]'
  d['__elrecoup']    = get_base_str(key) + ' * lepton_SF_E[4] * lepton_SF_E[0] * lepton_SF_E[6] * lepton_SF_E[9]'
  d['__elrecodown']  = get_base_str(key) + ' * lepton_SF_E[5] * lepton_SF_E[0] * lepton_SF_E[6] * lepton_SF_E[9]'
  d['__mutrgup']     = get_base_str(key) + ' * lepton_SF_M[7] * lepton_SF_M[0] * lepton_SF_M[3]'
  d['__mutrgdown']   = get_base_str(key) + ' * lepton_SF_M[8] * lepton_SF_M[0] * lepton_SF_M[3]'
  d['__elzvtxup']    = get_base_str(key) + ' * lepton_SF_E[7] * lepton_SF_E[0] * lepton_SF_E[3] * lepton_SF_E[9]'
  d['__elzvtxdown']  = get_base_str(key) + ' * lepton_SF_E[8] * lepton_SF_E[0] * lepton_SF_E[3] * lepton_SF_E[9]'
  d['__eltrgup']     = get_base_str(key) + ' * lepton_SF_E[10] * lepton_SF_E[0] * lepton_SF_E[3] * lepton_SF_E[6]'
  d['__eltrgdown']   = get_base_str(key) + ' * lepton_SF_E[11] * lepton_SF_E[0] * lepton_SF_E[3] * lepton_SF_E[6]'
  d['__lfup']        = get_base_str(key) + ' * (jet_SF_deepCSV_30[0]+jet_SF_deepCSV_30[3])'  
  d['__lfdown']      = get_base_str(key) + ' * (jet_SF_deepCSV_30[0]-jet_SF_deepCSV_30[4])'
  d['__hfup']        = get_base_str(key) + ' * (jet_SF_deepCSV_30[0]+jet_SF_deepCSV_30[5])'
  d['__hfdown']      = get_base_str(key) + ' * (jet_SF_deepCSV_30[0]-jet_SF_deepCSV_30[6])'
  d['__hfstat1up']   = get_base_str(key) + ' * (jet_SF_deepCSV_30[0]+jet_SF_deepCSV_30[7])'
  d['__hfstat1down'] = get_base_str(key) + ' * (jet_SF_deepCSV_30[0]-jet_SF_deepCSV_30[8])'
  d['__hfstat2up']   = get_base_str(key) + ' * (jet_SF_deepCSV_30[0]+jet_SF_deepCSV_30[9])'
  d['__hfstat2down'] = get_base_str(key) + ' * (jet_SF_deepCSV_30[0]-jet_SF_deepCSV_30[10])'
  d['__lfstat1up']   = get_base_str(key) + ' * (jet_SF_deepCSV_30[0]+jet_SF_deepCSV_30[11])'
  d['__lfstat1down'] = get_base_str(key) + ' * (jet_SF_deepCSV_30[0]-jet_SF_deepCSV_30[12])'
  d['__lfstat2up']   = get_base_str(key) + ' * (jet_SF_deepCSV_30[0]+jet_SF_deepCSV_30[13])'
  d['__lfstat2down'] = get_base_str(key) + ' * (jet_SF_deepCSV_30[0]-jet_SF_deepCSV_30[14])'
  d['__cferr1up']    = get_base_str(key) + ' * (jet_SF_deepCSV_30[0]+jet_SF_deepCSV_30[15])'
  d['__cferr1down']  = get_base_str(key) + ' * (jet_SF_deepCSV_30[0]-jet_SF_deepCSV_30[16])'
  d['__cferr2up']    = get_base_str(key) + ' * (jet_SF_deepCSV_30[0]+jet_SF_deepCSV_30[17])'
  d['__cferr2down']  = get_base_str(key) + ' * (jet_SF_deepCSV_30[0]-jet_SF_deepCSV_30[18])'

  for i in xrange(6):
    d['__scale'+str(i)] = get_base_str(key) + ' * scaleweight[{}]'.format(str(i))
  for i in xrange(6):
    d['__ps'+str(i)] = get_base_str(key) + ' * psweight[{}]'.format(str(i))
  for i in xrange(103):
    d['__pdf'+str(i)] = get_base_str(key) + ' * pdfweight[{}]'.format(str(i))

  syst_wgt_str = d[key]
  return syst_wgt_str


def get_base_str(key):

  base_str = 'wrongPVrate * genweight * prefireweight_F[0] * PUWeight[0] * lepton_SF_F[0] * lepton_SF_F[3] * lepton_SF_F[6] * lepton_SF_F[9] * jet_SF_deepCSV_30[0]'

  if   '__pu'      in key: base_str = 'wrongPVrate * genweight * prefireweight_F[0] * lepton_SF_F[0] * lepton_SF_F[3] * lepton_SF_F[6] * lepton_SF_F[9] * jet_SF_deepCSV_30[0]'
  elif '__prefire' in key: base_str = 'wrongPVrate * genweight * PUWeight[0] * lepton_SF_F[0] * lepton_SF_F[3] * lepton_SF_F[6] * lepton_SF_F[9] * jet_SF_deepCSV_30[0]'
  elif any(s in key for s in ['__mu', '__el']):
                           base_str = 'wrongPVrate * genweight * prefireweight_F[0] * PUWeight[0] * jet_SF_deepCSV_30[0]'
  elif any(s in key for s in ['__lf', '__hf', '__cf']):
                           base_str = 'wrongPVrate * genweight * prefireweight_F[0] * PUWeight[0] * lepton_SF_F[0] * lepton_SF_F[3] * lepton_SF_F[6] * lepton_SF_F[9]'

  return base_str
  



def syst_key_list():

  l = ["",
    "__puup", "__pudown", "__prefireup", "__prefiredown",
    "__muidup", "__muiddown", "__muisoup", "__muisodown", "__mutrgup", "__mutrgdown",
    "__elidup", "__eliddown", "__elrecoup", "__elrecodown",
    "__elzvtxup", "__elzvtxdown", "__eltrgup", "__eltrgdown",
    "__lfup", "__lfdown", "__hfup", "__hfdown",
    "__hfstat1up", "__hfstat1down", "__hfstat2up", "__hfstat2down",
    "__lfstat1up", "__lfstat1down", "__lfstat2up", "__lfstat2down",
    "__cferr1up", "__cferr1down", "__cferr2up", "__cferr2down",
    "__scale0", "__scale1", "__scale2", "__scale3", "__scale4", "__scale5",
    "__ps0", "__ps1", "__ps2", "__ps3",
    "__pdf0", "__pdf1", "__pdf2", "__pdf3", "__pdf4",
    "__pdf5", "__pdf6", "__pdf7", "__pdf8", "__pdf9",
    "__pdf10", "__pdf11", "__pdf12", "__pdf13", "__pdf14",
    "__pdf15", "__pdf16", "__pdf17", "__pdf18", "__pdf19",
    "__pdf20", "__pdf21", "__pdf22", "__pdf23", "__pdf24",
    "__pdf25", "__pdf26", "__pdf27", "__pdf28", "__pdf29",
    "__pdf30", "__pdf31", "__pdf32", "__pdf33", "__pdf34",
    "__pdf35", "__pdf36", "__pdf37", "__pdf38", "__pdf39",
    "__pdf40", "__pdf41", "__pdf42", "__pdf43", "__pdf44",
    "__pdf45", "__pdf46", "__pdf47", "__pdf48", "__pdf49",
    "__pdf50", "__pdf51", "__pdf52", "__pdf53", "__pdf54",
    "__pdf55", "__pdf56", "__pdf57", "__pdf58", "__pdf59",
    "__pdf60", "__pdf61", "__pdf62", "__pdf63", "__pdf64",
    "__pdf65", "__pdf66", "__pdf67", "__pdf68", "__pdf69",
    "__pdf70", "__pdf71", "__pdf72", "__pdf73", "__pdf74",
    "__pdf75", "__pdf76", "__pdf77", "__pdf78", "__pdf79",
    "__pdf80", "__pdf81", "__pdf82", "__pdf83", "__pdf84",
    "__pdf85", "__pdf86", "__pdf87", "__pdf88", "__pdf89",
    "__pdf90", "__pdf91", "__pdf92", "__pdf93", "__pdf94",
    "__pdf95", "__pdf96", "__pdf97", "__pdf98", "__pdf99",
    "__pdf100", "__pdf101", "__pdf102"]

  return l


