# example4-extrafiles.py - get info about all files in first thread
from __future__ import print_function
import basc_py4chan

def main():
    # grab the first thread on the board by checking first page
    board = py8chan.Board('v')
    all_thread_ids = board.get_all_thread_ids()
    first_thread_id = all_thread_ids[0]
    thread = board.get_thread(first_thread_id)

    # display the url of every file on the first thread, even extra files in posts
    for url in first_thread.files():
        print(url)

if __name__ == '__main__':
    main()
