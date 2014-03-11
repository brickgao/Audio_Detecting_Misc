# -*- coding: utf-8 -*-

import os
from libsvm.svmutil import *

_bitrate_list = [u'8', u'16', u'24', u'32', u'40', u'48',
                 u'56', u'64', u'80', u'96', u'112', u'128',
                 u'160', u'192', u'224', u'256', u'320']
_bitrate_list = [u'32']
_y, _x = [], []

def analyse_process(_group):
    os.remove(u'tmp.wav')
    os.remove(u'tmp.mp3')
    _file_in = open(u'data.tmp', 'r')
    _cnt_arr, _eq_zero, _len = [0.0 for x in range(20)], 0, 0
    try:
        for _i in range(2):  _line = _file_in.readline()
        while True:
            _line = _file_in.readline()
            if _line == '':     break
            if _line == '\n':   continue
            _mdct_arr = map(float, _line.split(' ')[:-1])
            _len += 1
            for _e in _mdct_arr:
                if _e == 0.0:   _eq_zero += 1
            for _i in range(20):
                _list = _mdct_arr[_i * 24: (_i + 1) * 24]
                _cnt_arr[_i] += sum(_list) / 24.0
        _eq_zero = float(_eq_zero) / float(_len)
        for i in range(20):     _cnt_arr[i] /= float(_len)
        _y.append(_group)
        _x.append([_eq_zero] + _cnt_arr)
    finally:
        _file_in.close()
        os.remove(u'data.tmp')

# Decoder path
_decoder = os.path.abspath(u'./mpg123_decode/mpg123_to_wav.exe')

# Encoder path
_encoder = os.path.abspath(u'./lame_encode/lame.exe')
                 
# Analyse origin mp3 file
for _bitrate in _bitrate_list:
    _folder_path = os.path.abspath(u'F:/mp3_sample/origin/' + _bitrate)
    _file_list = os.listdir(_folder_path)
    print 'Starting analyse origin ' + str(_bitrate) + '-bitrate mp3 file'
    for _file in _file_list:
        _file_path = os.path.abspath(unicode(_folder_path) + u'/' + _file)
        _recv = os.popen(_decoder + u' \"' + _file_path + u'\" tmp.wav').read()
        if 'written' not in _recv:
            print 'Warning: This file (' + str(_file_path) +  ') is not support'
        else:
            _recv = os.popen(_encoder + u' tmp.wav tmp.mp3 -b 32').read()
            analyse_process(1)
    print 'Analysing for origin ' + str(_bitrate) + '-bitrate mp3 file has been done'

# Analyse double double-compress mp3 file
for _bitrate in _bitrate_list:
    _folder_path = os.path.abspath(u'F:/mp3_sample/double_compression/' + _bitrate)
    _nxt_folder_list = os.listdir(_folder_path)
    print 'Starting analyse double-compress ' + str(_bitrate) + '-bitrate mp3 file'
    for _nxt_folder in _nxt_folder_list:
        _nxt_folder_path = os.path.abspath(unicode(_folder_path) + u'/' + _nxt_folder)
        _file_list = os.listdir(_nxt_folder_path)
        for _file in _file_list:
            if u'_' + _bitrate + u'.mp3' == _file:      continue
            if _file != u'_64.mp3':                     continue
            _file_path = os.path.abspath(unicode(_nxt_folder_path) + u'/' + _file)
            _recv = os.popen(_decoder + u' \"' + _file_path + u'\" tmp.wav').read()
            if 'written' not in _recv:
                print 'Warning: This file (' + str(_file_path) +  ') is not support'
            else:
                _recv = os.popen(_encoder + u' tmp.wav tmp.mp3 -b 64').read()
                analyse_process(-1)
    print 'Analysing for double-compress ' + str(_bitrate) + '-bitrate mp3 file has been done'

_m = svm_train(_y, _x)
svm_save_model('detecting_double_compression.model', _m)
