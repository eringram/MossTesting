#!/usr/bin/env python

import sys
import math
import numpy as np
import matplotlib.pyplot as plt
import itertools
import os


def computeMoments(dists):
    n = int(len(dists))
    m1 = 0.0
    m2 = 0.0
    m3 = 0.0
    m4 = 0.0
    mean = 0.0

    for i in range(n):
        mean = mean + dists[i]
    mean = mean / n

    centered_dists = dists - mean
    for i in range(n):
        m1 = m1 + centered_dists[i]
    m1 = m1 / n

    for i in range(n):
        m2 = m2 + (centered_dists[i] - m1) ** 2
        m3 = m3 + (centered_dists[i] - m1) ** 3
        m4 = m4 + (centered_dists[i] - m1) ** 4
    m2 = m2 / n
    m3 = m3 / n
    m4 = m4 / n
    m3 = m3 / (math.sqrt(m2)) ** 3
    m4 = m4 / (m2 ** 2)
    return [mean, m2, m3, m4]

def readCoords(filename):
    coords = []
    file = open(filename)
    for line in file:
        words = line.split()
        oneCoord = []
        for i in range(len(words)):
            oneCoord.append(float(words[i]))
        coords.append(oneCoord)
    file.close()
    return coords

def collectDataPoints():
    files = []
    for d in sorted(os.listdir(os.getcwd())):
        if os.path.isdir(d) and d.startswith("1"):
            os.chdir(d)
            for di in sorted(os.listdir(os.getcwd())):
                print(di)
                if os.path.isdir(di) and di.startswith("coord"):
                    # Now moving into the coords directory
                    os.chdir(di)
                    basepath = os.getcwd()
                    for f in sorted(os.listdir(os.getcwd())):
                        if os.path.isfile(f) and f.startswith("discs"):
                            files.append(basepath + "/" + f)
                    os.chdir("..")
            os.chdir("..")
    return files

def printMean(all_arr):
    avg_mean = 0.0
    avg_vari = 0.0
    avg_skew = 0.0
    avg_kurt = 0.0
    for i in range(0, len(all_y)):
        avg_mean += all_arr[i][0]
        avg_vari += all_arr[i][1]
        avg_skew += all_arr[i][2]
        avg_kurt += all_arr[i][3]

    avg_mean = avg_mean / len(all_arr)
    avg_vari = avg_vari / len(all_arr)
    avg_skew = avg_skew / len(all_arr)
    avg_kurt = avg_kurt / len(all_arr)
    print "avg_mean: ", avg_mean
    print "avg_vari: ", avg_vari
    print "avg_skew: ", avg_skew
    print "avg_kurt: ", avg_kurt



if __name__ == "__main__":
    files = collectDataPoints()
    all_y = []
    all_x = []
    
    for i in range(0, len(files)):
        coords = np.array(readCoords(files[i]))
        X = coords[:, 0]
        Y = coords[:, 1]
        mx = computeMoments(X)
        my = computeMoments(Y)
        all_y.append(my)
        all_x.append(mx)
#        coord_file_list = files[i].split("/")
#        coord_file_name = coord_file_list[len(coord_file_list) - 1]
    
    print "y averages: "
    printMean(all_y)
    print "\n ----- \n"
    print "x averages: "
    printMean(all_x)
