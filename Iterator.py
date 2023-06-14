from itertools import product


#  number_list creates a list of numbers from a given range
def number_list(start='0', end='0', digits=2):
    num_list = list(range(int(start), int(end) + 1, 1))
    return list(map(lambda x: f"{x:0{digits}d}", num_list))


#  letter_list creates a list of letters from a range of letters
def letter_list(start, end):
    start = ord(start)
    end = ord(end)
    num_list = list(range(int(start), int(end) + 1, 1))
    return list(map(lambda x: chr(x), num_list))


#  given a string consisting of '-' for sections
#  and '...' or '…' for ranges will create a list of every combination
#  if dash is true it will remove all bt the first dash
#  if arrow is true will add down arrows before and after bins ending in 'A'
#  and up arrows for the rest.
#  if arrow_up is true they only get up arrows
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

#  If omit dashes removes all but first dash
#  also pieces back together the possible bin variations into a bin list
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

#  ADD arrows at end of each bin. 'A' indicates a down arrow, everything else gets an up arrow
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

    return bin_list


#  gets a bin list and breaks it up with new line and adds a total
def get_bin_list_text(bin_list):
    total = len(bin_list)
    lst = ''
    for each in bin_list:
        lst += f'{each}\n'
    lst += f'Total= {total}'
    return lst
