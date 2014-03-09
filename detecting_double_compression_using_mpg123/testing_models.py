# -*- coding: utf-8 -*-

import os
from libsvm.svmutil import *

_y, _x = [], []

_mode_list = [(u'origin', 1), (u'double_compression', -1)]

def analyse_process(_group):
    os.remove(u'tmp.wav')
    _file_in = open(u'data.tmp', 'r')
    _cnt_arr, _p_arr = [0 for x in range(10)], []
    while True:
        _line = _file_in.readline()
        if _line == '':     break
        if _line == '\n':   continue
        _s_list = _line.split(' ')[:-1]
        for _e in _s_list:
            if _e[0] == '-':    _cnt_arr[int(_e[1])] += 1
            else:               _cnt_arr[int(_e[0])] += 1
    _total = 0
    for _e in _cnt_arr[1:]:     _total += _e
    if _total:
        for _e in _cnt_arr[1:]:     _p_arr.append(float(_e) / float(_total))
        _y.append(_group)
        _x.append(_p_arr)
    _file_in.close()
    os.remove(u'data.tmp')

# Decoder path
_decoder = os.path.abspath(u'./mpg123_decode/mpg123_to_wav.exe')

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
            analyse_process(_mode[1])

_m = svm_load_model('detecting_double_compression.model')
p_labels, p_acc, p_vals = svm_predict(_y, _x, _m)
