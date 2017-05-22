
import urllib.request
import os
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import AllChem
from rdkit.Chem import BRICS
from rdkit.Chem import rdMolDescriptors
from rdkit.Chem import rdFMCS

genus = ""
CurrentDir = os.getcwd()


def get_molfile(gen):
    global C_numbers
    C_number = []
    genus = gen
    url = "http://kanaya.naist.jp/knapsack_jsp/result.jsp?sname=all&word=%s" % (genus)
    try:
        if os.getcwd() == CurrentDir:
            os.mkdir(genus)
    except FileExistsError:
        pass
    if os.getcwd() == CurrentDir:
        os.chdir(genus)

    urllib.request.urlretrieve(url, '%s.txt' % (genus))
    with open("%s.txt" % (genus)) as ld:
        lines = ld.readlines()

    for line in lines:
        if line.find("word=C") >= 0:
            C_number.append(line[49:-34])
            urllib.request.urlretrieve("http://knapsack3d.sakura.ne.jp/mol3d/%s.3d.mol" % (line[49:-34]), '%s.mol' % (line[49:-34]))
    C_numbers = C_number
    os.chdir(CurrentDir)

    return C_number


def make_sdffile():
    if os.getcwd() == CurrentDir:
        os.chdir(genus)
    mols = []
    for i in C_numbers:
        mol_data = open('%s.mol' % (i), 'r').read()
        mol = Chem.MolFromMolBlock(mol_data)
        mols.append(mol)
    outf = Chem.SDWriter("output.sdf")
    for mol in mols:
        AllChem.Compute2DCoords(mol)
        outf.write(mol)
    os.chdir(CurrentDir)
    return None


def search_MCS(sdf, write=0):
    if os.getcwd() == CurrentDir:
        os.chdir(genus)
    ms = [m for m in Chem.SDMolSupplier(sdf) if m is not None]
    mcs = rdFMCS.FindMCS(ms)
    mcs_smarts = mcs.smartsString
    mcs_mol = Chem.MolFromSmarts(mcs_smarts)
    for i, m in enumerate(ms):
        match_atoms = m.GetSubstructMatch(mcs_mol)
        if write:
            print(match_atoms)
        Draw.MolToFile(m, 'comp_%d.png' % i, highlightAtoms=match_atoms)
    os.chdir(CurrentDir)
    return None
