# -*- coding: utf-8 -*-

import wave

def get_nframe(_file_name):
    _file_in = wave.open(_file_name, 'rb')
    _tmp = _file_in.getparams()
    return _tmp[3] / 576

def add_zero(_file_name, pos, offset):
    _file_in = wave.open(_file_name, 'rb')
    _tmp = _file_in.getparams()
    _params = (_tmp[0], _tmp[1], _tmp[2], _tmp[3] + offset, _tmp[4], _tmp[5])
    _data = _file_in.readframes(_tmp[3])
    _add = ''
    for _i in range(offset):
        for _j in range(_tmp[1]):
            _add += chr(0)
    _data = _data[:pos * 576] + _add + _data[pos * 576:]
    _file_out = wave.open('tmp_processed.wav', 'wb')
    _file_out.setparams(_params)
    _file_out.writeframes(_data)
    _file_out.close()
    _file_in.close()

if __name__ == '__main__':
    add_zero(u'tmp_origin.wav', 1, 1)
