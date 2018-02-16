
def search_all_Cnumber_from_label(label, ring=False, Type=None):
    import re

    if ring:
        Cnset = set()
        counter = 0
        for lab in mawasu(label):
            Cnset2, tempcounter = search_all_Cnumber_from_label(lab, ring=False,
                                                                Type=Type)
            counter += tempcounter
            for Cn in Cnset2:
                Cnset.add(Cn)
        return sorted(list(Cnset)), counter

    label_list = re.split("[-()+]", label)
    sep_list = re.split("[a-zA-Z][0-9]?[a-z]?", label)
    query = ""
    for i in range(label_list.count("")):
        label_list.remove("")
    for i in range(len(label_list)):
        label_list[i] += "[0-9]?[a-z]?"
    if sep_list[-1] != "":
        label_list.append("")
    for l1, l2 in zip(sep_list, label_list):
        query += l1 + l2
    query = re.sub("\(", "[(]", query)
    query = re.sub("\)", "[)]", query)
    query = re.sub("\+", "[+]", query)
    query += "\s"
    query = "\s" + query
    Cnset = set()
    counter = 0
    for i in ["1-9", "10-19", "20-29", "30-39", "40-49", "50-59"]:
        with open("../../../database/kcfs/KNApSAck" + i + ".kcfs")as f:
            file = f.read()
            molecule = file.split("///\n")
            for mole in molecule:
                if re.search(query, mole) is None:
                    continue
                for line in mole.split("\n")[2:]:
                    line_ = line
                    if re.match("^\s\s\S", line_):
                        type_ = line.split()[0]
                        line_ = " ".join(line_.split()[1:])
                        line_ = " " + line_
                    if Type is not None and Type != type_:
                        continue
                    if re.search(query, line_) is not None:
                        Cn = mole.split("\n")[0].split()[1]
                        Cnset.add(Cn)
                        counter += int(line_.split()[1][1:-1])
    return sorted(list(Cnset)), counter


def get_name(Cnumber):
    import requests
    import lxml.html
    html = requests.get("http://kanaya.naist.jp/knapsack_jsp/information.jsp?word=" + Cnumber)
    dom = lxml.html.fromstring(html.text)
    name = dom.xpath('//*[@id="my_contents"]/table/tr[2]/td[1]/table/tr[1]/td')[0].text
    return name


def get_genuses(Cnumber, other=True, genus=None, timeout=60):
    import lxml.html
    import requests
    import time
    genuses_list = []
    html = requests.get("http://kanaya.naist.jp/knapsack_jsp/information.jsp?word=" + Cnumber, timeout)
    time.sleep(1)
    dom = lxml.html.fromstring(html.text)
    for element in dom.xpath('//*[@class="org2"]'):
        genus2 = element.text.split()[0]
        if other:
            genuses_list.append(element.text.replace("\xa0", " ")[:-1])
        else:
            if genus2 == genus:
                genuses_list.append(element.text.replace("\xa0", " ")[:-1])
    return genuses_list


def downer(label, level=1):
    import re
    label_list = re.split("[-()+]", label)
    sep_list = re.split("[a-zA-Z][0-9]?[a-z]?", label)
    query = ""
    for i in range(label_list.count("")):
        label_list.remove("")
    for i in range(len(label_list)):
        label_list[i] = label_list[i][:level]
    if sep_list[-1] != "":
        label_list.append("")
    for l1, l2 in zip(sep_list, label_list):
        query += l1 + l2
    return query


def search(Cnumberlist, filename=None):
    "make kcffile only given Cnumbers from all kcffile"
    if filename is None:
        filename = "kcfs.kcfs"
    with open(filename, "w"):
        pass

    for Cnumber in Cnumberlist:
        Cn = int(Cnumber[1:])
        if Cn <= 9217:
            page = "1-9"
        elif Cn <= 19275:
            page = "10-19"
        elif Cn <= 29326:
            page = "20-29"
        elif Cn <= 39355:
            page = "30-39"
        elif Cn <= 49370:
            page = "40-49"
        elif Cn <= 50409:
            page = "50-59"
        else:
            print("your Cnumber " + Cnumber + " is too large")
            continue

        with open("../../../database/kcfs/KNApSAck" + page + ".kcfs") as f:
            for (i, line) in enumerate(f):
                # print(line[12:21]) # C00000000
                if line[12:21] == Cnumber:
                    # temp = i
                    # print("find", temp)
                    lin = line
                    flag = 0
                    with open(filename, "a") as fw:
                        while((lin[:5] != "ENTRY" and lin != "") or flag != 1):
                            flag = 1
                            fw.write(lin)
                            lin = f.readline()
                        else:
                            break
    return True


def kcfs2count(kcfs, txt):
    import re
    dic = {}
    with open(kcfs, "r") as f:
        for mol in f.read(None).split("///\n"):
            # sta = 0
            sta2 = 0
            type_ = 0
            for line in mol.split("\n"):
                # if re.match("^\S", line):
                    # sta = line.split()[0]
                if re.match("^\s\s\S", line):
                    sta2 = line.split()[0]
                if re.match("///", line):
                    pass
                elif sta2:
                    a = line[12:].split()
                    type_ = sta2
                    try:
                        num = int(re.findall("\d+", a[1])[0])
                        str_ = a[0]
                    except IndexError:
                        continue
                    str1 = re.sub("[a-z]", "", str_)
                    str2 = re.sub("\d", "", str1)
                    dic.setdefault((type_, str_), 0)
                    dic[(type_, str_)] += num
                    dic.setdefault((type_, str2), 0)
                    dic[(type_, str2)] += num
                    dic.setdefault((type_, str1), 0)
                    dic[(type_, str1)] += num

    array = []
    for item in dic.items():
        array += [[0 - item[1], item[0]]]

    with open(txt, "w") as f2:
        index = 0
        for list_ in sorted(array):
            index += 1
            num = str(index)
            while(len(num) < 8):
                num = "0" + num
            num = "S" + num + list_[1][0][0]
            f2.write(num + "\t" + list_[1][0] + "\t" + list_[1][1] + "\t" + str(0 - list_[0]) + "\n")
    return True


def mawasu(label):
    units = label.split("-")
    for i in range(len(units)):
        ret = units[i:] + units[:i]
        yield "-".join(ret)


def reverse(label):
    units = label.split("-")
    rev = ""
    for unit in units:
        rev = unit + "-" + rev
    return rev[:-1]


def kcfs2count2(kcfs, txt):
    import re
    dic = {}
    with open(kcfs, "r") as f:
        for mol in f.read(None).split("///\n"):
            # sta = 0
            sta2 = 0
            type_ = 0
            for line in mol.split("\n"):
                # if re.match("^\S", line):
                    # sta = line.split()[0]
                if re.match("^\s\s\S", line):
                    sta2 = line.split()[0]
                if re.match("///", line):
                    pass
                elif sta2:
                    a = line[12:].split()
                    type_ = sta2
                    try:
                        num = int(re.findall("\d+", a[1])[0])
                        str_ = a[0]
                    except IndexError:
                        continue
                    str1 = re.sub("[a-z]", "", str_)
                    str2 = re.sub("\d", "", str1)
                    if type_ == "RING":
                        ringlist1 = [i for i in mawasu(str1)]
                        ringlist2 = [i for i in mawasu(str2)]
                        str1 = sorted(ringlist1)[0]
                        str2 = sorted(ringlist2)[0]
                    elif type_ == "SKELETON":
                        rev1 = reverse(str1)
                        rev2 = reverse(str2)
                        if rev1 < str1:
                            str1 = rev1
                        if rev2 < str2:
                            str2 = rev2
                    dic.setdefault((type_, str_), 0)
                    dic[(type_, str_)] += num
                    dic.setdefault((type_, str2), 0)
                    dic[(type_, str2)] += num
                    dic.setdefault((type_, str1), 0)
                    dic[(type_, str1)] += num

    array = []
    for item in dic.items():
        array += [[0 - item[1], item[0]]]

    with open(txt, "w") as f2:
        index = 0
        for list_ in sorted(array):
            index += 1
            num = str(index)
            while(len(num) < 8):
                num = "0" + num
            num = "S" + num + list_[1][0][0]
            f2.write(num + "\t" + list_[1][0] + "\t" + list_[1][1] + "\t" + str(0 - list_[0]) + "\n")
    return True


def split(countfile, result="test.txt", limit=0):
    with open(countfile, "r") as f:
        with open(result, "w") as f2:
            for line in f:
                i = -1
                if line[11] == "R":
                    i = -1
                    while(True):
                        if line[i] == "\t":
                            # print(line[i+1:])
                            break
                        i -= 1
                    if int(line[i + 1:]) < limit:
                        break
                    # print(line)
                    f2.write(line)
                elif line[11] == "I":
                    i = -1
                    while(True):
                        if line[i] == "\t":
                            # print(line[i+1:])
                            break
                        i -= 1
                    if int(line[i + 1:]) < limit:
                        break
                    # print(line)
                    f2.write(line)
                elif line[11] == "S":
                    i = -1
                    while(True):
                        if line[i] == "\t":
                            # print(line[i+1:])
                            break
                        i -= 1
                    if int(line[i + 1:]) < limit:
                        break
                    # print(line)
                    f2.write(line)
    return True


def make_kcfs(Cnlist, path, limit=2000, splimit=0):
    search(Cnlist, path + "kcfs.kcfs")
    kcfs2count(path + "kcfs.kcfs", path + "kcfscount.txt")
    split(path + "kcfscount.txt", path + "splitedcount.txt", splimit)
    return True


def make_kcfs2(Cnlist, path, limit=2000, splimit=0):
    search(Cnlist, path + "kcfs.kcfs")
    kcfs2count2(path + "kcfs.kcfs", path + "kcfscount.txt")
    split(path + "kcfscount.txt", path + "splitedcount.txt", splimit)
    return True


def make_mol_object(Cnlist, rdD=True):
    import sys
    sys.path.append("../../module")
    import kcf.converter as kcfco
    from rdkit.Chem import rdDepictor
    from rdkit import Chem

    hanni = []
    for i in range(1, 52):
        page = str(i)
        with open("../../../database/knapsack-kcf/KNApSAck" + page + ".kcf")as f1:
            hanni.append(f1.read().split()[1])

    mol_list = []
    counter = 0
    nCnumber = []
    for z, Cn in enumerate(sorted(Cnlist)):
        num = int(Cn[1:])
        for p, hanCn in enumerate(hanni[1:]):
            hannum = int(hanCn[1:])
            if hannum > num:
                pagenum = str(p+1)
                with open("../../../database/knapsack-kcf/KNApSAck" + pagenum + ".kcf")as f2:
                    complist = f2.read().split("///\n")
                    try:
                        for comp in complist:
                            if Cn == comp.split()[1]:
                                molblock = kcfco.kcf_to_molblock(comp)
                                # print("OK", i)
                                # print(molblock[1])
                                mol = Chem.MolFromMolBlock(molblock[1])
                                if mol is None:
                                    print("None", Cn, z)
                                    if "#+" in comp or "#-" in comp:
                                        print("Charge #- or #+ in\n")
                                    counter += 1
                                    break
                                if rdD:
                                    rdDepictor.Compute2DCoords(mol)
                                mol_list.append(mol)
                                nCnumber.append(i)
                                if "#+" in comp or "#-" in comp:
                                    print(Cn, z, k3, "Charge in  but have no error\n")
                                break
                    except IndexError:
                        counter += 1
                        print("IndexError", Cn, z)
                break
    print("number of Compound having charge is " + str(counter))
    return mol_list


def draw_png(cn_list, filename, highlight=[]):
    from rdkit.Chem import Draw

    mol_list = make_mol_object(cn_list)
    img = Draw.MolsToGridImage(mol_list, legends=cn_list, subImgSize=(400, 400),
                               highlightAtomLists=highlight)
    img.save(filename)


def draw_png_with_compound_name(cn_list, filename, highlight):
    from rdkit.Chem import Draw
    import time

    name = []
    for Cnumber in cn_list:
        name.append(get_name(Cnumber))
        time.sleep(3)
    mol_list = make_mol_object(cn_list)
    img = Draw.MolsToGridImage(mol_list, legends=name, subImgSize=(400, 400),
                               highlightAtomLists=highlight)
    img.save(filename)


def draw_png_highlight(cn_list, typelabel, filename, with_Cname=False):
    import os
    import re

    search(cn_list, "tempkcfs.kcfs")
    matchlist = []
    label_list = re.split("[-()]", typelabel[1])
    sep_list = re.split("[a-zA-Z][0-9]?[a-z]?", typelabel[1])
    query = ""
    for i in range(label_list.count("")):
        label_list.remove("")
    for i in range(len(label_list)):
        label_list[i] += "[0-9]?[a-z]?"
    for l1, l2 in zip(sep_list, label_list):
        query += l1 + l2
    query = re.sub("\(", "[(]", query)
    query = re.sub("\)", "[)]", query)
    with open("tempkcfs.kcfs")as f:
        for mol, cn in zip(f.read().split("///\n"), cn_list):
            sta2 = False
            if mol.split()[1] != cn:
                matchlist.append([])
                continue
            for line in mol.split("\n"):
                if re.match("^\s\s\S", line):
                    sta2 = line.split()[0]
                if re.match("///", line):
                    pass
                elif sta2:
                    a = line[12:].split()
                    type_ = sta2
                    try:
                        if type_ == typelabel[0]:
                            if re.fullmatch(query, a[0]) is not None:
                                matchnumber = set()
                                for match in a[2:]:
                                    ma = list(map(int,match.split("-")))
                                    ma = set(map(lambda x: x-1, ma))
                                    matchnumber = matchnumber.union(ma)
                                matchlist.append(sorted(list(matchnumber)))
                                break
                    except IndexError:
                        continue
    if with_Cname:
        draw_png_with_compound_name(cn_list, filename, matchlist)
    else:
        draw_png(cn_list, filename, matchlist)
    os.remove("tempkcfs.kcfs")
    return True

def get_label_atoms_number(label):
    import re

    length = len(re.findall("[A-Z]", label))
    return length
