# -*- coding: utf-8 -*-

import table_misc as TM
import os


def split_mp3(_file_name):
    with open(_file_name, 'rb') as _file:
        _file_size = os.path.getsize(_file_name)
        _size_left = _file_size
        _tmp_buffer = _file.read(10)
        cnt = 0
        # Skip ID3V2 tag If there is
        if _tmp_buffer[:3] == 'ID3':
            ID3V2 = True
            if ord(_tmp_buffer[4]) > 2 and (_tmp_buffer[5] & 0x40) != 0:
                _extend_header = 1
            _ID3V2_length = (ord(_tmp_buffer[6]) & 0x7F << 21) | \
                            (ord(_tmp_buffer[7]) & 0x7F << 14) | \
                            (ord(_tmp_buffer[8]) & 0x7F << 7) | \
                            (ord(_tmp_buffer[9]) & 0x7F)
            _tmp_buffer = f.read(_ID3V2_length - 10)
            _size_left -= _ID3V2_length - 10
        else:
            _file.seek(0)
            ID3V2 = False
        while True:
            _frame = {}
            _tmp_buffer = _file.read(4)
            if _size_left == 0 or _tmp_buffer[:3] == 'TAG':
                break
            _frame_header = (ord(_tmp_buffer[0]) << 24) + \
                            (ord(_tmp_buffer[1]) << 16) + \
                            (ord(_tmp_buffer[2]) << 8) + \
                            ord(_tmp_buffer[3])
            _frame['version_id'] = (_frame_header >> 19) & 0x3
            _frame['lay'] = 4 - (_frame_header >> 17) & 0x3
            _frame['error_protection'] = (_frame_header >> 16) & 0x1
            _frame['bitrate_index'] = (_frame_header >> 12) & 0xF
            _frame['sampling_freq'] = (_frame_header >> 10) & 0x3
            _frame['padding'] = (_frame_header >> 9) & 0x1
            _frame['mode'] = (_frame_header >> 6) & 0x3
            _frame['mode_ext'] = (_frame_header >> 4) & 0x3
            _frame['LSP'] = (lambda x: 0 if x == 3 else 1)(_frame['version_id'])
            _frame['side_info_size'] = 0
            if _frame['lay'] == 1:
                _frame['frame_size'] = TM.bitrate_table[_frame['LSP']][0][_frame['bitrate_index']] * 12000
                _frame['frame_size'] /= TM.sampling_rate_table[_frame['version_id']][_frame['sampling_freq']]
                _frame['frame_size'] = (_frame['frame_size'] + _frame['padding']) << 2
            elif _frame['lay'] == 2:
                _frame['frame_size'] = TM.bitrate_table[_frame['LSP']][1][_frame['bitrate_index']] * 144000
                _frame['frame_size'] /= TM.sampling_rate_table[_frame['version_id']][_frame['sampling_freq']]
                _frame['frame_size'] += _frame['padding']
            elif _frame['lay'] == 3:
                _frame['frame_size'] = TM.bitrate_table[_frame['LSP']][2][_frame['bitrate_index']] * 144000
                _frame['frame_size'] /= (TM.sampling_rate_table[_frame['version_id']][_frame['sampling_freq']] << _frame['LSP'])
                _frame['frame_size'] += _frame['padding']
                if _frame['version_id'] == 3:
                    _frame['side_info_size'] = (lambda x: 17 if x == 3 else 32)(_frame['mode'])
                else:
                    _frame['side_info_size'] = (lambda x: 9 if x == 3 else 17)(_frame['mode'])
            _frame['main_data_size'] = _frame['frame_size'] - 4 - _frame['side_info_size']
            if _frame['error_protection'] == 0:
                _frame['main_data_size'] -= 2
            _frame['data'] = _tmp_buffer + _file.read(_frame['frame_size'] - 4)
            _size_left -= _frame['frame_size']
            # TODO fix the last part of the data
            print "%X" % (_frame_header >> (32 - 11)), _frame['bitrate_index'], _frame['frame_size'], _size_left
            with open(u'test_' + unicode(str(cnt)) + u'.mp3' , 'wb') as _file_out:
                _file_out.write(_frame['data'])
                _file_out.close()
            cnt += 1

if __name__ == '__main__':
    split_mp3(u'test.mp3')
