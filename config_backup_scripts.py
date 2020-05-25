#!/bin/python

import datetime
import requests
import dropbox
import os


links = [
		'~/.config/i3',
		'~/.config/i3blocks',
		'~/.config/dunst',
		'/etc/i3blocks.conf',
		'/etc/i3status.conf',
		'/usr/share/rofi/themes/Adapta-Nokto.rasi'		
]

class BackupCreate:
	def __init__(self):
		self.day = datetime.datetime.today().strftime("%Y-%m-%d")
		self.dir = f'/tmp/{self.day}-backup-dir'

	def directory_create(self):
		if not os.path.isdir(self.dir):
			os.mkdir(self.dir)
			return

	def directory_remove(self):
		os.rmdir(self.dir)

	def copy_file(self):
		for i in links:
			os.popen(f'cp -r {i} {self.dir}')
		self.create_archive()

	def create_archive(self):
		os.chdir('/tmp')
		os.popen(f'tar -czf {self.day}-backup-dir.tar.gz -C {self.dir} .')


class DropBoxUpload:
	def __init__(self, dropbox_token,):
		self.file = BackupCreate()
		self.path = f'/config/{self.file.day}-backup.tar.gz'
		self.client = dropbox.Dropbox(dropbox_token)

	def file_upload(self):
		self.client.files_upload(open(f'{self.file.dir}.tar.gz', 'rb').read(), self.path)


class TelegramNotify:
	def __init__(self, token, chatid):
		self.bot_token = token
		self.chat_id = chatid

	def send_notice(self, text):
		message = f'https://api.telegram.org/bot{self.bot_token}/sendMessage?chat_id={self.chat_id}&text={text}'
		return requests.get(message)


class Application:
	def __init__(self):
		self.backup = BackupCreate()
		self.record = DropBoxUpload('<DROPBOX-TOKEN>')
		self.notify = TelegramNotify('<TELEGRAM-BOT-TOKEN>', '<CHAT-ID>')

	def run(self):
		self.backup.directory_create()
		self.backup.copy_file()
		self.backup.create_archive()
		try: 
			self.record.file_upload()
			self.notify.send_notice(f'Configuration files have been uploaded.({self.backup.day})')
		except:
			self.notify.send_notice(f'Failed to upload files! ({self.backup.day})')

if __name__ == '__main__':
	app = Application()
	app.run()
