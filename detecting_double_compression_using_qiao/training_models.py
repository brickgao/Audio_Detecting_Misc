# -*- coding: utf-8 -*-

import os, eyed3, numpy
from collections import Counter
from libsvm.svmutil import *

_bitrate_list = [u'8', u'16', u'24', u'32', u'40', u'48',
                 u'56', u'64', u'80', u'96', u'112', u'128',
                 u'160', u'192', u'224', u'256', u'320']
_bitrate_list = [u'32']
_y, _x = [], []

# Decoder path
_decoder = os.path.abspath(u'./mpg123_decode/mpg123_to_wav.exe')

# Encoder path
_encoder = os.path.abspath(u'./lame_encode/lame.exe')

def get_features(_mdct_arr, _len):
    _mdct_arr_dict = dict(Counter(_mdct_arr))
    _mdct_arr_dict.items().sort()
    _f1 = float(_mdct_arr_dict[0.0]) / float(_len)
    _f2 = sum(_mdct_arr) / float(_len)
    del _mdct_arr_dict[0.0]
    if len(_mdct_arr_dict) <= 1:
        _mdct_arr_d = []
        _d_keys = _mdct_arr_dict.keys()
        _d_len = len(_d_keys)
        for _i in range(_d_len - 1):
            _mdct_arr_d.append(_mdct_arr_dict[_d_keys[_i] + 1] - _mdct_arr_dict[_d_keys[_i]])
        _mdct_arr_f = []
        for _i in range(_d_len - 1):
            _mdct_arr_f.append(_mdct_arr_d[_i] * (_mdct_arr_dict[_d_keys[_i]] + _mdct_arr_dict[_d_keys[_i] + 1]))
        _f3 = float(_d_len)
        _f4 = sum(_mdct_arr_d) / float(_d_len - 1)
        _f5 = numpy.std(_mdct_arr_d)
        _f6 = sum(_mdct_arr_f) / (_d_len - 1)
        _f7 = numpy.std(_mdct_arr_f)
    else:
        _f3 = _f4 = _f5 = _f6 = _f7 = 0.0
    return [_f1, _f2, _f3, _f4, _f5, _f6, _f7]

def analyse_process(_group):
    with open(u'data.tmp', 'r') as _file_in:
        _len = 0
        _mdct_arr = []
        for _i in range(2):  _line = _file_in.readline()
        while True:
            _line = _file_in.readline()
            if _line == '':     break
            if _line == '\n':   continue
            _mdct_arr += map(abs, map(float, _line.split(' ')[:-1]))
            _len += 1
        _y.append(_group)
        _x.append(get_features(_mdct_arr, _len))
        _file_in.close()
    os.remove(u'data.tmp')
    os.remove(u'tmp.wav')
    os.remove(u'tmp.mp3')
 
# Analyse origin mp3 file
for _bitrate in _bitrate_list:
    _folder_path = os.path.abspath(u'F:/mp3_sample/origin/')
    _file_list = os.listdir(_folder_path)
    print 'Starting analyse origin ' + str(_bitrate) + '-bitrate mp3 file'
    _cnt, _total = 1, len(_file_list)
    for _file in _file_list:
        print 'Dealing with %s [%d/%d]' % (_file, _cnt, _total)
        _file_path = os.path.abspath(unicode(_folder_path) + u'/' + _file)
        _recv = os.popen(_decoder + u' \"' + _file_path + u'\" tmp.wav').read()
        if 'written' not in _recv:
            print 'Warning: This file (' + str(_file_path) +  ') is not support'
        else:
            _audio = eyed3.load(_file_path)
            _audio_bitrate = str(_audio.info.bit_rate[1])
            _recv = os.popen(_encoder + u' tmp.wav tmp.mp3 -b ' + _audio_bitrate).read()
            analyse_process(1)
        _cnt += 1
    print 'Analysing for origin ' + str(_bitrate) + '-bitrate mp3 file has been done'

# Analyse double double-compress mp3 file
for _bitrate in _bitrate_list:
    _folder_path = os.path.abspath(u'F:/mp3_sample/double_compression/')
    _file_list = os.listdir(_folder_path)
    print 'Starting analyse double-compress ' + str(_bitrate) + '-bitrate mp3 file'
    _cnt, _total = 1, len(_file_list)
    for _file in _file_list:
        print 'Dealing with %s [%d/%d]' % (_file, _cnt, _total)
        _file_path = os.path.abspath(unicode(_folder_path) + u'/' + _file)
        _recv = os.popen(_decoder + u' \"' + _file_path + u'\" tmp.wav').read()
        if 'written' not in _recv:
            print 'Warning: This file (' + str(_file_path) +  ') is not support'
        else:
            _audio = eyed3.load(_file_path)
            _audio_bitrate = str(_audio.info.bit_rate[1])
            _recv = os.popen(_encoder + u' tmp.wav tmp.mp3 -b ' + _audio_bitrate).read()
            analyse_process(-1)
        _cnt += 1
    print 'Analysing for double-compress ' + str(_bitrate) + '-bitrate mp3 file has been done'

_m = svm_train(_y, _x)
svm_save_model('detecting_double_compression.model', _m)
