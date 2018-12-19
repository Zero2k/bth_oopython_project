#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Binary Search
"""

def binary_search(arr_list, target):
    """ Binary Search for Array List """
    start = 0
    end = len(arr_list) - 1

    while start <= end:
        middle = (start + end) // 2
        midpoint = arr_list[middle]

        if midpoint.name > target:
            end = middle - 1

        elif midpoint.name < target:
            start = middle + 1

        else:
            return [midpoint]
