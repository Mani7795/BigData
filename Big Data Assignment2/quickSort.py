# -*- coding: utf-8 -*-
"""
Created on Tue May 16 14:01:22 2023

@author: mani
"""

def quickSort(lst):
    if len(lst)<=1:
        return lst
    else:
        pivot = lst[0]
        left =[]
        right=[]
        for i in range (1,len(lst)):
            if lst[i]<pivot:
                left.append(lst[i])
            else:
                right.append(lst[i])
        return quickSort(left) +[pivot] + quickSort(right)

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        left = []
        right = []
        for i in range(1, len(arr)):
            if arr[i] < pivot:
                left.append(arr[i])
            else:
                right.append(arr[i])
        return quicksort(left) + [pivot] + quicksort(right)      
arr = [5,1,4,73,3,2,0]
print(quickSort(arr))
            
    