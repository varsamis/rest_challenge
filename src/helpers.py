"""
Helper methods
"""
import json
import csv

def process_file(file_name, ext):
    if ext == 'json':
        return f'{file_name}.{ext}'
    return f'{file_name}.{ext}'
