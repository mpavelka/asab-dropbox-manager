import asab
from .service import DropBoxService

class DropBoxModule(asab.Module):
	def __init__(self, app):
		super().__init__(app)
		self.service = DropBoxService(app, "DropBoxService")
