# -*- coding: utf-8 -*-

import wave

def add_zero(_file_name, offset):
    _file_in = wave.open(_file_name, 'rb')
    _tmp = _file_in.getparams()
    _params = (_tmp[0], _tmp[1], _tmp[2], _tmp[3] + offset, _tmp[4], _tmp[5])
    _data = _file_in.readframes(_tmp[3])
    for _i in range(offset):
        for _j in range(_tmp[1]):
            _data = chr(0) + _data
    _file_out = wave.open('tmp.wav', 'wb')
    _file_out.setparams(_params)
    _file_out.writeframes(_data)
    _file_out.close()
    _file_in.close()