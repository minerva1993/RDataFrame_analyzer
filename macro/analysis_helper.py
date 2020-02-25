import ROOT
import os, sys

RDF = ROOT.ROOT.RDataFrame

def get_file_list(rootDir, dataset):

  out = []
  tmp = os.listdir(os.path.join(rootDir, dataset))
  for i in tmp:
    if not i.endswith('.root'): continue
#    if not i.endswith('000.root'): continue 
#    if i.endswith('001.root'): continue 
#    if i.endswith('002.root'): continue 
#    if i.endswith('003.root'): continue 
#    if i.endswith('004.root'): continue 
#    if i.endswith('005.root'): continue 
#    if i.endswith('006.root'): continue 
#    if i.endswith('007.root'): continue 
#    if i.endswith('008.root'): continue 
    out.append(os.path.join(rootDir,dataset,i))

  return out
    

def load_file(fileList, branchList):

  vec_file = ROOT.vector("string")()
  for i in xrange(len(fileList)):
    vec_file.push_back(fileList[i])

  vec_br = ROOT.vector("string")()
  for i in xrange(len(branchList)):
    vec_br.push_back(branchList[i])

  treeName = "fcncLepJets/tree"
  d = RDF(treeName, vec_file, vec_br)

  return d


def wrongPVRate(fileName, year):

  if int(year) == 2017:
    if   "DYJets10to50"            in fileName: wrongPVrate = 1.02921
    elif "QCDEM15to20"             in fileName: wrongPVrate = 1.01333
    elif "QCDEM20to30"             in fileName: wrongPVrate = 1.01227
    elif "QCDEM300toInf"           in fileName: wrongPVrate = 1.01194
    elif "QCDEM50to80"             in fileName: wrongPVrate = 1.02226
    elif "QCDMu120to170"           in fileName: wrongPVrate = 1.01289
    elif "QCDMu170to300"           in fileName: wrongPVrate = 1.01181
    elif "QCDMu20to30"             in fileName: wrongPVrate = 1.0253
    elif "QCDMu30to50"             in fileName: wrongPVrate = 1.02105
    elif "QCDMu470to600"           in fileName: wrongPVrate = 1.0141
    elif "QCDMu50to80"             in fileName: wrongPVrate = 1.01149
    elif "QCDMu80to120"            in fileName: wrongPVrate = 1.01278
    elif "TTLLpowhegttbbhdampup"   in fileName: wrongPVrate = 1.01807
    elif "TTLLpowhegttcchdampup"   in fileName: wrongPVrate = 1.01978
    elif "TTLLpowhegttlfhdampup"   in fileName: wrongPVrate = 1.01938
    elif "TTZToLLNuNu"             in fileName: wrongPVrate = 1.02425
    elif "TTpowhegttbbTuneCP5down" in fileName: wrongPVrate = 1.02715
    elif "TTpowhegttbbhdampdown"   in fileName: wrongPVrate = 1.02717
    elif "TTpowhegttccTuneCP5down" in fileName: wrongPVrate = 1.0273
    elif "TTpowhegttcchdampdown"   in fileName: wrongPVrate = 1.02746
    elif "TTpowhegttlfTuneCP5down" in fileName: wrongPVrate = 1.02742
    elif "TTpowhegttlfhdampdown"   in fileName: wrongPVrate = 1.02774
    elif "W3JetsToLNu"             in fileName: wrongPVrate = 1.02348
    elif "WW"                      in fileName: wrongPVrate = 1.0295
    elif "WZ"                      in fileName: wrongPVrate = 1.02298
    elif "ZZ"                      in fileName: wrongPVrate = 1.01508
    else: wrongPVrate = 1.0

  else: wrongPVrate = 1.0

  return float(wrongPVrate)


#Transverse Mass
ROOT.gInterpreter.Declare("""
double transverseMass(double p1_pt, double p1_eta, double p1_phi, double p1_e, double p2_pt, double p2_eta, double p2_phi, double p2_e){

  TLorentzVector lepton, met;
  lepton.SetPtEtaPhiE(p1_pt, p1_eta, p1_phi, p1_e);
  met.SetPtEtaPhiE(p2_pt, p2_eta, p2_phi, p2_e);

  TLorentzVector leptonT(lepton.Px(),lepton.Py(),0.,lepton.E()*TMath::Sin(lepton.Theta()));
  TLorentzVector metT(met.Px(), met.Py(), 0, met.E());

  TLorentzVector sumT=leptonT+metT;
  float out = sumT.M();

  return out;
};
""")


ROOT.gInterpreter.Declare("""
ROOT::VecOps::RVec<float> convertRVecDoubleToFloat( const ROOT::VecOps::RVec<double> &v ){

  ROOT::VecOps::RVec<float> out;

  for( int i=0; i<v.size(); i++ ){
    out.push_back( static_cast<float>(v.at(i)) );
  }
  return out;
};
""")

ROOT.gInterpreter.Declare("""
ROOT::VecOps::RVec<float> fillLepSFArray( const ROOT::VecOps::RVec<float> &v, int ch, int num ){

  ROOT::VecOps::RVec<float> out;

  for( int i=0; i<v.size(); i++ ){
    float tmpSF = v.at(i);
    if( ch == 0 ){
      int sf_idx = i / 3;
      int var_idx = i % 3;
      if( var_idx != 0 ){
        tmpSF = v.at(sf_idx) + pow(-1, var_idx+1) * sqrt(pow(v.at(i) - v.at(sf_idx), 2) + pow(0.005, 2));
      }
    }
    out.push_back(tmpSF);
  }
  if(out.size() < num){
    while( out.size() != num ) out.push_back(1.0);
  }
  return out;
};
""")

ROOT.gInterpreter.Declare("""
ROOT::VecOps::RVec<float> splitLepSFArray( const ROOT::VecOps::RVec<float> &v, int ch, int out_ch, int num ){

  ROOT::VecOps::RVec<float> out;

  for( int i=0; i<v.size(); i++ ){

    int sf_idx = i / 3;
    int var_idx = i % 3;

    float tmpSF = 1.0;

    if( ch == out_ch ){
      if( ch == 0 ){
        if( var_idx != 0 ){
          tmpSF = v.at(sf_idx) + pow(-1, var_idx+1) * sqrt(pow(v.at(i) - v.at(sf_idx), 2) + pow(0.005, 2));
        }
        else tmpSF = v.at(i);
      }
      else tmpSF = v.at(i);
    }
    out.push_back(tmpSF);
  }
  
  if(out.size() < num){
    while( out.size() != num ) out.push_back(1.0);
  }

  return out;
};
""")
