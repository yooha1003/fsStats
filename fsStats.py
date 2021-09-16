#!/usr/bin/env python3
# import library
import pandas as pd
import numpy as np
import csv
import os
import argparse

## set ArgumentParser
parser = argparse.ArgumentParser(description='This is input args')
parser.add_argument('--subjid', required = True, help = ' ++ please input subject id (directory name)')
args = parser.parse_args()
sid = args.subjid

## set current working directory
curDir = os.getcwd()

## import dataset
asegDataDir = curDir + '/' + sid + '/stats/' + 'aseg.stats'
aparclhDataDir = curDir + '/' + sid + '/stats/' + 'lh.aparc.DKTatlas.stats'
aparcrhDataDir = curDir + '/' + sid + '/stats/' + 'rh.aparc.DKTatlas.stats'
#
def fsStat2pd(input):
    f = open(input, 'rt')
    reader = csv.reader(f)
    #
    csv_list = []
    for l in reader:
        csv_list.append(l)
    f.close()
    df = pd.DataFrame(csv_list)
    return df
# import raw data
asegRaw = fsStat2pd(asegDataDir)
aparclhRaw = fsStat2pd(aparclhDataDir)
aparcrhRaw = fsStat2pd(aparcrhDataDir)

# confirm starting index
asegInd = asegRaw[0][asegRaw[0] == '# NRows 45 '].index[0]
aparcInd = aparclhRaw[0][aparclhRaw[0] == '# ColHeaders StructName NumVert SurfArea GrayVol ThickAvg ThickStd MeanCurv GausCurv FoldInd CurvInd'].index[0]

## data resorting
asegData = asegRaw.iloc[asegInd+3:]
aparclhData =aparclhRaw.iloc[aparcInd+1:]
aparcrhData = aparcrhRaw.iloc[aparcInd+1:]
icv_ind = aparclhRaw[1][aparclhRaw[1] == ' BrainSegVol'].index[0]
icvVal = aparclhRaw.iloc[icv_ind, 3]
float(icvVal)
# convert to dataFrame
def fsValExt(data):
    res = []
    for i in range(data.shape[0]):
        tmp = data.iloc[i].str.split(' ')
        tmp_value = ' '.join(tmp[0]).split()
        df = res.append(tmp_value)
    res_df = pd.DataFrame(res)
    return res_df
aseg_df = fsValExt(asegData)
aparclh_df = fsValExt(aparclhData)
aparcrh_df = fsValExt(aparcrhData)
aparclh_df[3]
# add prefix
aparclh_df[0] = 'left' + aparclh_df[0].astype(str)
aparcrh_df[0] = 'right' + aparcrh_df[0].astype(str)
aseg_nvol = aseg_df[3].to_numpy(dtype=float) / float(icvVal) * 100 # P (normalized volume)
aseg_nvol_df = pd.DataFrame(aseg_nvol)
aparclh_nvol = aparclh_df[3].to_numpy(dtype=float) / float(icvVal) * 100 # P (normalized volume)
aparclh_nvol_df = pd.DataFrame(aparclh_nvol)
aparcrh_nvol = aparcrh_df[3].to_numpy(dtype=float) / float(icvVal) * 100 # P (normalized volume)
aparcrh_nvol_df = pd.DataFrame(aparcrh_nvol)

# aseg
aseg_stats = pd.concat([aseg_df[4], aseg_df[3], aseg_nvol_df], axis=1)
aseg_stats.columns = ['Region','V','P']
aseg_stats['T'] = 0
aseg_stats = aseg_stats[['Region','P','T','V']]

# aparc
aparclh_stats = pd.concat([aparclh_df[0], aparclh_nvol_df, aparclh_df[4],  aparclh_df[3]], axis=1)
aparclh_stats.columns = ['Region', 'P', 'T', 'V']
aparcrh_stats = pd.concat([aparcrh_df[0], aparcrh_nvol_df, aparcrh_df[4],  aparcrh_df[3]], axis=1)
aparcrh_stats.columns = ['Region', 'P', 'T', 'V']

# combine aseg+aparc
aseg_aparc_stats = pd.concat([aseg_stats,aparclh_stats,aparcrh_stats], axis=0).T
aseg_aparc_stats.to_csv(curDir + '/' + sid + '/' + sid + '_fs_stats.csv', header=False)
