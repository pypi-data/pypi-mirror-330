from inspyre_toolbox.ver_man import PyPiVersionInfo, VersionParser
from inspyre_toolbox.ver_man.helpers import read_version_file
from pathlib import Path


CWD = Path(__file__).parent


VERSION_FILE_PATH = CWD / '__VERSION__'

VERSION_PARSER = VersionParser(read_version_file(VERSION_FILE_PATH))

VERSION = VERSION_PARSER.version_str
