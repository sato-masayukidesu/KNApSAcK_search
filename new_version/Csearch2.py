

def search(Cnumberlist, filename="test.kcfs"):
    "make kcffile only given Cnumbers from all kcffile"
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

        with open("../../../作業場/kcfs/KNApSAck" + page + ".kcfs") as f:
            for (i, line) in enumerate(f):
                # print(line[12:21]) # C00000000
                if line[12:21] == Cnumber:
                    # temp = i
                    # print("find", temp)
                    lin = line
                    flag = 0
                    with open(filename, "a") as fw:
                        while(lin[:5] != "ENTRY" or flag != 1):
                            flag = 1
                            fw.write(lin)
                            lin = f.readline()
                        else:
                            break


def main(Clist):
    # Clist = input()
    search(Clist)


if __name__ == "__main__":
    main(['C00000730', 'C00000733', 'C00000734'])
