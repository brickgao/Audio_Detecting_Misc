# -*- coding: utf-8 -*-

import os

_p_list = [u'origin', u'after_double_compression']

for _p in _p_list:
    _list = os.listdir(u'./sample/' + _p)
    for _f in _list:
        _file_in_path = os.path.join(u'./sample/' + _p, _f)
        _file_in = open(_file_in_path, 'r')
        _arr = [0 for x in range(10)]
        while True:
            _line = _file_in.readline()
            if _line == '':     break
            if _line == '\n':   continue
            _list = _line.split()[:-1]
            for _e in _list:
                if _e[0] == '-':
                    _arr[int(_e[1])] += 1
                else:
                    _arr[int(_e[0])] += 1
        _file_out_path = os.path.join(u'./sample_extract/' + _p, _f)
        _file_out = open(_file_out_path, 'w')
        _total = 0
        _s = ''
        for _e in _arr[1:]:     _total += _e
        for _e in _arr[1:]:     _s += str(float(_e) / float(_total)) + ' '
        _file_out.write(_s)
        _file_in.close()
        _file_out.close()
