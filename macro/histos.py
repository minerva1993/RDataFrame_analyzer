import ROOT
import collections

def histos(ch, step, syst_name):

  d = collections.OrderedDict()
  d['GoodPV'] = ROOT.RDF.TH1DModel('h_PV_Ch{}_S{}{}'.format(ch, step, syst_name), ';Good PV;Entries', 60, 0, 60)
  d['lepton_eta'] = ROOT.RDF.TH1DModel('h_LepEta_Ch{}_S{}{}'.format(ch, step, syst_name), ';Lepton |#eta|;Entries', 30, -3, 3)
  d['njet_jerc'] = ROOT.RDF.TH1DModel('h_NJet_Ch{}_S{}{}'.format(ch, step, syst_name), ';Jet Multiplicity;Entries', 12, 0, 12)
  d['nbjet_jerc'] = ROOT.RDF.TH1DModel('h_NBJetCSVv2M_Ch{}_S{}{}'.format(ch, step, syst_name), ';b-tagged Jet Multiplicity (DeepCSVM);Entries', 6, 0, 6)
  #d[''] = ROOT.RDF.TH1DModel('h__Ch{}_S{}{}'.format(ch, step, syst_name), ';;Entries', , , )
  #d[''] = ROOT.RDF.TH1DModel('h__Ch{}_S{}{}'.format(ch, step, syst_name), ';;Entries', , , )
  #d[''] = ROOT.RDF.TH1DModel('h__Ch{}_S{}{}'.format(ch, step, syst_name), ';;Entries', , , )
  #d[''] = ROOT.RDF.TH1DModel('h__Ch{}_S{}{}'.format(ch, step, syst_name), ';;Entries', , , )
  #d[''] = ROOT.RDF.TH1DModel('h__Ch{}_S{}{}'.format(ch, step, syst_name), ';;Entries', , , )
  #d[''] = ROOT.RDF.TH1DModel('h__Ch{}_S{}{}'.format(ch, step, syst_name), ';;Entries', , , )
  #d[''] = ROOT.RDF.TH1DModel('h__Ch{}_S{}{}'.format(ch, step, syst_name), ';;Entries', , , )
  #d[''] = ROOT.RDF.TH1DModel('h__Ch{}_S{}{}'.format(ch, step, syst_name), ';;Entries', , , )
  #d[''] = ROOT.RDF.TH1DModel('h__Ch{}_S{}{}'.format(ch, step, syst_name), ';;Entries', , , )

  return d

