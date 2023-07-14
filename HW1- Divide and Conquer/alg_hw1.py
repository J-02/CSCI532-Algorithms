# -*- coding: utf-8 -*-
"""Alg.HW1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dkOD5nSlvhaTHaUM2o8-dSrYtdN5dwJK
"""

import numpy as np

"""O(n^2) naive"""

def naive(A,B):
    n = len(A)
    c = np.zeros([2*n])
    for a in range(n):
        for b in range(n):
            c[a+b] += (A[a]*B[b])
    return c

def divide(x, y):
    product = np.zeros(len(x) * 2)
    length = int(len(x))

    if length == 1:
        product[0] = x[0] * y[0]
        return product

    half = int(len(x) // 2)

    f1 = x[:half]
    s1 = x[half:]

    f2 = y[:half]
    s2 = y[half:]
#recursively until bascase
    one = divide(f1, f2)
    two = divide(s1, s2)
    three = divide(f1 + s1, f2 + s2)
# empty array to store middle products
    product_middle = np.empty(length)
    for i in range(0, length):
        product_middle[i] = three[i] - one[i] - two[i]

    for i in range(0, length):
        product[i] += one[i]
        product[i + length] += two[i]
        product[i + half] += product_middle[i]

    #print(product)
    return product

vector_size = 2500

A = np.random.randint(low=1, high=100, size=vector_size)
B = np.random.randint(low=1, high=100, size=vector_size)

# Commented out IPython magic to ensure Python compatibility.
# %%timeit
# naive(A,B)

"""Divide and conquer"""

# Commented out IPython magic to ensure Python compatibility.
# %%timeit
# divide(A,B)

n = 50
A = np.poly1d(np.random.randint(1, 100, n))
B = np.poly1d(np.random.randint(1, 100, n))

def DFT(a):
    n = a.o+1
    if n == 1: return a
    a0 = np.zeros(n)
    a1 = np.zeros(n)
    a0[::2] = a.coefficients[::2]
    a1[1::2] = a.coefficients[1::2]



C = A*B
print (C)


vector_size = 2048
poly1 = np.random.randint(low=1, high=100, size=vector_size)
poly2 = np.random.randint(low=1, high=100, size=vector_size)

def divide(x, y):

    #create array double length of x and initialize length variable
    multiply = np.zeros(len(x) * 2)
    length = int(len(x))

    #base case add product of x and y polynomials to multiply array
    if length == 1:
        multiply[0] = x[0] * y[0]
        return multiply

    #initialize half variable
    half = int(len(x) // 2)

    #split arrays into two halfs each
    f1 = x[:half]
    s1 = x[half:]

    f2 = y[:half]
    s2 = y[half:]

    #3 recursive step to divide until base case then multiply first halfs, second halfs
    #and both
    one = divide(f1, f2)
    two = divide(s1, s2)
    three = divide(f1 + s1, f2 + s2)

    #get the middle array to be the three - one - two
    middle = np.empty(length)
    for i in range(0, length):
        middle[i] = three[i] - one[i] - two[i]

    #fill product array with one in first half, two in second half of product,
    #and add middle to middle portion
    for i in range(0, length):
        multiply[i] += one[i]
        multiply[i + length] += two[i]
        multiply[i + half] += middle[i]

    return multiply

output = divide(poly1, poly2)
print(output)
print(np.polymul(poly1,poly2))

def naive(A,B):
    n = len(A)
    c = np.zeros([2*n])
    for a in range(n):
        for b in range(n):
            c[a+b] += (A[a]*B[b])
    return c

print(naive(poly1,poly2))