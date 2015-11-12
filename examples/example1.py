# credits to Anarov for improved example.py
import basc_py4chan

def main():
	# grab the first thread on the board by checking first page
	v = basc_py4chan.Board('v')
	threads = v.get_threads()
	print("Got %i threads" % len(threads))
	first_thread = threads[0]

	# thread information
	print(thread)
	print('Sticky?', first_thread.sticky)
	print('Closed?', first_thread.closed)

	# topic information
	topic = thread.topic
	print('Topic Repr', topic)
	print('Postnumber', topic.post_number)
	print('Timestamp',  topic.timestamp)
	print('Datetime',   repr(topic.datetime))
	print('Subject',    topic.subject)
	print('Comment',    topic.text_comment)
	print('Replies',    first_thread.replies)

	# file information
	for f in first_thread.file_objects():
		print('Filename', f.filename)
		print('  Filemd5hex', f.file_md5_hex)
		print('  Fileurl', f.file_url)
		print('  Thumbnailurl', f.thumbnail_url)
		print()


if __name__ == '__main__':
	main()
