# example4-extrafiles.py - get info about all files in first thread
from __future__ import print_function
import basc_py4chan

def main():
    # grab the first thread on the board by checking first page
    board = basc_py4chan.Board('v')
    all_thread_ids = board.get_all_thread_ids()
    first_thread_id = all_thread_ids[0]
    thread = board.get_thread(first_thread_id)

    # display info about every file on the first thread, even extra files in posts
    for post in thread.all_posts:
        if post.has_file:
            print(":: Post #", post.post_number)
            print("  ", post.file.filename)
            print("  ", post.file.file_md5_hex)
            print("  ", post.file.file_url)
            print("  ", post.file.thumbnail_url)
            print()

if __name__ == '__main__':
    main()