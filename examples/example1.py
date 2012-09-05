import sys
sys.path.insert(0, '../')

import py4chan

def main():
    v = py4chan.Board('v')
    thread = v.getThread(152900882)
    print thread
    print 'Sticky?', thread.Sticky
    print 'Closed?', thread.Closed
    topic = thread.topic
    print 'Topic Repr', topic
    print 'PostNumber', topic.PostNumber
    print 'Timestamp',  topic.Timestamp
    print 'DateTime',   repr(topic.Datetime)
    print 'FileMd5hex', topic.FileMd5Hex
    print 'FileUrl',    topic.FileUrl
    print 'Subject',    topic.Subject
    print 'Comment',    topic.Comment
    print 'ThumbnailUrl',topic.ThumbnailUrl
    print 'Replies',    thread.replies


if __name__ == '__main__':
    main()
