# credits to Anarov for improved example.py
# https://github.com/Anorov/py-4chan
import sys
sys.path.insert(0, '../')

import py4chan

def main():
    v = py4chan.Board('v')
    thread = v.get_thread(152900882)
    print(thread)
    print('Sticky?', thread.sticky)
    print('Closed?', thread.closed)
    topic = thread.topic
    print('Topic Repr', topic)
    print('Postnumber', topic.post_number)
    print('Timestamp',  topic.timestamp)
    print('Datetime',   repr(topic.datetime))
    print('Filemd5hex', topic.file_md5_hex)
    print('Fileurl',    topic.file_url)
    print('Subject',    topic.subject)
    print('Comment',    topic.comment)
    print('Thumbnailurl',topic.thumbnail_url)
    print('Replies',    thread.replies)
    print('All posts',  thread.all_posts)


if __name__ == '__main__':
    main()