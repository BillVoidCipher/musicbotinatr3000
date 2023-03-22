playlist_id = {}


def _registration(name_id):
    if name_id in playlist_id.keys():
        return True
    else:
        playlist_id[name_id] = {}
        return False


def _append(name_id, name, url):
    try:
        playlist_id[name_id][0][name] = url
    except:
        print('Такого пользователя нет в базе данных')
        return False
    return True


def _delete(name_id, name):
    try:
        playlist_id[name_id][0].pop(name)
    except:
        print('Такой песни нет')
        return False
    return True


def _get_playlist(name_id):
    return [playlist_id[name_id][0][i] for i in playlist_id[name_id][0].keys()]


def _get_status(name_id):
    return playlist_id[name_id][1]