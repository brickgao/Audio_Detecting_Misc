# -*- coding: utf-8 -*-

import os
import TableMisc as TM

class MP3Decode:
    
    def __init__(self, path):
        
        self.path       = path
        self.ID3V1      = False
        self.ID3V2      = False
        self.f          = open(self.path, 'rb')
        self.file_size  = os.path.getsize(self.path)
        self.frame_list = []

        
    def get_frame(self):
        
        _size_left  = self.file_size
        _tmp_buffer = self.f.read(10)
        # Skip ID3V2 tag If there is
        if _tmp_buffer[:3] == 'ID3':
            self.ID3V2    = True
            if ord(_tmp_buffer[4]) > 2 and (_tmp_buffer[5] & 0x40) != 0:
                _extend_header = 1
            _ID3V2_length = (ord(_tmp_buffer[6]) & 0x7F << 21) | \
                            (ord(_tmp_buffer[7]) & 0x7F << 14) | \
                            (ord(_tmp_buffer[8]) & 0x7F << 7)  |\
                            (ord(_tmp_buffer[9]) & 0x7F)
            _tmp_buffer   = self.f.read(_ID3V2_length)
            _size_left -= _ID3V2_length - 10
        else:
            self.f.seek(0)
        while True:
            _frame      = {}
            _tmp_buffer = self.f.read(4)
            if _tmp_buffer[:3] == 'TAG':    break
            _frame_header = (ord(_tmp_buffer[0]) << 24) + \
                            (ord(_tmp_buffer[1]) << 16) + \
                            (ord(_tmp_buffer[2]) << 8) + \
                             ord(_tmp_buffer[3])
            if _size_left == 0:             break
            _frame['version_id']       = (_frame_header >> 19) & 0x3
            _frame['lay']              = 4 - (_frame_header >> 17) & 0x3
            _frame['error_protection'] = (_frame_header >> 16) & 0x1
            _frame['bitrate_index']    = (_frame_header >> 12) & 0xF
            _frame['sampling_freq']    = (_frame_header >> 10) & 0x3
            _frame['padding']          = (_frame_header >> 9) & 0x1
            _frame['mode']             = (_frame_header >> 6) & 0x3
            _frame['mode_ext']         = (_frame_header >> 4) & 0x3
            _frame['LSP']              = (lambda x: 0 if x == 3 else 1)(_frame['version_id'])
            _frame['side_info_size']   = 0
            if _frame['lay'] == 1:
                _frame['frame_size']  = TM.bitrate_table[_frame['LSP']][0][_frame['bitrate_index']] * 12000
                _frame['frame_size'] /= TM.sampling_rate_table[_frame['version_id']][_frame['sampling_freq']]
                _frame['frame_size']  = (_frame['frame_size'] + _frame['padding']) << 2
            elif _frame['lay'] == 2:
                _frame['frame_size']  = TM.bitrate_table[_frame['LSP']][1][_frame['bitrate_index']] * 144000
                _frame['frame_size'] /= TM.sampling_rate_table[_frame['version_id']][_frame['sampling_freq']]
                _frame['frame_size'] += _frame['padding']
            elif _frame['lay'] == 3:
                _frame['frame_size']  = TM.bitrate_table[_frame['LSP']][2][_frame['bitrate_index']] * 144000
                _frame['frame_size'] /= (TM.sampling_rate_table[_frame['version_id']][_frame['sampling_freq']] << _frame['LSP'])
                _frame['frame_size'] += _frame['padding']
                if _frame['version_id'] == 3:
                    _frame['side_info_size'] = (lambda x: 17 if x == 3 else 32)(_frame['mode'])
                else:
                    _frame['side_info_size'] = (lambda x: 9 if x == 3 else 17)(_frame['mode'])
            _frame['main_data_size'] = _frame['frame_size'] - 4 - _frame['side_info_size']
            if _frame['error_protection'] == 0:     _frame['main_data_size'] -= 2
            _frame['data'] = self.f.read(_frame['frame_size'] - 4)
            self.frame_list.append(_frame)
            _size_left -= _frame['frame_size']
            print _frame['frame_size'], _frame['version_id'], _frame['lay'], _frame['sampling_freq']
            # TODO fix the last part of the data
            if _size_left <= 128:     break


if __name__ == '__main__':
    _ = MP3Decode(u'brush_synth.mp3')
    _.get_frame()
    print 'done'
