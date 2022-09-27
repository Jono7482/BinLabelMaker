####################################
# Ascending Number Array Generator #
####################################

# Creates an array of numbers as strings given a start number and end number
# 2 digit adds a 0 before the numbers 1-9 Ex. 01, 02
# 3 digit adds 2 0's for numbers 1-9 and 1 0 for numbers 10-99
def make_list(start='0', end='0', digits=2):
    num_list = []
    start = int(start)
    list_length = int(end) - int(start)
    while list_length >= 0:
        if start <= 9 and digits == 2:
            num_list.append('0' + str(start))
        elif 99 >= start >= 10 and digits == 3:
            num_list.append('0' + str(start))
        elif start <= 9 and digits == 3:
            num_list.append('00' + str(start))
        else:
            num_list.append(str(start))
        start = start + 1
        list_length = list_length - 1
    return num_list


def letter_list(input_string=('A', )):
    string_array = []
    for each in input_string:
        string_array.append(each)
    return string_array


# Create the lists of Aisles Sections, Bins, and Positions
def get_bin_list(astart='1', aend='4', sec=('A', ), bstart='1', bend='1', pos=('A', ), digits=2):
    aisles = make_list(start=astart, end=aend, digits=digits)
    sections = (letter_list(sec))
    bins = make_list(start=bstart, end=bend, digits=digits)
    positions = (letter_list(pos))

    # Create the bin array
    total = 0
    bin_list = []
    for aisle in aisles:
        for section in sections:
            for a_bin in bins:
                for pos in positions:
                    bin_list.append(f'{aisle}-{section}-{a_bin}-{pos}')
                    total = total + 1
    return bin_list


