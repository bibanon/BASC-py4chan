# example4-extrafiles.py - get info about all files in first thread

import basc_py4chan

def main():
	# grab the first thread on the board by checking first page
	v = basc_py4chan.Board('v')
	threads = v.get_threads()
	print("Got %i threads" % len(threads))
	first_thread = threads[0]

	# display info about every file on the first thread, even extra files in posts
	for post in first_thread.all_posts:
		if post.has_file:
			print(":: Post #", post.post_number)
			for file in post.all_files():
				print("  ", file.filename)
				print("  ", file.file_md5_hex)
				print("  ", file.file_url)
				print("  ", file.thumbnail_url)
				print()

if __name__ == '__main__':
	main()
