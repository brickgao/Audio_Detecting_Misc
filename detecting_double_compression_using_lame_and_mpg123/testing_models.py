# -*- coding: utf-8 -*-

import os
from libsvm.svmutil import *

_y, _x = [], []

_mode_list = [(u'origin', u'32', 1), (u'double_compression', u'64', -1)]

def analyse_process(_group):
    try:
        _file_in = open(u'data.tmp', 'r')
        _cnt_arr, _eq_zero, _len = [0.0 for x in range(20)], 0, 0
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
        os.remove(u'tmp.wav')
        os.remove(u'tmp.mp3')

# Decoder path
_decoder = os.path.abspath(u'./mpg123_decode/mpg123_to_wav.exe')

# Encoder path
_encoder = os.path.abspath(u'./lame_encode/lame.exe')

# Analyse origin and double-compress mp3 file
for _mode in _mode_list:
    _folder_path = os.path.abspath(u'F:/test_sample/' + _mode[0] + u'/')
    _file_list = os.listdir(_folder_path)
    for _file in _file_list:
        _file_path = os.path.abspath(unicode(_folder_path) + u'/' + _file)
        _recv = os.popen((_decoder + u' \"' + _file_path + u'\" tmp.wav').encode('gbk')).read()
        if 'written' not in _recv:
            print 'Warning: This file (' + str(_file_path) +  ') is not support'
        else:
            _recv = os.popen((_encoder + u' tmp.wav tmp.mp3 -b ' + _mode[1]).encode('gbk')).read()
            analyse_process(_mode[2])

_m = svm_load_model('detecting_double_compression.model')
p_labels, p_acc, p_vals = svm_predict(_y, _x, _m)
