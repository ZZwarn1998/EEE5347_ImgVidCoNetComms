import copy
from collections import Counter
from heapq import heapify, heappush, heappop
from itertools import count
import copy
import six
import math
import os
import matplotlib.pyplot as plt
import csv


def getSymbolProbability(filepath):
    file = open(filepath,"r")
    raw_str = file.read()
    file.close()

    counter = Counter(raw_str)
    leng = sum(list(counter.values()))
    prb = []
    symbols = []
    frq = []
    entropy = 0

    for item in counter.items():
        symbols.append(item[0])
        prb.append(item[1]/leng)
        frq.append(item[1])
        entropy = entropy - item[1]/leng * math.log2(item[1]/leng)

    pro_item = ["Filepath", "Filesize", "CharNum ", "Entropy ", "Numspic "]
    pro_val = [filepath,
               str(os.path.getsize(filepath)) + " bytes" if os.path.getsize(filepath) > 1 else str(os.path.getsize(filepath)) + " byte",
               str(leng) + " pcs" if leng > 1 else str(leng) + " pc",
               "%.3f" % entropy + " bits" if entropy > 1 else "%.3f" % entropy + " bit",
               str(len(prb)) + " pcs" if len(prb) > 1 else str(len(prb)) + " pc"]
    info = dict(list(zip(pro_item, pro_val)))

    return symbols, prb, frq, info


def bulidTreeByHeapq(symbols, prb):
    num = count()
    prbs = list(zip(prb, num, symbols))
    trees = prbs
    heapify(trees)

    while(len(trees) > 1):
        prb1, _, sym1 = heappop(trees)
        prb2, _, sym2 = heappop(trees)
        heappush(trees, (prb1 + prb2, next(num),[sym1, sym2]))

    return trees[0][2]


def genemerateHaffC(trees, symbols, codewords, prefix):
    if len(trees) == 1:
        symbols.append(trees)
        codewords.append(copy.deepcopy(prefix))
        return
    else:
        for bit, branch in zip(['0','1'], trees):
            genemerateHaffC(branch, symbols, codewords, prefix + bit)
    return


def getHuffmanCode(symbols, prb):
    trees = bulidTreeByHeapq(symbols, prb)
    codewords = []
    symbols = []
    prefix = ""
    genemerateHaffC(trees, symbols, codewords, prefix)
    return symbols, codewords


def int_2_4bytes(num):
    byte_1 = six.int2byte(num & 255)
    num = num >> 8
    byte_2 = six.int2byte(num & 255)
    num = num >> 8
    byte_3 = six.int2byte(num & 255)
    num = num >> 8
    byte_4 = six.int2byte(num & 255)
    return byte_1, byte_2, byte_3, byte_4


def _4bytes_2_int(byte_1, byte_2, byte_3, byte_4):
    num = 0
    num = num | byte_4
    num = num << 8
    num = num | byte_3
    num = num << 8
    num = num | byte_2
    num = num << 8
    num = num | byte_1
    return num


def encode(codebook, frqbook, inpath, outpath):
    file = open(inpath, "r")
    raw_str = file.read()
    file.close()
    content = ""
    for char in raw_str:
        content = content + codebook[char]

    symbols_num = len(codebook.keys())
    byte_1, byte_2, byte_3, byte_4 = int_2_4bytes(symbols_num)

    file = open(outpath, 'wb')
    file.write(byte_1)
    file.write(byte_2)
    file.write(byte_3)
    file.write(byte_4)

    for item in frqbook.items():
        file.write(six.int2byte(ord(item[0])))
        byte_1, byte_2, byte_3, byte_4 = int_2_4bytes(item[1])
        file.write(byte_1)
        file.write(byte_2)
        file.write(byte_3)
        file.write(byte_4)

    while(len(content) > 8):
        out = 0
        for i in range(8):
            out = out << 1
            if content[i] == '1':
                out = out | 1
        content = content[8:]
        file.write(six.int2byte(out))
    out = 0
    for i in range(len(content)):
        out = out << 1
        if content[i] == '1':
            out = out | 1
    for i in range(8 - len(content)):
        out = out << 1
    file.write(six.int2byte(out))

    file.close()


def decode(path, outpath):
    file = open(path, 'rb')
    bdata = file.read()
    size = file.tell()
    file.close()
    sym_num = _4bytes_2_int(bdata[0], bdata[1], bdata[2], bdata[3])
    frq = []
    symbols = []
    global rev_codebook

    for i in range(sym_num):
        char = chr(bdata[4 + i * 5 + 0])
        byte1 = bdata[4 + i * 5 + 1]
        byte2 = bdata[4 + i * 5 + 2]
        byte3 = bdata[4 + i * 5 + 3]
        byte4 = bdata[4 + i * 5 + 4]
        pfrq = _4bytes_2_int(byte1, byte2, byte3, byte4)
        symbols.append(char)
        frq.append(pfrq)
    num = sum(frq)

    prb = [pfrq / num for pfrq in frq]

    if len(symbols) == 1:
        rev_codebook = dict(zip(['1'], symbols))
    else:
        sym , codewords = getHuffmanCode(symbols, prb)
        rev_codebook = dict(zip(codewords, sym))

    bdata = bdata[4 + sym_num * 5:]
    size -= (sym_num * 5 + 4)

    str = ""
    out = open(outpath, "w")
    for i in range(size):
        curbin = bdata[i]
        for j in range(8):
            if curbin & (1 << 7) == 0:
                str += "0"
            else:
                str += "1"
            curbin = curbin << 1

    stri = 0
    cnt_char = 0
    while(stri < len(str)):
        cur = str[stri]
        while(cur not in rev_codebook.keys()):
            stri += 1
            if stri < len(str):
                cur = cur + str[stri]
            else:
                break
        if stri < len(str) and cnt_char < num:
            out.write(rev_codebook[cur])
            stri += 1
            cnt_char += 1
        else:
            break
    out.close()


def plot_prob_distri(symbols, prb):
    x = range(len(symbols))
    symbol_prb = list(zip(symbols, prb))
    symbol_prb.sort(key = lambda x: -x[1])
    s = [item[0] for item in symbol_prb]
    p = [item[1] for item in symbol_prb]
    plt.bar(x, p)
    plt.xticks(x, s, rotation = 45, fontsize = "x-large", family= "fantasy")
    plt.yticks(fontsize = "xx-large", family= "fantasy")
    plt.ylabel("Probability", fontsize = "xx-large", family= "fantasy")
    plt.title("Probability Distribution", fontsize = "20", family= "fantasy")
    plt.show()


if __name__=="__main__":
    filepath =[".\\txtfile\\empty.txt",
               ".\\txtfile\\one.txt",
               ".\\txtfile\\paragraph_1.txt",
               ".\\txtfile\\paragraph_2.txt",
               ".\\txtfile\\paragraph_3.txt",
               ".\\txtfile\\Clinton's speech.txt",
               ".\\txtfile\\I have a dream.txt",
               ".\\txtfile\\Pearl Harbor Address to the Nation.txt",
               ".\\txtfile\\Share Our Wealth.txt"
               ]

    # change filepath
    path = filepath[5]

    outpath = ".\\compression\\"+ path.split('\\')[-1].split('.')[0] + "_compressed.txt"
    decomp_path = ".\\decompression\\" + path.split('\\')[-1].split('.')[0] + "_decompressed.txt"
    print(">" * 50)
    print("Start Analysing...")
    symbols, prb, frq, info = getSymbolProbability(path)
    print("Finish Analysing!")
    print(">" * 50)
    print("Property Manifest".center(50))
    print("|-"+"-"*46+"-|")
    for item in info.items():
        print(item[0]+":", item[1].center(40))

    global codebook

    print(">"*50)
    print("Generate Huffman Code".center(50))
    print("|-" + "-" * 46 + "-|")
    if len(symbols) == 0:
        print("This is an empty file. Please replace it with another file.")
    else:
        if len(symbols) == 1:
            codebook = dict(zip(symbols, ['1']))
        else:
            sym, codewords = getHuffmanCode(symbols, prb)
            codebook = dict(zip(sym, codewords))

        print("Symbol(ASCII)".center(25), "codeword".center(25))
        csvfile = open(".\\codebook\\"+ path.split('\\')[-1].split('.')[0] + "_path.csv",'w')
        csvw = csv.writer(csvfile)
        bitRate = 0
        frqbook = dict(zip(symbols, frq))
        prbbook = dict(zip(symbols, prb))
        for item in codebook.items():
            print(str(ord(item[0])).center(25),item[1].center(25))
            csvw.writerow([item[0],item[1]])
            bitRate += (len(item[1])*prbbook[item[0]])
        csvfile.close()
        print(">" * 50)

        # Encode
        print(("%-20s"%('Strating Encoding '+path.split('\\')[-1]+'...')))
        encode(codebook, frqbook, path, outpath)
        print("%-20s" % 'Finish Encoding!')
        print(">" * 50)
        print("Compression Manifest".center(50))
        print("|-" + "-" * 46 + "-|")
        print("Filesize(BEFORE) :", (str(os.path.getsize(path)) + " bytes").center(30) if os.path.getsize(path) > 1 else (str(os.path.getsize(path)) + " byte").center(30))
        print("Filesize(AFTER)  :",
              (str(os.path.getsize(outpath)) + " bytes").center(30) if os.path.getsize(outpath) > 1 else (str(os.path.getsize(outpath)) + " byte").center(30))
        print("Compression Ratio:", "{:.2%}".format(os.path.getsize(outpath)/os.path.getsize(path)).center(30))
        print("Average bit Rate: ", "%.3f".center(30)%(bitRate))
        print(">" * 50)

        # Decode
        print("%-20s"%('Strating Encoding '+path.split('\\')[-1]+'...'))
        decode(outpath, decomp_path)
        print("%-20s"%'Finishing Decoding!')

        # file = open(outpath,'rb')
        # data = file.read()
        # counter = Counter(data)
        # entropy = 0
        # summary = sum(counter.values())
        # for item in counter.items():
        #     entropy = entropy - (item[1] / summary) * math.log2(item[1] / summary)
        # print()
        # plot_prob_distri(symbols, prb)


