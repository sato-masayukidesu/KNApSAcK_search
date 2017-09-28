
class MCS_Finder(object):
    def __init__(self, genus):
        import urllib.request
        import os
        import time
        from rdkit.Chem import rdFMCS
        from rdkit import Chem
        from rdkit.Chem import Draw
        from rdkit.Chem import rdDepictor
        import requests
        import lxml.html
        import re

        self.genus = genus
        self.mol_list = None

        if not os.path.exists(self.genus):
            os.mkdir(self.genus)

    def get_html(self, genus):
        """
        get htmlfile from KNApSAck search engine

        input
            genus: str, genusric name

        output
            html: requests.models.Response
        """
        import requests
        html = requests.get("http://kanaya.naist.jp/knapsack_jsp/result.jsp?sname=organism&word=" + genus)
        return html

    def get_Cnumber(self, html, limit=2000):
        """
        get Cnumber list from KNApSAck htmlfile

        input
            html: requests.models.Response
            limit: int, itertion limit

        output
            Cnumber: list, sorted list of Cnumber
        """
        import lxml.html
        dom = lxml.html.fromstring(html.text)
        i = 1
        Cnumber = set()
        genus = dom.xpath('//*[@id="my_contents"]/font[2]')[0].text
        genus = genus[0].upper() + genus[1:]
        while(True):
            if i > limit:
                print("max itertion")
                raise Exception("max iteration change limit")

            try:
                Cn = dom.xpath('//*[@class="sortable d1"]/tr[' + str(i) + ']/td[1]/a')[0].text
            except IndexError:
                print("finish getting Cnumber")
                # print(i)
                break

            try:
                if genus != dom.xpath('//*[@class="sortable d1"]/tr[' + str(i) + ']/td[6]/font')[0].text:
                    i += 1
                    continue
            except IndexError:
                print("font error line ", + str(i))
                i += 1
                continue

            Cnumber.add(Cn)
            i += 1
        Cnumber = list(sorted(Cnumber))
        return Cnumber

    def search(self, Cnumberlist, filename=None):
        "make kcffile only given Cnumbers from all kcffile"
        if filename is None:
            filename = self.genus + "/kcfs.kcfs"
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

    def kcfs2count(self, kcfs, txt):
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

    def split(self, countfile, result="test.txt", limit=0):
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

    def make_kcfs(self, limit=2000, splimit=0):
        html = self.get_html(self.genus)
        print("get html")
        Cnumber = self.get_Cnumber(html, limit)
        self.search(Cnumber)
        self.kcfs2count(self.genus + "/kcfs.kcfs", self.genus + "/kcfscount.txt")
        self.split(self.genus + "/kcfscount.txt", self.genus + "/splitedcount.txt", splimit)
        return True

    def make_mol_list(self, Cnlist):
        from rdkit import Chem
        from rdkit.Chem import rdDepictor

        if self.mol_list is None:
            self.mol_list = []
            for Cn in Cnlist:
                with open('KNApSAck_mol/%s.mol' % (Cn))as f:
                    mol = Chem.MolFromMolBlock(f.read())
                    rdDepictor.Compute2DCoords(mol)
                    self.mol_list.append(mol)
            return True
        else:
            return False

    def get_Cnlist_from_label(self, label):
        with open(self.genus + "/kcfs.kcfs")as f:
            file = f.read()
            molecule = file.split("///\n")
            Cnlist = []
            for mole in molecule:
                if mole.find(label) > 0:
                    Cn = mole.split("\n")[0].split()[1]
                    Cnlist.append(Cn)
            return Cnlist

    def get_Cnlist_from_label2(self, label):
        import re
        label_list = re.split("[-()]", label)
        sep_list = re.split("[a-zA-Z][0-9]?[a-z]?", label)
        query = ""
        for i in range(label_list.count("")):
            label_list.remove("")
        for i in range(len(label_list)):
            label_list[i] += "[0-9]?[a-z]?"
        for l1, l2 in zip(sep_list, label_list):
            query += l1 + l2
        query = re.sub("\(", "[(]", query)
        query = re.sub("\)", "[)]", query)
        with open(self.genus + "/kcfs.kcfs")as f:
            file = f.read()
            molecule = file.split("///\n")
            Cnlist = []
            for mole in molecule:
                if re.search(query, mole) is not None:
                    Cn = mole.split("\n")[0].split()[1]
                    Cnlist.append(Cn)
            return Cnlist

    def get_molfile(self, Cnlist):
        import os
        import time
        import urllib.request

        if not os.path.exists("KNApSAck_mol"):
            os.mkdir("KNApSAck_mol")
        for Cn in Cnlist:
            if not os.path.exists('KNApSAck_mol/%s.mol' % (Cn)):
                time.sleep(2)
                urllib.request.urlretrieve("http://knapsack3d.sakura.ne.jp/mol3d/%s.3d.mol" % (Cn), 'KNApSAck_mol/%s.mol' % (Cn))
                time.sleep(2)
        return True

    def find_MCS(self, Cnlist, filename="mcs.png"):
        from rdkit.Chem import rdFMCS
        from rdkit import Chem
        from rdkit.Chem import Draw

        self.make_mol_list(Cnlist)
        mcs = rdFMCS.FindMCS(self.mol_list)
        mcs_smarts = mcs.smartsString
        mcsMol = Chem.MolFromSmarts(mcs_smarts, mergeHs=True)
        Draw.MolToFile(Chem.Mol(mcsMol.ToBinary()), self.genus + "/" + filename, kekulize=False)
        return True

    def find_MCS_grid_image(self, Cnlist, filename="all_comp.png"):
        from rdkit.Chem import rdFMCS
        from rdkit import Chem
        from rdkit.Chem import Draw

        self.make_mol_list(Cnlist)

        mcs = rdFMCS.FindMCS(self.mol_list, matchValences=True, completeRingsOnly=True)
        mcs_smarts = mcs.smartsString
        mcs_mol = Chem.MolFromSmarts(mcs_smarts)
        match_list = []
        for m in self.mol_list:
            match_atoms = m.GetSubstructMatch(mcs_mol)
            match_list.append(match_atoms)
        img = Draw.MolsToGridImage(self.mol_list, highlightAtomLists=match_list, legends=Cnlist, subImgSize=(400, 400))
        img.save(self.genus + "/" + filename)
        return True

    def make_image(self, label):
        self.mol_list = None
        Cnlist = self.get_Cnlist_from_label2(label)
        self.get_molfile(Cnlist)
        self.find_MCS(Cnlist)
        self.find_MCS_grid_image(Cnlist)
        return True

    def get_genuses(self, Cnumber, other=True):
        import lxml.html
        import requests
        import time
        genuses_list = []
        html = requests.get("http://kanaya.naist.jp/knapsack_jsp/information.jsp?word=" + Cnumber)
        time.sleep(1)
        dom = lxml.html.fromstring(html.text)
        for element in dom.xpath('//*[@class="org2"]'):
            genus2 = element.text.split()[0]
            if other:
                genuses_list.append(element.text.replace("\xa0", " ")[:-1])
            else:
                if genus2 == self.genus:
                    genuses_list.append(element.text.replace("\xa0", " ")[:-1])
        return genuses_list
