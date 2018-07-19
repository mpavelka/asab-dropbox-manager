import asab
import logging
import sys

from .module import DropBoxModule
###

L = logging.getLogger(__name__)

###

class DropBoxManagerApp(asab.Application):

	def __init__(self):
		super().__init__()
		self.add_module(DropBoxModule)
		self.DropBoxService = self.get_service("DropBoxService")
		self.command_map = {
			"upload": self.DropBoxService.upload_file,
		}


	def create_argparser(self):
		parser = super().create_argparser()

		subparsers = parser.add_subparsers(dest="command")
		upload_subparser = subparsers.add_parser('upload')
		upload_subparser.add_argument('-i', '--input-file')
		upload_subparser.add_argument('-d', '--dest-path')

		return parser


	def parse_args(self):
		args = super().parse_args()
		self.command =  args.command or ""

		if self.command == "upload":
			self.command_args = {
				"file_path": args.input_file or "",
				"dest_path": args.dest_path or "",
			}

		return args


	async def initialize(self):
		L.setLevel(logging.INFO)


	async def main(self):

		if not self.command in self.command_map:
			print("Unknown command. Run with --help to see your options.", file=sys.stderr)
			self.stop()
			return

		# Run command
		self.command_map[self.command](**self.command_args)
		self.stop()

