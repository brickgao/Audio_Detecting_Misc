# -*- coding: utf-8 -*-

import os, shutil, eyed3


# Decoder path
_decoder = os.path.abspath(u'./mpg123_decode/mpg123_to_wav.exe')

# Encoder path
_encoder = os.path.abspath(u'./lame_encode/lame.exe')

# Root path
_root_path = os.path.abspath(u'./')

# Output path
_output_path = os.path.abspath(u'./output')

def collect_mdct():
    if not os.path.exists(u'output'):
        os.mkdir(u'output')
    _input_path = os.path.abspath(u'./input')
    _file_in_list = os.listdir(_input_path)
    _input_len = len(_file_in_list)
    print 'Begin to collect MDCT...'
    print 'There is %d file(s) in \'./input\'.' % _input_len
    _cnt = 1
    for _file in _file_in_list:
        print 'Dealing with %s [%d/%d].' % (_file, _cnt, _input_len)
        _file_path = os.path.join(_input_path, _file)
        _audio = eyed3.load(_file_path)
        _bitrate = str(_audio.info.bit_rate[1])
        _recv = os.popen((_decoder + u' \"' + _file_path + u'\" tmp.wav').encode('gbk')).read()
        if 'written' not in _recv:
            print 'Warning: This file (' + str(_file_path) +  ') is not support'
        else:
            _recv = os.popen((_encoder + u' tmp.wav tmp.mp3 -b ' + _bitrate).encode('gbk')).read()
            with open(u'data.tmp', 'r') as _f1:
                _f2_name = os.path.splitext(_file)[0] + '_oneline.txt'
                with open(_f2_name, 'w') as _f2:
                    while True:
                        _line = _f1.readline()
                        if _line == '':     break
                        if _line == '\n':   continue
                        _f2.write(_line[:-1] + ' ')
                    _f2.close()
                _f1.close()
            shutil.move(os.path.join(_root_path, _f2_name), os.path.join(_output_path, _f2_name))
            shutil.move(u'data.tmp', os.path.join(_output_path, os.path.splitext(_file)[0] + '.txt'))
        os.remove(u'tmp.wav')
        os.remove(u'tmp.mp3')
        _cnt += 1
    print 'Task has been done, input any key to exit...'
    _ = raw_input()
    
if __name__ == '__main__':
    collect_mdct()
