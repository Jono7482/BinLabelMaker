
def number_list(start='0', end='0', digits=2):
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


def letter_list(start, end):
    string_array = []
    start = ord(start)
    end = ord(end)
    total = end - start
    while total >= 0:
        string_array.append(chr(start))
        start += 1
        total -= 1
    return string_array


# Create_bins_from_string takes a string with '-' as breaks and '...' as ranges
# and creates an array with each range of numbers or letters ex.[(MC),(1, 2, 3, 4), (A, B, C)
# then using those ranges creates every possible combination and return is in an array of strings
# ex. ['MC-01-A', 'MC-01-B', 'MC-01-C', 'MC-02-A', 'MC-02-B', 'MC-02-C', 'MC-03-A' ect...
# also counts and returns the total
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
    total = 0
    bin_list = []
    for s1 in list_of_bins[0]:
        if len(list_of_bins) == 1:
            bin_list.append(f'{s1}')
            total += 1
        elif len(list_of_bins) == 2:
            for s2 in list_of_bins[1]:
                bin_list.append(f'{s1}-{s2}')
                total += 1
        elif len(list_of_bins) == 3:
            for s2 in list_of_bins[1]:
                for s3 in list_of_bins[2]:
                    bin_list.append(f'{s1}-{s2}-{s3}')
                    total += 1
        elif len(list_of_bins) == 4:
            for s2 in list_of_bins[1]:
                for s3 in list_of_bins[2]:
                    for s4 in list_of_bins[3]:
                        bin_list.append(f'{s1}-{s2}-{s3}-{s4}')
                        total += 1
        elif len(list_of_bins) == 5:
            for s2 in list_of_bins[1]:
                for s3 in list_of_bins[2]:
                    for s4 in list_of_bins[3]:
                        for s5 in list_of_bins[4]:
                            bin_list.append(f'{s1}-{s2}-{s3}-{s4}-{s5}')
                            total += 1
        else:
            print('>>> Max of 5 categories (-) allowed')
    print(f'Total = {total}')
    print(f'Bin List = {bin_list}')
    return bin_list, total
