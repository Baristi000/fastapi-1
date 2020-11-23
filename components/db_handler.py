def removeUserId(raw_data):
    for item in raw_data:
        item.pop('UserId')
    return raw_data