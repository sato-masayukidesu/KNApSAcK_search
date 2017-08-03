
import sys
import re


def kcfs2count(kcfs, txt):
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


def main():
    kcfs2count(sys.argv[1], sys.argv[2])
    # kcfs2count("test.kcfs", "kcf2count.txt")


if __name__ == '__main__':
    main()
