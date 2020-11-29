def removeUserId(raw_data):
    for item in raw_data:
        item.pop('UserId')
    return raw_data

def joindata(main, temp, joincol : str, fillcol : str, data):
    for item in main:
        check = 0
        for t in temp:
            if int(item[joincol]) == int(t[joincol]):
                item.update({fillcol : t[fillcol]})
                check = 1
            elif(check == 0):
                item.update({fillcol : data})
    return main