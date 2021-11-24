from createToken import *

global cnfList
cnfList = []

def LoadCNF(fn):
    file = open(fn).read()
    aturan = file.split('\n')
    
    for i in range(0, len(aturan),1):
        A = aturan[i].split(' -> ')
        cnfList.append(A)

    for i in range(0, len(cnfList),1):
        cnfList[i][1] = cnfList[i][1].split(' | ')
        a = 0
        for j in (cnfList[i][1]):
            cnfList[i][1][a] = j.replace(" ","")
            a += 1

def checkInCNFList(x):
    listForX = []
    for i in range(len(cnfList)):
        for j in cnfList[i][1]:
            if (j == x):
                listForX.append(cnfList[i][0])
    return listForX

def combine(a,b):
    l = []
    x = ''
    for i in (a):
        for j in (b):
            x = i + j
            l.append(x)
    return l

def CYK(token):
    LoadCNF("CNF.txt")
    cykTable= [[[] for i in range(j)]for j in range(len(token),-1,-1)]
    k = 1
    for i in range(len(token)):
        if (i == 0):
            for j in range(len(token)):
                l = checkInCNFList(token[j])
                cykTable[i][j] = l
        else:
            for j in range(len(token) - i):
                #print(f"Section i = {i}; j = {j}")
                set1 = []
                for cons in range(k):
                    a = cykTable[cons][j]
                    #print(f"a[{cons}][{j}] :",a)
                    b = cykTable[i-1-cons][j+cons+1]
                    #print(f"b[{i-1-cons}][{j+cons+1}] :",b)
                    tempL = combine(a,b)
                    #print("tempL : ",tempL)
                    for x in tempL:
                        l = checkInCNFList(x)
                        for y in l:
                            if (y != []):
                                set1.append(y)
                cykTable[i][j] = set1
            k += 1
    
    #Mengubah tabel of array menjadi tabel of set
    for i in range(len(token)):
        for j in range(len(token)-i):
            cykTable[i][j] = set(cykTable[i][j])

    # Menampilkan seluruh elemen cykTable
    #print("\nThis is CYK Table : ")
    #for i in (cykTable):
    #    print(i)
    return cykTable


def isSyntaxValid(table, startState):
    s = table[-2][0]
    for i in s:
        if (i == startState):
            return True
    return False
