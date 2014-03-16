import sys
sys.path.insert(0, '../')

import py4chan

def main():
    v = py4chan.Board('v')
    thread = v.get_thread(152900882)
    print thread
    print 'Sticky?', thread.sticky
    print 'Closed?', thread.closed
    topic = thread.topic
    print 'Topic Repr',   topic
    print 'Post_number',  topic.post_number
    print 'Timestamp',    topic.timestamp
    print 'Date_time',    repr(topic.datetime)
    print 'Image_md5_hex', topic.image_md5_hex
    print 'Image_url',     topic.image_url
    print 'Subject',      topic.subject
    print 'Comment',      topic.comment
    print 'Thumbnail_url',topic.thumbnail_url
    print 'Replies',      thread.replies
    print 'All_posts',    thread.all_posts
    print 'Thread_url',    thread.thread_url

if __name__ == '__main__':
    main()
