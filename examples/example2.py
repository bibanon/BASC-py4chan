import sys
sys.path.insert(0, '../')

import py4chan

def main():
    if len(sys.argv) != 3:
        print "Usage: python %s [board] [thread]" % sys.argv[0]
        print "Shows the URL of all the files in the thread."
        print "Example (download all files in thread): python %s v 12351234 | xargs wget" % sys.argv[0]
        return

    board = py4chan.Board(sys.argv[1])
    thread = board.get_thread(int(sys.argv[2]))
    for file in thread.files():
        print file

if __name__ == '__main__':
    main()
