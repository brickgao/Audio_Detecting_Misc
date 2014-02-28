# -*- coding: utf-8 -*-

import os
from lib.libsvm.svmutil import *

_p_list = [u'origin', u'after_double_compression']
_x = []
_y = []

for _p in _p_list:
    _list = os.listdir(u'./sample_extract/' + _p)
    for _f in _list:
        _file_in_path = os.path.join(u'./sample_extract/' + _p, _f)
        _file_in = open(_file_in_path, 'r')
        _list = _file_in.readline().split()
        _file_in.close()
        _list = map(float, _list)
        if _p == u'origin':     _y.append(1)
        else:                   _y.append(-1)
        _x.append(_list)

_m = svm_train(_y[:40], _x[:40])
p_label, p_acc, p_val = svm_predict(_y[40:], _x[40:], _m)
