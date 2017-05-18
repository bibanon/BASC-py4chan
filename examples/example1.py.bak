# credits to Anarov for improved example.py
from __future__ import print_function
import basc_py4chan

def main():
    # grab the first thread on the board by checking first page
    board = basc_py4chan.Board('v')
    all_thread_ids = board.get_all_thread_ids()
    first_thread_id = all_thread_ids[0]
    thread = board.get_thread(first_thread_id)

    # thread information
    print(thread)
    print('Sticky?', thread.sticky)
    print('Closed?', thread.closed)

    # topic information
    topic = thread.topic
    print('Topic Repr', topic)
    print('Postnumber', topic.post_number)
    print('Timestamp',  topic.timestamp)
    print('Datetime',   repr(topic.datetime))
    print('Subject',    topic.subject)
    print('Comment',    topic.text_comment)
    print('Replies',    thread.replies)

    # file information
    for f in thread.file_objects():
        print('Filename', f.filename)
        print('  Filemd5hex', f.file_md5_hex)
        print('  Fileurl', f.file_url)
        print('  Thumbnailurl', f.thumbnail_url)
        print()


if __name__ == '__main__':
    main()
