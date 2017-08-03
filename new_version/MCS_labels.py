
import urllib.request
import os
import time
from rdkit.Chem import rdFMCS
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import rdDepictor


def get_Cnlist_from_label(label):
    with open("Streptomyces.kcfs")as f:
        file = f.read()
        molecule = file.split("///\n")
        Cnlist = []
        for mole in molecule:
            if mole.find(label) > 0:
                Cn = mole.split("\n")[0].split()[1]
                Cnlist.append(Cn)
        return Cnlist


def get_molfile(Cnlist):
    if not os.path.exists("KNApSaAck_mol"):
        os.mkdir("KNApSaAck_mol")
    for Cn in Cnlist:
        if not os.path.exists('KNApSaAck_mol/%s.mol' % (Cn)):
            time.sleep(2)
            urllib.request.urlretrieve("http://knapsack3d.sakura.ne.jp/mol3d/%s.3d.mol" % (Cn), 'KNApSaAck_mol/%s.mol' % (Cn))
            time.sleep(2)
    return True


def find_MCS(Cnlist, filename="mcs.png"):
    ms = []
    for Cn in Cnlist:
        with open('KNApSaAck_mol/%s.mol' % (Cn))as f:
            mol = Chem.MolFromMolBlock(f.read())
            rdDepictor.Compute2DCoords(mol)
            ms.append(mol)
    mcs = rdFMCS.FindMCS(ms)
    mcs_smarts = mcs.smartsString
    mcsMol = Chem.MolFromSmarts(mcs_smarts, mergeHs=True)
    Draw.MolToFile(Chem.Mol(mcsMol.ToBinary()), filename, kekulize=False)
    return True


def find_MCS_grid_image(Cnlist, filename="all_comp.png"):
    ms = []
    for Cn in Cnlist:
        with open('KNApSaAck_mol/%s.mol' % (Cn))as f:
            mol = Chem.MolFromMolBlock(f.read())
            rdDepictor.Compute2DCoords(mol)
            ms.append(mol)
    mcs = rdFMCS.FindMCS(ms, matchValences=True, completeRingsOnly=True)
    mcs_smarts = mcs.smartsString
    mcs_mol = Chem.MolFromSmarts(mcs_smarts)
    match_list = []
    for i, m in enumerate(ms):
        match_atoms = m.GetSubstructMatch(mcs_mol)
        match_list.append(match_atoms)
    img = Draw.MolsToGridImage(ms, highlightAtomLists=match_list, legends=Cnlist, subImgSize=(400, 400))
    img.save(filename)


def main():
    Cnlist = get_Cnlist_from_label(input())
    get_molfile(Cnlist)
    find_MCS(Cnlist)
    find_MCS_grid_image(Cnlist)


if __name__ == '__main__':
    main()
