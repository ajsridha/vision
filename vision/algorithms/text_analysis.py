def find_total_on_line(lines, index):
    for word in lines[index]:
        if word.is_percentage():
            continue
        if word.is_money():
            return word
