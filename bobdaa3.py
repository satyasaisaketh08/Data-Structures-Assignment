import numpy as np
import heapq
from collections import defaultdict
from collections import Counter
log1 = open("encrypt1.txt")
log2 = open("encrypt2.txt")
data1 = log1.read()
data2 = log2.read()
split_it1 = data1.split()
split_it2 = data2.split()

Counter1 = Counter(split_it1)
Counter2 = Counter(split_it2)
Counter1 += Counter2

freoc = Counter1.most_common(3)

print("The most frequently occuring 3 words after going through the two log files  are: ")
print(freoc)
print("                        |                      ")
print("                        |                      ")

#***********Finding the string representing the longest common subsequence ***********

def lcs(str1, str2):
    a = len(str1)
    b = len(str2)
    string_matrix = [[0 for i in range(b+1)] for i in range(a+1)]   
    for i in range(1, a+1):
        for j in range(1, b+1):
            if i == 0 or j == 0:
                string_matrix[i][j] = 0
            elif str1[i-1] == str2[j-1]:
                string_matrix[i][j] = 1 + string_matrix[i-1][j-1]
            else:
                string_matrix[i][j] = max(string_matrix[i-1][j], string_matrix[i][j-1])
    index = string_matrix[a][b]
    res = [""] * index
    i = a
    j = b
    while i > 0 and j > 0:
        if str1[i-1] == str2[j-1]:
            res[index-1] = str1[i-1]
            i -= 1
            j -= 1
            index -= 1
        elif string_matrix[i-1][j] > string_matrix[i][j-1]:
            i -= 1
        else:
            j -= 1
    return res
    
str1 = freoc[0][0] + freoc[1][0]
str2 = freoc[1][0] + freoc[2][0]
str3 = freoc[2][0] + freoc[0][0]
lcstring1 = ''.join(lcs(str1, str2))
lcstring2 = ''.join(lcs(lcstring1, str3))
print("Length of least common subsequence is:", len(lcstring2),"\n The common subsequence is:", lcstring2)
    
    #Optimal encoding of the longest common subsequence
    

def encode(frequency):
    heap = [[weight, [symbol, '']] for symbol, weight in frequency.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))


data = lcstring2
frequency = defaultdict(int)
for symbol in data:
    frequency[symbol] += 1

huff = encode(frequency)
print ("Character".ljust(10) + "Weight".ljust(10) + "Huffman Code")
for p in huff:
    print (p[0].ljust(10) + str(frequency[p[0]]).ljust(10) + p[1])

keystring=''    
for char in data :
    for p in huff:
        if char==p[0] :
            keystring+=p[1]
    
print("The required password(key) is: "+ keystring)