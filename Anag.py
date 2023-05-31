from itertools import product

def number_list(start='0', end='0', digits=2):
    num_list = list(range(int(start), int(end) + 1, 1))
    return list(map(lambda x: f"{x:0{digits}d}", num_list))


def letter_list(start, end):
    start = ord(start)
    end = ord(end)
    num_list = list(range(int(start), int(end) + 1, 1))
    return list(map(lambda x: chr(x), num_list))


def create_bins_from_string(string):
    add_arrows = False
    string = string.upper()
    # Tests last char of string for a 'V' if v exists program will add arrows
    if string[-1] == 'V':
        add_arrows = True
    split_string = string.split('-')
    list_of_bins = []
    for each in split_string:

        if '...' in each:
            range_split = each.split('...', 1)
            if range_split[0].isalpha() and range_split[1].isalpha():
                alpha = (letter_list(range_split[0], range_split[1]))
                list_of_bins.append(alpha)
            elif range_split[0].isnumeric() and range_split[1].isnumeric():
                num = (number_list(range_split[0], range_split[1]))
                list_of_bins.append(num)
            else:
                print('>>> Usage of "..." must be between numbers OR letters for creating a range')
        else:
            list_of_bins.append([each])

    bin_list = []
    bin_listTemp = []
    for each in product(*list_of_bins):
        print(f"list of bins = {list_of_bins}")
        print(f"for each in product list of bins each = {each}")

        tempstring = list(each)
        print(f'tempstring = each = {tempstring}')
        tempstring2 = [tempstring[0], tempstring[1]]
        print(f"tempstring2 = {tempstring2}")
        tempstring2 = ['-'.join([*tempstring2])]
        print(f"tempstring2 after join = {tempstring2}")
        print(f"tempstring before pop = {tempstring}")
        tempstring.pop(0)
        print(f"tempstring after pop1 = {tempstring}")
        tempstring.pop(0)
        print(f"tempstring after pop2 = {tempstring}")
        # tempstring = ''.join([*tempstring])
        # print(f"tempstring after .join {tempstring}")
        tempstring2.extend(tempstring)
        print(f"tempstring2 after append tempstring  = {tempstring2}")

        print(f"Tempstring = {tempstring}")
        bin_listTemp.append(f"{''.join([*tempstring2])}")
        print(f"Binlisttemp= {bin_listTemp}")
        bin_list.append(f"{'-'.join([*each])}")
        print(f"binlist = {bin_list}\n")
    bin_list = bin_listTemp
    #  ADD arrows in place of 'V' at end of bin 'A' indicates a down arrow, everything else gets an up arrow
    if add_arrows:
        for index, _each in enumerate(bin_list):
            _each = list(_each)
            if _each[-3] == 'A':
                _each[-1] = '▼'
            else:
                _each[-1] = '▲'
            bin_list[index] = "".join(_each)

    return bin_list, len(bin_list)


def get_bin_list_text(list_name):
    bin_list, total = create_bins_from_string(list_name)
    lst = ''
    for each in bin_list:
        lst += f'{each}\n'
    lst += f'Total= {total}\n'
    return lst

