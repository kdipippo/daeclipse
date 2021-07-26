def get_status_msg(group_name, folder_name, message):
    return '{0} | {1} | {2}'.format(group_name, folder_name, message)

print(get_status_msg("GROUP", '', "MESSAGE"))