# Windows Disk Space Checker Script
# Py Version:   Python 3.4 
# Author:       Kevin Bridges
# Github:       https://github.com/dickeymoe/DiskSpaceChecker
# External Packages Required:
#       pip install pypiwin32
#       pip install wmi

import os, sys, time, argparse
import wmi
import math

from sys import argv

class Disk_Object():
    def __init__(self):
        self.Name = ""
        self.SystemName = ""
        self.VolumeName = ""
        self.Caption = ""
        self.FreeSpace = ""
        self.Size = ""
        self.DriveType = ""
        self.used_spaceGB = ""
        self.percent_filled = ""
        self.SizeGB = ""
        self.FreeSpaceGB = ""
   
def get_disk_space_percent(fs, ts):
    used_spaceGB = ts - fs
    percent_filled = "{0:.0f}%".format(used_spaceGB / ts * 100)
    return percent_filled

def disk_check(argv):
    c = wmi.WMI()
    this_count = 0
    for d in c.Win32_LogicalDisk():
        procede_with_disk_check = False
        this_count += 1
        cdobj = construct_disk_object(this_count, d)
        targ = argv.upper()+":"
        if cdobj.Caption == targ:
            procede_with_disk_check = True
        if procede_with_disk_check == True:
            return cdobj
    print("Disk Check Complete")

def construct_disk_object(count, d):
    disk = Disk_Object
    if d.DriveType == 3:
            dobj = disk()
            dobj.Name = "dobj"+str(count)
            dobj.SystemName = d.SystemName
            dobj.VolumeName = d.VolumeName
            dobj.Caption = d.Caption
            dobj.FreeSpace = d.FreeSpace
            dobj.Size = d.Size
            dobj.DriveType = d.DriveType
            dobj.FreeSpaceGB = convertSize(float(dobj.FreeSpace))
            dobj.SizeGB = convertSize(float(dobj.Size))
            dobj.percent_filled = get_disk_space_percent(dobj.FreeSpaceGB, dobj.SizeGB)
            return dobj

def convertSize(size):
   if (size == 0):
       return '0B'
   i = int(math.floor(math.log(size,1024)))
   p = math.pow(1024,i)
   s = round(size/p,2)
   return (s)

def main(argv):
    fdobj = disk_check(argv)
    print("Hostname       : " + fdobj.SystemName)
    print("Drive Letter   : " + fdobj.Caption)
    print("Total Size     : " + str(fdobj.SizeGB) + " GB")
    print("Free Space     : " + str(fdobj.FreeSpaceGB) + " GB")
    print("Percent Filled : " + fdobj.percent_filled)

if __name__ == '__main__':
    main(sys.argv[1])
    
