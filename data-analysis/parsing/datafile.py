#   Copyright (C) 2019 Hockey Player Tracking Inc. - All Rights Reserved
#   Unauthorized copying of this file, via any medium is strictly prohibited.
#
#   Author: Taylor Dean

''' Data file parser. '''

import re

FIRMWARE_HEADER_REGEX_PATTERN = 'Firmware v'
COLUMN_NAME_HEADER_REGEX_PATTERN = '<([a-zA-Z]+)>'


class Parser():
    '''
    Parse a data file into memory.
    '''

    def __init__(self, filepath):
        ''' Parser constructor. '''

        self.filepath = filepath
        self._file = open(filepath, 'r')
        self.header_regex = re.compile(COLUMN_NAME_HEADER_REGEX_PATTERN)

    def parse(self):
        ''' Parse the file to a data object. '''

        # Sets the file pointer to the column header line.
        # Next line is start of data.
        header_names = self._get_header_column_names()
        line = self._file.readline().rstrip()
        data = []

        while(line):
            vals = line.split(',')

            entries = {header_names[i]: vals[i] for i in range(0, len(vals))}
            row = DataRow(entries)
            data.append(row)
            line = self._file.readline().rstrip()

        return data

    def _get_header_column_names(self):
        ''' Get the column names from the header. '''

        self._reset_file_pointer()
        match = None
        line = self._file.readline()

        while((match is None) and line):
            line = self._file.readline()
            match = self.header_regex.search(line)

        if (match is None):
            raise RuntimeError('No match found for header pattern.')

        header_names = self.header_regex.findall(line)
        return header_names

    def _reset_file_pointer(self):
        ''' Move the file pointer back to the start of the file. '''
        
        self._file.seek(0)


class DataRow():
    '''
    A single row of data in the data file.
    '''

    def __init__(self, entries):
        ''' Data row constructor. '''

        for key, value in entries.items():
            setattr(self, key, value)
