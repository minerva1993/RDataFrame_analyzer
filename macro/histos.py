import ROOT
import collections

def histos(ch, step, syst_int):

  d = collections.OrderedDict()
  d['GoodPV'] = ROOT.RDF.TH1DModel('h_PV_Ch{}_S{}{}'.format(ch, step, syst_int), ';Good PV;Entries', 60, 0, 60)
  d['EventWeight'] = ROOT.RDF.TH1DModel('h_EventWeight_Ch{}_S{}{}'.format(ch, step, syst_int), ';Event Weights;Entries', 100, 0, 2)
  #d['njet_jerc'] = ROOT.RDF.TH1DModel('h_NJet_Ch{}_S{}{}'.format(ch, step, syst_int), ';Jet Multiplicity;Entries', 12, 0, 12)
  #d['nbjet_jerc'] = ROOT.RDF.TH1DModel('h_NBJetCSVv2M_Ch{}_S{}{}'.format(ch, step, syst_int), ';b-tagged Jet Multiplicity (DeepCSVM);Entries', 6, 0, 6)
  #d['met_pt_jerc'] = ROOT.RDF.TH1DModel('h_MET_Ch{}_S{}{}'.format(ch, step, syst_int), ';MET (GeV);Entries', 30, 0, 200)
  #d['lepton_pt'] = ROOT.RDF.TH1DModel('h_LepPt_Ch{}_S{}{}'.format(ch, step, syst_int), ';Lepton p_{T} (GeV);Entries', 30, 0, 200)
  #d['lepton_phi'] = ROOT.RDF.TH1DModel('h_LepPhi_Ch{}_S{}{}'.format(ch, step, syst_int), ';Lepton |#phi|;Entries', 30, 0, 3.2)
  #d['lepton_eta'] = ROOT.RDF.TH1DModel('h_LepEta_Ch{}_S{}{}'.format(ch, step, syst_int), ';Lepton #eta;Entries', 30, -2.5, 2.5)
  #d['transverseM'] = ROOT.RDF.TH1DModel('h_WMass_Ch{}_S{}{}'.format(ch, step, syst_int), ';W Transverse Mass (Lep) (GeV);Entries', 30, 30, 200)
  #d['lepDphi'] = ROOT.RDF.TH1DModel('h_DPhi_Ch{}_S{}{}'.format(ch, step, syst_int), ';Lepton MET #Delta#phi;Entries', 30, 0, 3.2)
  #d[''] = ROOT.RDF.TH1DModel('h__Ch{}_S{}{}'.format(ch, step, syst_int), ';;Entries', , , )
  #d[''] = ROOT.RDF.TH1DModel('h__Ch{}_S{}{}'.format(ch, step, syst_int), ';;Entries', , , )
  #d[''] = ROOT.RDF.TH1DModel('h__Ch{}_S{}{}'.format(ch, step, syst_int), ';;Entries', , , )
  #d[''] = ROOT.RDF.TH1DModel('h__Ch{}_S{}{}'.format(ch, step, syst_int), ';;Entries', , , )
  #d[''] = ROOT.RDF.TH1DModel('h__Ch{}_S{}{}'.format(ch, step, syst_int), ';;Entries', , , )
  #d[''] = ROOT.RDF.TH1DModel('h__Ch{}_S{}{}'.format(ch, step, syst_int), ';;Entries', , , )
  #d[''] = ROOT.RDF.TH1DModel('h__Ch{}_S{}{}'.format(ch, step, syst_int), ';;Entries', , , )
  #d[''] = ROOT.RDF.TH1DModel('h__Ch{}_S{}{}'.format(ch, step, syst_int), ';;Entries', , , )
  #d[''] = ROOT.RDF.TH1DModel('h__Ch{}_S{}{}'.format(ch, step, syst_int), ';;Entries', , , )

  return d

