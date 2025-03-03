from . import log
from . import config
from . import sqliteConn
from . import widgetlog
import platform
if platform.system() == "Windows":
    from . import regEdit
