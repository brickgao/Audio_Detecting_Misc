# -*- coding: utf-8 -*-

import wave_op, math, os

# Decoder path
_decoder = os.path.abspath(u'./mpg123_decode/mpg123_to_wav.exe')

# Encoder path
_encoder = os.path.abspath(u'./lame_encode/lame.exe')

def detect(_file_name):
    _ret = []
    _recv = os.popen((_decoder + u' ' + _file_name + u' tmp_origin.wav').encode('gbk')).read()
    if 'written' not in _recv:
        print 'Warning: This file is not support'
    else:
        _nframe = wave_op.get_nframe(u'tmp_origin.wav')
        for _frame in range(_nframe):
            print 'dealing with frame ' + str(_frame)
            _min_num, _offset = [], []
            for _i in range(576):
                wave_op.add_zero(u'tmp_origin.wav', _frame, _i)
                _recv = os.popen(_encoder + u' tmp_processed.wav tmp.mp3 -b 32').read()
                _len = 0
                with open(u'data.tmp', 'r') as _file_in:
                    for _j in range(2):  _line = _file_in.readline()
                    while True:
                        _line = _file_in.readline()
                        if _line == '':     break
                        if _line == '\n':   continue
                        _mdct_arr = map(float, _line.split(' ')[:-1])
                        _cnt = 0
                        for _j in range(576):
                            _tmp = 10 * math.log(max((_mdct_arr[_j] ** 2) * (10 ** 10), 1.0), 10)
                            if _tmp == 0.0:     _cnt += 1
                        if not _i:
                            _offset.append(0)
                            _min_num.append(_cnt)
                        else:
                            if _len < len(_min_num) and _cnt < _min_num[_len]:
                                _min_num[_len], _offset[_len] = _cnt, _i
                        _len += 1
                    _file_in.close()
                os.remove(u'tmp_processed.wav')
                os.remove(u'tmp.mp3')
                os.remove(u'data.tmp')
            _ret.append(_offset[_frame])
        print _ret
    os.remove(u'tmp_origin.wav')
            


if __name__ == '__main__':
    detect(u'test.mp3')
