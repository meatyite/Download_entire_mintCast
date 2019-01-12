#!/usr/bin/python2

import urllib
from bs4 import BeautifulSoup
from urlparse import urlparse
from os.path import basename, isfile
#from thread import start_new_thread
from threading import Thread
import sys

main_page_url = "http://mintcast.org/"
pages = [main_page_url, 'http://mintcast.org/page/1/']
file_format = '.ogg'
download_everything_at_once = False

VERSION = '1.0.0'

def search_for_pages(url):
	opener = urllib.urlopen(url)
	content = opener.read()
	soup = BeautifulSoup(content, 'html.parser')
	for link in soup.find_all('a'):
		a_tag_url = link.get('href')
		if not(a_tag_url == None):
			a_tag_url = a_tag_url.replace('https://', 'http://')
			if a_tag_url.startswith('http://mintcast.org/page/'):
				if not(a_tag_url in pages):
					pages.append(a_tag_url)
					print "found page: " + a_tag_url
					search_for_pages(a_tag_url)

def search_and_download(url):

	opener = urllib.urlopen(url)
	content = opener.read()
	soup = BeautifulSoup(content, 'html.parser')

	for link in soup.find_all('a'):
    		a_tag_string = link.get('string')
    		a_tag_url = link.get('href')
		if not(a_tag_url == None): a_tag_url = a_tag_url.replace('https://', 'http://')
		if not(a_tag_url == None):

	  	  	if a_tag_url.endswith(file_format):
				filename_to_save = basename(urlparse(a_tag_url).path)
				print 'downloading ' + filename_to_save + "..."
				try:
					if not(isfile(filename_to_save)):
				
						if download_everything_at_once:
							Thread(target=urllib.urlretrieve, args=(a_tag_url, filename_to_save)).start()
						else:
							urllib.urlretrieve(a_tag_url, filename_to_save)
				except Exception as e:
					print 'DOWNLOAD FAILED FOR: ' + filename_to_save + ': ' + str(e)
			

if __name__ == '__main__':
	for i in range(0, len(sys.argv)):
		arg = sys.argv[i] 
		if arg == '-h' or arg == '--help':
			print """usage: download_entire_mintcast.py [flag1] [flag2]
				list of flags:
				-h   --help          Show this help menu
				-v   --version       Show this program's version
				-f   --format        Choose the file format to download (ogg or mp3) (default: ogg)
				-a   --all-at-once   Download every file at once instead of waiting for each file to download
			       """ 
			sys.exit(0)
		elif arg == '-v' or arg == '--version':
			print "download_entire_mintcast version " + VERSION
			sys.exit(0)
		elif arg == '-f' or arg == '--format':
			file_format = '.' + sys.argv[i + 1]
		elif arg == '-a' or arg == '--all-at-once':
			download_everything_at_once = True					

	
	print "Finding pages..."
	search_for_pages(main_page_url)
	for page in pages:
		search_and_download(page)
