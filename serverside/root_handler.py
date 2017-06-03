# encrypt songs from root mus_library to user collection_library
# set gold for users
# set price for songs
# update collection

import glob

from serverside import pickle_file


def main():
    print('Encrypt files: encrypt <file_name>')
    print('Set gold for user: setgold <user_name> <amount>')
    print('Set price for song: setprice <song_name> <price>')
    for file in glob.glob("mus_library/*"):
        print(file)
    while True:
        stream = input()
        cmd = stream.split(" ")
        if cmd[0] == 'encrypt':
            fname = cmd[1]
        if cmd[0] == 'setgold':
            username = pickle_file.fileload(cmd[1], root=True)
            if username == 'Retry':
                print('No such user')
                continue
            else:
                username.set_gold(int(cmd[2]))
                pickle_file.filesave(username)
        if cmd[0] == 'setprice':

            cmd[1].set_price(cmd[2])
        if stream == 'quit':
            return

