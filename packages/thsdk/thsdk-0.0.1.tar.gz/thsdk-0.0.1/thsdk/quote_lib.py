# -*- coding: utf-8 -*-
"""
版本：1.0.0.1
作者：阿猛 ameng@nomyhexin.com 时间：20141106
更新时间：20141106 增加数据接口
文档介绍：Lib Python接口程序。需与.dll一起使用
修改历史：
版权：
"""

import ctypes
import os
import platform
import json


class QuoteLib:
    def __init__(self, ops: dict = ()):
        self.__lib_path = self._get_lib_path()
        self.lib = ctypes.CDLL(self.__lib_path)
        self._define_functions()
        self.lib.NewQuote(json.dumps(ops).encode('utf-8'))

    def _get_lib_path(self):
        system = platform.system()
        if system == 'Linux':
            lib_path = os.path.join(os.path.dirname(__file__), 'libquote.so')
        elif system == 'Darwin': # intel
            lib_path = os.path.join(os.path.dirname(__file__), 'libquote.dylib')
        elif system == 'Windows':
            lib_path = os.path.join(os.path.dirname(__file__), 'libquote.dll')
        else:
            raise OSError('Unsupported operating system')
        return lib_path

    def _get_lib_path_v2(self):
        system = platform.system()
        arch = platform.machine()
        print(f"system: {system}, arch: {arch}")
        lib_name = 'libquote'

        if system == 'Linux':
            if arch == 'x86_64':
                lib_path = os.path.join(os.path.dirname(__file__), f'{lib_name}_amd64.so')
            elif arch == 'aarch64':
                lib_path = os.path.join(os.path.dirname(__file__), f'{lib_name}_arm64.so')
            else:
                lib_path = os.path.join(os.path.dirname(__file__), f'{lib_name}.so')
        elif system == 'Darwin':
            if arch == 'x86_64':
                lib_path = os.path.join(os.path.dirname(__file__), f'{lib_name}_amd64.dylib')
            elif arch == 'arm64':
                lib_path = os.path.join(os.path.dirname(__file__), f'{lib_name}_arm64.dylib')
            else:
                lib_path = os.path.join(os.path.dirname(__file__), f'{lib_name}.dylib')
        elif system == 'Windows':
            lib_path = os.path.join(os.path.dirname(__file__), f'{lib_name}.dll')
        else:
            raise OSError('Unsupported operating system')

        return lib_path

    def _define_functions(self):
        self.lib.NewQuote.argtypes = [ctypes.c_char_p]
        self.lib.NewQuote.restype = None

        self.lib.Connect.restype = ctypes.c_char_p

        self.lib.DisConnect.restype = ctypes.c_char_p

        self.lib.QueryData.argtypes = [ctypes.c_char_p]
        self.lib.QueryData.restype = ctypes.c_char_p

    def connect(self):
        return self.lib.Connect()

    def disconnect(self):
        return self.lib.DisConnect()

    def query_data(self, req: str = ""):
        return self.lib.QueryData(req.encode('utf-8'))
