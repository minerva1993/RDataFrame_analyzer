import ROOT
import collections

def histos(ch, step, syst_name):

  d = collections.OrderedDict()
  d['lepton_eta'] = ROOT.RDF.TH1DModel('h_LepEta_Ch{}_S{}{}'.format(ch, step, syst_name),';Lepton |#eta|;Entries',30,-3,3)

  return d
