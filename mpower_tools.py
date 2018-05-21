import matplotlib.pyplot as plt
import numpy as np
import sys
import getopt
import re
import time
import copy
import xlsxwriter as xlw

from dateutil import parser

KEY_WORDS_PATTERN = {
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

KEY_WORDS_VALUE = {
    "time":     "1900-1-1 0:0:0",
    "chgtyp":   "unknown",
    "cc":       0,
    "icl":      0,
    "brdtmp":   0.0,
    "petyp":    "unknown",
    "vbus":     0,
    "ulmt":     0,
    "scrn":     0,
    "fstchg":   0,
    "usoc":     0,
    "tsoc":     0,
    "battmp":   0.0,
    "vbat":     0,
    "ibat":     0,
    "usbtmp":   0.0,
    "usbvltg":  0,
    "dischg":   0,
    "plg":      0
}

INT_KEY_WORDS = (
    "cc",       "icl",      "vbus",     "ulmt",     "scrn",
    "fstchg",   "usoc",     "tsoc",     "vbat",     "ibat",
    "usbvltg",  "dischg"
)

FLT_KEY_WORDS = (
    "brdtmp",   "battmp",   "usbtmp"
)

STR_KEY_WORDS = (
    "chgtyp",   "petyp"
)

SPC_KEY_WORDS = (
    "plg",      "time"
)

ORDERED_KEY_WORDS = (
    "time",     "plg" ,     "chgtyp",   "petyp",
    "brdtmp",   "battmp",   "usbtmp",
    "cc",       "icl",      "ulmt",     "scrn",     "dischg",
    "fstchg",   "usoc",     "tsoc",     "vbat",     "ibat",
    "usbvltg"
)


def parse(path):
    global KEY_WORDS_PATTERN
    global KEY_WORDS_VALUE

    key_words_val_cur = copy.deepcopy(KEY_WORDS_VALUE)
    key_words_val_ser = []

    pattern_compiled = {}
    for key_word in KEY_WORDS_PATTERN:
        pattern_compiled[key_word] = re.compile(KEY_WORDS_PATTERN[key_word])

    with open(path, "r") as log:
        for line in log:
            # valid log
            if pattern_compiled["flag"].match(line):
                # parse the tag type
                tag_type = "unknown"
                if pattern_compiled["chg"].match(line):
                    tag_type = "chg"
                elif pattern_compiled["fg"].match(line):
                    tag_type = "fg"
                elif pattern_compiled["usb"].match(line):
                    tag_type = "usb"
                else:
                    continue

                # parse all the tag
                for key_word in INT_KEY_WORDS:
                    match = pattern_compiled[key_word].match(line)
                    if match:
                        key_words_val_cur[key_word] = int(match.group(1))
                for key_word in FLT_KEY_WORDS:
                    match = pattern_compiled[key_word].match(line)
                    if match:
                        key_words_val_cur[key_word] = float(match.group(1))
                for key_word in STR_KEY_WORDS:
                    match = pattern_compiled[key_word].match(line)
                    if match:
                        key_words_val_cur[key_word] = match.group(1)
                for key_word in SPC_KEY_WORDS:
                    match = pattern_compiled[key_word].match(line)
                    if match:
                        if key_word == "plg":
                            if match.group(1) == "in":
                                key_words_val_cur[key_word] = 1
                            elif match.group(1) == "out":
                                key_words_val_cur[key_word] = 0
                        elif key_word == "time":
                            # key_words_val_cur["time"] = parser.parse(match.group(1))
                            key_words_val_cur["time"] = match.group(1)

                key_words_val_ser.append(key_words_val_cur)
                key_words_val_cur = copy.deepcopy(key_words_val_ser[-1])

    return key_words_val_ser

def save_to_xls(val_ser, filename):
    workbook = xlw.Workbook(filename)
    worksheet = workbook.add_worksheet()
    worksheet.write_row(0, 0, ORDERED_KEY_WORDS)
    row = 1
    for val in val_ser:
        col = 0
        for key_word in ORDERED_KEY_WORDS:
            worksheet.write(row, col, dict(val)[key_word])
            col += 1
        row += 1
    workbook.close()

# 4test
def plot_key_words_value(values):
    y = []
    for value in values:
        y.append(value["time"])
    x = range(len(y))
    plt.plot(x, y)
    plt.show()

# 4test
def plot_key_words_value2(values):
    y = []
    x = []
    for value in values:
        x.append(value["time"])
        y.append(value["vbat"])
    plt.plot(x, y)
    plt.show()

def help():
    help_msg = (
        "usage: python mpower_tools.py logname [options]\n"
        "option:\n"
        "   -h                  print help message\n"
        "       --help\n"
        "   -o <filename>       the excel file save to\n"
        "       --output\n"
        "   -p <curvename>      plot the given curve\n"
        "       --plot\n"
    )
    print(help_msg)

#under dev
def main():
    log_path = ""
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvl:o:",
            ["help", "version", "log", "output"])
    except getopt.GetoptError:
        help()
        sys.exit(0)
    for opt, arg in opts:
        if opt == "-h":
            help()
            exit(0)
        elif opt in ("-v", "--version"):
            print("version: v0.1")
        elif opt in ("-l", "--log"):
            log_path = arg
    val_ser = parse(log_path)
    save_to_xls(val_ser, "/home/weipeng/pro/chargerTest/chargerTest/output.xlsx")

if __name__ == "__main__":
    main()

