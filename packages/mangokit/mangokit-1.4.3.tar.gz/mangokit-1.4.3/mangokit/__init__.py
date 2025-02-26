# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-09-07 22:15
# @Author : 毛鹏
import platform
import sys
import os

python_version = sys.version_info
if f"{python_version.major}.{python_version.minor}" != "3.10":
    raise Exception("必须使用Python3.10.N")

system = platform.system()
if system == 'Windows':
    runtime_path = os.path.join(os.path.dirname(__file__), "mangos", "pyarmor_runtime_windows")
elif system == 'Linux':
    runtime_path = os.path.join(os.path.dirname(__file__), "mangos", "pyarmor_runtime_linux")
elif system == 'Darwin':  # macOS
    runtime_path = os.path.join(os.path.dirname(__file__), "mangos", "pyarmor_runtime_macos")
else:
    raise ImportError("Unsupported operating system")

if runtime_path not in sys.path:
    sys.path.append(runtime_path)

runtime_sub_path = os.path.join(runtime_path, "pyarmor_runtime_000000")
if runtime_sub_path not in sys.path:
    sys.path.append(runtime_sub_path)

try:
    import pyarmor_runtime_000000
except ImportError as e:
    raise RuntimeError(f"Failed to load PyArmor runtime for {system}: {e}")
try:
    from mangokit.mangos.pyarmor_runtime_windows.mango import Mango
except ImportError as e:
    raise RuntimeError(f"Failed to import obfuscated module: {e}")

from mangokit.tools.base_request import *
from mangokit.tools.log_collector import set_log
from mangokit.tools.data_processor import *
from mangokit.tools.database import *
from mangokit.models.models import *
from mangokit.tools.decorator import *
from mangokit.tools.notice import *
from mangokit.enums.enums import *
from mangokit.exceptions import MangoKitError

__all__ = [
    'DataProcessor',
    'DataClean',
    'ObtainRandomData',
    'CacheTool',
    'CodingTool',
    'EncryptionTool',
    'JsonTool',
    'RandomCharacterInfoData',
    'RandomNumberData',
    'RandomStringData',
    'RandomTimeData',

    'MysqlConingModel',
    'ResponseModel',
    'EmailNoticeModel',
    'TestReportModel',
    'WeChatNoticeModel',
    'FunctionModel',
    'ClassMethodModel',

    'CacheValueTypeEnum',
    'NoticeEnum',

    'MysqlConnect',
    'SQLiteConnect',
    'requests',
    'async_requests',
    'set_log',
    'WeChatSend',
    'EmailSend',

    'singleton',
    'convert_args',

    'Mango',

    'MangoKitError',
]