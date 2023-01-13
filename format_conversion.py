# Reading an excel file using Python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.image as img
import warnings
import math as math
import sys
import argparse
import re


"""
x is the input fixed number which is of integer datatype
e is the number of fractional bits for example in Q1.15 e = 15
"""
def to_float(x):
    c = abs(x)
    sign = 1
    if x < 0:
        # convert back from two's complement
        c = x - 1
        c = ~c
        sign = -1
    f = (1.0 * c) / (2 ** 20)
    f = f * sign
    return f

# Function to convert Binary
# of Mantissa to float value.
def convertTofloat(value):
    # First bit will be sign bit.
    sign_bit = (value & 0x80000000) >> 31
    # Next 8 bits will be
    # Exponent Bits in Biased
    # form.
    exponent_bias = (value & 0x7F800000) >> 23

    # In 32 Bit format bias
    # value is 127 so to have
    # unbiased exponent
    # subtract 127.
    exponent_unbias = exponent_bias - 127

    # Next 23 Bits will be
    # Mantissa (1.M format)
    mantissa_arr = []
    mantissa_str = (value & 0x007FFFFF)
    power_count = -1
    sum = 0.0
    for i in range(23):
        sum += ((mantissa_str & 0x400000) >> 22) * pow(2, power_count)
        mantissa_str = mantissa_str << 1
        power_count -= 1
    sum += 1

    # The final real no. obtained
    # by sign bit, mantissa and
    # Exponent.
    real_no = pow(-1, sign_bit) * sum * pow(2, exponent_unbias)

    return round(real_no,12)

# warnings.filterwarnings('ignore')
# plt.Text("AAA")

parser = argparse.ArgumentParser(description ='Formating the csv output'
, formatter_class=argparse.RawDescriptionHelpFormatter
, epilog="""
Example:
python format_conversion.py --input powertrace_combined_Idle.csv --output mldata.csv --config "IA_C0_ANY:ieee754 AVG_NUM_CORES:ieee754"
python format_conversion.py --input powertrace_combined_Idle.csv --header "IA_C0_ANY AVG_NUM_CORES" --output mldata.csv --format ieee754
""")
parser.add_argument('--format', action='store', dest='format', help="define either ieee754 or 8.20 formatting")
parser.add_argument('--input', action='store', dest='input', required=True, help="Input filename")
parser.add_argument('--output', action='store', dest='output', default='output.csv', help="Output filename")
parser.add_argument('--header', action='store', dest='header', help="The header in the csv file to be converted")
parser.add_argument('--config', action='store', help="configuration for individual headers")

args = parser.parse_args()
# print(args.format)
# print(args.input)
# print(args.output)
# print(args.header)

header_list = []
header_format = {}

# Formating the headers
if (args.config is not None):
    print("config available")
    configs = re.split("\s+", args.config)
    for conf in configs:
        header_name, header_formatting = re.split("\:", conf)
        header_list.append(header_name)
        header_format[header_name] = header_formatting

# for a,b in header_format.items():  
#     print(a, "==", b)

if (args.header is not None):
    header_list = re.split('\s+', args.header)
    # for a in header_list:
    #     print(a)

df = pd.read_csv(args.input)

if (args.config is not None):
    print("converting")

    for header in header_list:
        c1 = []
        if (not header in df.columns):
            print("missing column header %s", header)
            exit(0)
        else:
            col_length = len(df[header])

        for i in range(col_length):
            if (not math.isnan(df[header][i])):
                value2 = int(df[header][i])
                if (header_format[header] == "ieee754"):
                    c1.append(convertTofloat(value2))
                elif (header_format[header] == "8.20"):
                    c1.append(to_float(value2))
            else:
                c1.append("")

        new_header = header + "_FLOAT"
        df[new_header] = c1

elif (args.format == "ieee754"):
    print("converting ieee754 format")
    for header in header_list:
        c1 = []
        if (not header in df.columns):
            print("missing column header %s", header)
            exit(0)
        else:
            col_length = len(df[header])

        for i in range(col_length):
            if (not math.isnan(df[header][i])):
                value2 = int(df[header][i])
                c1.append(convertTofloat(value2))
            else:
                c1.append("")

        new_header = header + "_FLOAT"
        df[new_header] = c1

elif (args.format == "8.20"):
    print("converting 8.20 format")
    for header in header_list:
        c1 = []
        if (not header in df.columns):
            print("missing column header %s", header)
            exit(0)
        else:
            col_length = len(df[header])

        for i in range(col_length):
            if (not math.isnan(df[header][i])):
                value2 = int(df[header][i])
                c1.append(to_float(value2))
            else:
                c1.append("")

        new_header = header + "_FLOAT"
        df[new_header] = c1
else:
    print("wrong format. Please use either 'ieee754' or '8.20'")
    exit(0)

print("writing output to: ", args.output)
df.to_csv(args.output)

