import matplotlib.pyplot as plt
import numpy as np
import sys
import getopt
import re
import time
import copy

from dateutil import parser

keyWordsMap = {
    "time":     "^\[(.*?)\].*",
    "flag":     ".*\[mpower\].*",
    "chg":      ".*\[charger\].*",
    "plg":      ".*<plug_(.*?)>.*",
    "chgtyp":   ".*<chr_type=(.*?)>.*",
    "cc":       ".*<setting_battery_current=(\d+?)uA>.*",
    "icl":      ".*<setting_input_current=(\d+?)uA>.*",
    "brdtmp":   ".*<board_temp=(\d+?)degree>.*",
    "petyp":    ".*<protocol_type=(.*?)>.*",
    "vbus":     ".*<vbus=(\d*?)uV>.*",
    "ulmt":     ".*<is_usb_unlimited=(\d)>.*",
    "scrn":     ".*<is_screen_on=(\d)>.*",
    "fstchg":   ".*<is_supported_fastcharging=(\d)>.*",
    "fg":       ".*\[fuelgauge\].*",
    "usoc":     ".*<ui_soc=(\d{1,3})%>.*",
    "tsoc":     ".*<true_soc=(\d{1,3})%>.*",
    "battmp":   ".*<battery_temp=(-?\d{1,3}\.?\d{1,2})degree>.*",
    "vbat":     ".*<vbat=(\d{1,7})uV>.*",
    "ibat":     ".*<ibat=(\d{1,7})uA>.*",
    "usb":      ".*\[usb_thermal\].*",
    "usbtmp":   ".*<temp=(\d+?\.?\d+?)degree>.*",
    "usbvltg":  ".*<voltage=(\d+?)uV>.*",
    "dischg":   ".*<is_disable_charge=(\d)>.*"
}

class ChargerState:
    "represent charge state at one moment"
    time = parser.parse("1900-1-1 00:00:00")
    chgtyp = "unknown"
    cc = 0
    icl = 0
    brdtmp = 0
    petyp = "unknown"
    vbus = 0
    ulmt = 0
    scrn = 0
    fstchg = 0
    usoc = 0
    tsoc = 0
    battmp = 0
    vbat = 0
    ibat = 0
    usbtmp = 0
    usbvltg = 0
    dischg = 0
    plg = 0

def parse(path):
    global keyWordsMap
    chgStatCur = ChargerState()
    chgStatPre = [chgStatCur]
    with open(path, "r") as log:
        for line in log:
            # valid log
            if re.match(keyWordsMap["flag"], line):
                # parse the tag type
                tagType = "unknown"
                if re.match(keyWordsMap["chg"], line):
                   tagType = "chg"
                elif re.match(keyWordsMap["fg"], line):
                    tagType = "fg"
                elif re.match(keyWordsMap["usb"], line):
                    tagType = "usb"
                # parse the tag
                for keyWord in keyWordsMap:
                    # print(keyWord)
                    match = re.match(keyWordsMap[keyWord], line)
                    if match:
                        # for debug
                        # if keyWord != "flag" and keyWord != "fg" and keyWord != "chg" and keyWord != "usb":
                        #     print(match.group(1))
                        # parse all key words
                        if keyWord == "time":
                            chgStatCur.time = parser.parse(match.group(1))
                        elif keyWord == "plg":
                            if match.group(1) == "in":
                                chgStatCur.plg = 1
                            elif match.group(1) == "out":
                                chgStatCur.plg = 0
                        elif keyWord == "chgtyp":
                            chgStatCur.chgtyp = match.group(1)
                        elif keyWord == "cc":
                            chgStatCur.cc = int(match.group(1))
                        elif keyWord == "icl":
                            chgStatCur.icl = int(match.group(1))
                        elif keyWord == "brdtmp":
                            chgStatCur.brdtmp = float(match.group(1))
                        elif keyWord == "petyp":
                            chgStatCur.petyp = match.group(1)
                        elif keyWord == "vbus":
                            chgStatCur.vbus = int(match.group(1))
                        elif keyWord == "ulmt":
                            chgStatCur.ulmt = int(match.group(1))
                        elif keyWord == "scrn":
                            chgStatCur.scrn = int(match.group(1))
                        elif keyWord == "fstchg":
                            chgStatCur.fstchg = int(match.group(1))
                        elif keyWord == "usoc":
                            chgStatCur.usoc = int(match.group(1))
                        elif keyWord == "tsoc":
                            chgStatCur.tsoc = int(match.group(1))
                        elif keyWord == "battmp":
                            chgStatCur.battmp = float(match.group(1))
                        elif keyWord == "vbat":
                            chgStatCur.vbat = int(match.group(1))
                        elif keyWord == "ibat":
                            chgStatCur.ibat = int(match.group(1))
                        elif keyWord == "usbtmp":
                            chgStatCur.usbtmp = float(match.group(1))
                        elif keyWord == "usbvltg":
                            chgStatCur.usbvltg = int(match.group(1))
                        elif keyWord == "dischg":
                            chgStatCur.dischg = int(match.group(1))
                chgStatPre.append(chgStatCur)
                chgStatCur = copy.copy(chgStatPre[-1])
        return chgStatPre

# under dev
def plotChgStatSeries(chgStatSeries):
    y = []
    for chgStat in chgStatSeries:
        y.append(chgStat.vbat)
    x = range(len(y))
    plt.plot(x, y)
    plt.show()


def main():
    logPath = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hl:v", ["help", "log", "version"])
    except getopt.GetoptError:
        print("usage: mpower_tools -l <log_path>")
        sys.exit(0)
    for opt, arg in opts:
        if opt == "-h":
            print("usage: mpower_tools -l <log_path>")
        elif opt in ("-v", "--version"):
            print("version: v0.1")
        elif opt in ("-l", "--log"):
            logPath = arg
    chgStatSeries = parse(logPath)
    plotChgStatSeries(chgStatSeries)


if __name__ == "__main__":
    main()

