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
    string = string.upper()
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
    for each in product(*list_of_bins):
        bin_list.append(f"{'-'.join([*each])}")

    return bin_list, len(bin_list)


def get_bin_list_text(list_name):
    bin_list, total = create_bins_from_string(list_name)
    lst = ''
    for each in bin_list:
        lst += f'{each}\n'
    lst += f'Total= {total}\n'
    return lst

