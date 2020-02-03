import ROOT
import os, sys

RDF = ROOT.ROOT.RDataFrame

def get_file_list(rootDir, dataset):

  out = []
  tmp = os.listdir(os.path.join(rootDir, dataset))
  for i in tmp:
    if not i.endswith('.root'): tmp.remove(i)
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

