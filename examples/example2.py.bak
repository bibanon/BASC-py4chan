# credits to Anarov for improved example.py
from __future__ import print_function
import basc_py4chan

def main():
    if len(sys.argv) != 3:
        print("Usage: python %s [board] [thread]" % sys.argv[0])
        print("Shows the URL of all the files in the thread.")
        print("Example (download all files in thread): python %s v 12351234 | xargs wget"
              % sys.argv[0])
        return

    board = basc_py4chan.Board(sys.argv[1])
    thread = board.get_thread(int(sys.argv[2]))
    for f in thread.files():
        print(f)

if __name__ == '__main__':
    main()
