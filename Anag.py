from itertools import product


def number_list(start='0', end='0', digits=2):
    num_list = list(range(int(start), int(end) + 1, 1))
    return list(map(lambda x: f"{x:0{digits}d}", num_list))


def letter_list(start, end):
    start = ord(start)
    end = ord(end)
    num_list = list(range(int(start), int(end) + 1, 1))
    return list(map(lambda x: chr(x), num_list))


def create_bins_from_string(string, dash=True, arrow=False, arrow_up=False):
    omit_dashes = dash
    add_arrows = arrow
    arrows_up = arrow_up
    string = string.upper()
    split_string = string.split('-')
    list_of_bins = []
    for each in split_string:
        if '...' in each or '…' in each:
            if '...' in each:
                range_split = each.split('...', 1)
            else:
                range_split = each.split('…', 1)
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
    if omit_dashes and len(list_of_bins) >= 3:
        for each in product(*list_of_bins):
            each = list(each)
            _string = [each[0], each[1]]
            _string = ['-'.join([*_string])]
            each.pop(0)
            each.pop(0)
            _string.extend(each)
            bin_list.append(f"{''.join([*_string])}")
    else:
        for each in product(*list_of_bins):
            bin_list.append(f"{'-'.join([*each])}")

    #  ADD arrows at end of bin, 'A' indicates a down arrow, everything else gets an up arrow
    if add_arrows or arrows_up:
        for index, _each in enumerate(bin_list):
            _each = list(_each)
            if _each[-1] == 'A' and not arrows_up:
                _each.insert(0, '▼')
                _each.append('▼')
            else:
                _each.insert(0, '▲')
                _each.append('▲')
            bin_list[index] = "".join(_each)

    return bin_list, len(bin_list)


def get_bin_list_text(list_name, dash, arrow, arrow_up):
    bin_list, total = create_bins_from_string(list_name, dash, arrow, arrow_up)
    lst = ''
    for each in bin_list:
        lst += f'{each}\n'
    lst += f'Total= {total}\n'
    return lst

