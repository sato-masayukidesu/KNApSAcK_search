
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
                    if int(line[i+1:]) < limit:
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
                    if int(line[i+1:]) < limit:
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
                    if int(line[i+1:]) < limit:
                        break
                    # print(line)
                    f2.write(line)


def main():
    split("my_kcfs2count.txt")


if __name__ == '__main__':
    main()
