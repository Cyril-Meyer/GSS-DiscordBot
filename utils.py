SIZE_COL_1 = 11
SIZE_COL_2 = 21
LINE_SIZE = SIZE_COL_1+SIZE_COL_2+8
# 2000 - 10 is an overestimation to avoid problems
MAX_LINE = (2000 - 10) // LINE_SIZE


def get_message_line(key, info):
    return f'║ {key:<{SIZE_COL_1}.{SIZE_COL_1}} ║ {info:<{SIZE_COL_2}.{SIZE_COL_2}} ║\n'


def get_message(desc, info):
    # only one list allowed and in last position
    for i, k in enumerate(info.keys()):
        if type(info[k]) is list and not i == len(info.keys()) - 1:
            raise ValueError
    # create header
    output = '```'
    line_break = f'╠{"":═<{SIZE_COL_1+2}}╬{"":═<{SIZE_COL_2+2}}╣\n'
    output += f'╔{"":═<{SIZE_COL_1+SIZE_COL_2+5}}╗\n'
    output += f'║{desc:^{SIZE_COL_1+SIZE_COL_2+5}}║\n'
    output += f'╠{"":═<{SIZE_COL_1+2}}╦{"":═<{SIZE_COL_2+2}}╣\n'
    # count lines to avoid more than 2000 characters
    line_counter = 3
    # add line for each key of the dict
    for i, k in enumerate(info.keys()):
        # handle list
        if type(info[k]) is list:
            output += get_message_line(k, info[k][0])
            line_counter += 1
            for e in info[k][1:]:
                output += get_message_line('', e)
                line_counter += 1
                if line_counter+3 > MAX_LINE:
                    output += get_message_line('', 'and more...')
                    break
        elif type(info[k]) is str or type(info[k]) is int or type(info[k]) is float:
            output += get_message_line(k, str(info[k]))
            line_counter += 1
        else:
            raise NotImplementedError

        if i == len(info.keys()) - 1:
            output += f'╚{"":═<{SIZE_COL_1 + 2}}╩{"":═<{SIZE_COL_2 + 2}}╝\n'
            line_counter += 1
        else:
            output += line_break
            line_counter += 1

    # crop string to be 200 chars safe
    output = output[0:1997]
    output += '```'

    return output
