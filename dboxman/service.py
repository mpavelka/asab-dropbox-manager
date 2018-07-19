import asab
import dropbox
import logging
import os
import sys
import dropbox.exceptions


L = logging.getLogger(__name__)


asab.Config.add_defaults({
	'dropbox': {
		'access_token': '',
		'chunk_size': '4194304', # 4 * 1024 * 1024
	}
})



class DropBoxService(asab.Service):

	def __init__(self, app, service_name):
		super().__init__(app, service_name)
		self._chunk_size = int(asab.Config['dropbox']['chunk_size'])
		self._dropbox = dropbox.Dropbox(asab.Config['dropbox']['access_token'])


	def upload_file(self, file_path, dest_path):
		"""
			Inspired by https://stackoverflow.com/a/37399658/2086932
		"""

		try:
			f = open(file_path, "rb")
		except IOError as e:
			L.error("Can't open '{}': {}".format(file_path, e.strerror))
			return

		# Default file destination
		if dest_path is None or dest_path == "":
			dest_path = "/"+os.path.basename(file_path)

		# Get file size
		file_size = os.path.getsize(file_path)


		# File fits to one chunk
		if file_size <= self._chunk_size:
			try:
				self._dropbox.files_upload(f.read(), dest_path)
			except dropbox.exceptions.DropboxException as e:
				L.error("Error when uploading file at once: {}".format(e))
				f.close()
				return

		# File is larger then one chunk
		else:
			try:
				session = self._dropbox.files_upload_session_start(f.read(self._chunk_size))
				cursor 	= dropbox.files.UploadSessionCursor(
							session_id=session.session_id,
							offset=f.tell())
			except dropbox.exceptions.DropboxException as e:
				L.error("Error when starting dropbox session: {}".format(e))
				f.close()
				return

			try:
				commit 	= dropbox.files.CommitInfo(path=dest_path)
			except dropbox.exceptions.DropboxException as e:
				L.error("Error when commiting info to file at once: {}".format(e))
				f.close()
				return

			while f.tell() < file_size:
				if ((file_size - f.tell()) > self._chunk_size):
					try:
						self._dropbox.files_upload_session_append(
							f.read(self._chunk_size),
							cursor.session_id,
							cursor.offset)
						cursor.offset = f.tell()
					except dropbox.exceptions.DropboxException as e:
						L.error("Error when finishing file upload: {}".format(e))
						f.close()
						return
				else:
					try:
						self._dropbox.files_upload_session_finish(
							f.read(self._chunk_size),
							cursor,
							commit)
					except dropbox.exceptions.DropboxException as e:
						L.error("Error when finishing file upload: {}".format(e))
						f.close()
						return
