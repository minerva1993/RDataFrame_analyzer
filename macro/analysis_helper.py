import ROOT
import os, sys

RDF = ROOT.ROOT.RDataFrame

def get_file_list(rootDir, dataset):

  out = []
  tmp = os.listdir(os.path.join(rootDir, dataset))
  for i in tmp:
    if not i.endswith('.root'): continue
    if i.endswith('000.root'): continue 
    if i.endswith('001.root'): continue 
    if i.endswith('002.root'): continue 
    if i.endswith('003.root'): continue 
    if i.endswith('004.root'): continue 
    if i.endswith('005.root'): continue 
    if i.endswith('006.root'): continue 
    if i.endswith('007.root'): continue 
    if i.endswith('008.root'): continue 
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

