
import requests
import lxml.html


def get_html(genus):
    """
    get htmlfile from KNApSAck search engine

    input
        genus: str, generic name

    output
        html: requests.models.Response
    """

    html = requests.get("http://kanaya.naist.jp/knapsack_jsp/result.jsp?sname=organism&word=" + genus)
    return html


def get_Cnumber(html, limit=30):
    """
    get Cnumber list from KNApSAck htmlfile

    input
        html: requests.models.Response
        limit: int, itertion limit

    output
        Cnumber: list, sorted list of Cnumber
    """

    dom = lxml.html.fromstring(html.text)
    i = 1
    Cnumber = set()
    genus = dom.xpath('//*[@id="my_contents"]/font[2]')[0].text
    genus = genus[0].upper() + genus[1:]
    while(True):
        if i > limit:
            print("max itertion")
            break

        try:
            Cn = dom.xpath('//*[@class="sortable d1"]/tr[' + str(i) + ']/td[1]/a')[0].text
        except IndexError:
            print("finish")
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


def main():
    genus = input()
    html = get_html(genus)
    Cnumber = get_Cnumber(html)
    # print(Cnumber)
    return Cnumber


if __name__ == '__main__':
    main()
