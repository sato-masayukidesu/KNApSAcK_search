
class MCS_Finder(object):
    def __init__(self, genus, path=None):
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
        import networkx as nx

        self.genus = genus
        self.mol_list = None
        if path is None:
            self.path = self.genus
        else:
            self.path = path + "/" + self.genus
        self.hanni = self.get_range()

        if not os.path.exists(self.path):
            os.mkdir(self.path)


    def get_range(self):
        hanni = []
        for i in range(1, 52):
            page = str(i)
            with open("../../../database/knapsack-kcf/KNApSAck" + page + ".kcf")as f1:
                clist = f1.read().split()
                hanni.append(clist[1])
        return hanni


    def get_html(self, genus):
        """
        get htmlfile from KNApSAck search engine

        input
            genus: str, genusric name

        output
            html: requests.models.Response
        """
        import requests
        html = requests.get("http://kanaya.naist.jp/knapsack_jsp/result.jsp?sname=organism&word=" + genus, 60)
        return html


    def get_urltxt(self, genus, update):
        import requests
        import os
        if not update:
            if os.path.exists(self.path + "/url.txt"):
                print("pass")
                return True
        html = requests.get("http://kanaya.naist.jp/knapsack_jsp/result.jsp?sname=organism&word=" + genus, 60)
        with open(self.path + "/url.txt", "w")as f:
            f.write(html.text)
        return True


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
                if genus != str(dom.xpath('//*[@class="sortable d1"]/tr[' + str(i) + ']/td[6]')[0].text_content()).split()[0]:
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


    def get_Cnumber2(self, txt, limit=2000):
        """
        get Cnumber list from KNApSAck htmlfile

        input
            html: requests.models.Response
            limit: int, itertion limit

        output
            Cnumber: list, sorted list of Cnumber
        """
        import lxml.html
        dom = lxml.html.fromstring(txt)
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
                if genus != str(dom.xpath('//*[@class="sortable d1"]/tr[' + str(i) + ']/td[6]')[0].text_content()).split()[0]:
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
            filename = self.path + "/kcfs.kcfs"
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
        if html.status_code != 200:
            raise Exception
        print("get html " + self.genus)
        Cnumber = self.get_Cnumber(html, limit)
        if Cnumber == []:
            return False
        self.search(Cnumber)
        self.kcfs2count(self.path + "/kcfs.kcfs", self.path + "/kcfscount.txt")
        self.split(self.path + "/kcfscount.txt", self.path + "/splitedcount.txt", splimit)
        return True


    def make_kcfs2(self, limit=2000, splimit=0, update=False):
        self.get_urltxt(self.genus, update)
        with open(self.path + "/urltext.txt")as fi:
            text = fi.read()
        Cnumber = self.get_Cnumber2(text, limit)
        if Cnumber == []:
            return False
        self.search(Cnumber)
        self.kcfs2count(self.path + "/kcfs.kcfs", self.path + "/kcfscount.txt")
        self.split(self.path + "/kcfscount.txt", self.path + "/splitedcount.txt", splimit)
        return True


    def gCfl(self, label):
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
        query += "\s"
        query = "\s" + query
        with open(self.path + "/kcfs.kcfs")as f:
            file = f.read()
            molecule = file.split("///\n")
            Cnlist = []
            for mole in molecule:
                if re.search(query, mole) is not None:
                    Cn = mole.split("\n")[0].split()[1]
                    Cnlist.append(Cn)
        return Cnlist


    def get_genuses(self, Cnumber, other=True):
        import lxml.html
        import requests
        import time
        genuses_list = []
        html = requests.get("http://kanaya.naist.jp/knapsack_jsp/information.jsp?word=" + Cnumber, 60)
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


    def get_name(self, Cnumber):
        import requests
        import lxml.html
        html = requests.get("http://kanaya.naist.jp/knapsack_jsp/information.jsp?word=" + Cnumber, 60)
        dom = lxml.html.fromstring(html.text)
        name = dom.xpath('//*[@id="my_contents"]/table/tr[2]/td[1]/table/tr[1]/td')[0].text
        return name



class control_all_genus(object):
    def __init__(self, path):
        import os
        self.path = path
        self.ari = self.get_having_list()
        self.allkcfs = None


    def get_having_list(self):
        import os

        ari = []
        for genus in os.listdir(self.path):
            if genus == ".DS_Store" or genus == "others" or genus == "genuses.pickle":
                continue
            elif os.listdir(self.path + "/" + genus) == []:
                continue
            else:
                ari.append(genus)
        return ari


    def get_number_of_Cnumber(self):
        import os

        kosuu = dict()
        for genus in self.ari:
            if genus == ".DS_Store" or genus == "others":
                continue
            with open(self.path + "/" + genus + "/kcfs.kcfs")as f:
                Cnlist = []
                molecule = f.read().split("///\n")
                for mol in molecule[:-1]:
                    Cn = mol.split("\n")[0].split()[1]
                    Cnlist.append(Cn)
                    kosuu[Cn] = kosuu.get(Cn, 0) + 1
        return kosuu


    def get_all_kcfs(self):
        import os

        kosuu = dict()
        for genus in self.ari:
            if genus == ".DS_Store" or genus == "others":
                continue
            with open(self.path + "/" + genus + "/kcfscount.txt")as f:
                units = f.read().split("\n")
                for unit in units[:-1]:
                    temp = unit.split()
                    kosuu[(temp[1], temp[2])] = kosuu.get((temp[1], temp[2]),0) + int(temp[3])
        return kosuu


    def get_split_kcfs(self):
        import os

        kosuu = dict()
        for genus in self.ari:
            with open(self.path + "/" + genus + "/splitedcount.txt")as f:
                units = f.read().split("\n")
                for unit in units[:-1]:
                    temp = unit.split()
                    kosuu[(temp[1], temp[2])] = kosuu.get((temp[1], temp[2]),0) + int(temp[3])
        return kosuu


    def get_Cnumber_from_label(self, label):
        import os

        Cn_in_genus = dict()
        for genus in self.ari:
            Cnlist = self.gCfl(genus, label)
            if Cnlist != []:
                Cn_in_genus[genus] = Cnlist
        return Cn_in_genus


    def get_specifics(self):
        if self.allkcfs is None:
            self.allkcfs = self.get_all_kcfs()
        only = dict()
        for genus in self.ari:
            with open(self.path + "/" + genus + "/kcfscount.txt")as f:
                units = f.read().split("\n")
                for unit in units[:-1]:
                    temp = unit.split()
                    if self.allkcfs[(temp[1], temp[2])] == int(temp[3]):
                        only[(temp[1], temp[2])] = (int(temp[3]), genus)
        return only


    def gCfl(self, genus, label):
        import re
        path = self.path + "/" + genus
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
        query += "\s"
        query = "\s" + query
        with open(path + "/kcfs.kcfs")as f:
            file = f.read()
            molecule = file.split("///\n")
            Cnlist = []
            for mole in molecule:
                if re.search(query, mole) is not None:
                    Cn = mole.split("\n")[0].split()[1]
                    Cnlist.append(Cn)
        return Cnlist
