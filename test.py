import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import os
import math
import pprint as pp

"""
Parsing .xml overlap file
"""


def time_converter(time_str):
    time_str = time_str.replace(',', ':')
    time_str = time_str.split(':')
    hours, mins, secs, msecs = list(time_str)
    msecs = int(msecs) + int(hours) * 3600000 + int(mins) * 60000 + int(secs) * 1000
    return msecs


def parse_subtitles(tree_root):
    time_start = -1
    time_end = -1
    sub_count = 0
    single_buffer = ''
    group_buffer = []
    group_id = None
    # Making a nan array to store subs
    subtitles = dict()
    for sub in tree_root:
        if sub.tag == 's':
            # Check for time start
            if sub[0].tag == 'time':
                time_start = time_converter(sub[0].attrib['value'])
                sub_count = 1
            else:
                sub_count += 1
            if sub[-1].tag == 'time':
                time_end = time_converter(sub[-1].attrib['value'])
            else:
                time_end = -1
            # Collecting subtitles
            single_buffer = ""
            for element in sub:
                if element.tag == 'w':
                    single_buffer = single_buffer + ' ' + element.text
            group_buffer.append((single_buffer, sub.attrib['id']))
            # Subtitles collected. Flush with time stamps if done
            if time_end != -1:
                duration = time_end - time_start
                fragment = math.floor(duration / sub_count)
                # print("CLEARING GROUP BUFFER")
                # print(group_buffer)
                # Assigning time fragments to subs
                stamp = time_start
                for single_sub, sub_id in group_buffer:
                    subtitles[sub_id] = (single_sub, stamp, stamp + fragment - 80)
                    stamp = stamp + fragment + 80
                group_buffer = []
                single_buffer = ''
    return subtitles


def write_to_file(filename, subs, indices):
    with open(filename, 'a+') as f:
        buffer = ''
        for index in indices:
            buffer = buffer + subs[index][0]
            print(buffer)
        f.write(buffer + '\n')
    return
align_tree = ET.parse("datasets/align_en_pl_sample.xml")
collection = align_tree.getroot()
overlap_index = dict()
for document in collection:
    src_file = os.path.join(os.getcwd(), 'datasets/OpenSubtitles/xml', document.attrib['fromDoc'][:-3])
    tgt_file = os.path.join(os.getcwd(), 'datasets/OpenSubtitles/xml', document.attrib['toDoc'][:-3])
    print(src_file)
    cxt_src = None
    cxt_tgt = None
    cxt_id = None
    pairs_to_parse = []
    for alignment in document:
        # overlap_index[['381'],['288', '289']]
        if 'overlap' in alignment.attrib.keys() and float(alignment.attrib['overlap']) > 0.9:
            src, tgt = alignment.attrib['xtargets'].split(';')
            src, tgt = src.split(), tgt.split()
            id = int(alignment.attrib['id'][2:])
            # Check for context; context sentence must exist and it must be the immediate previous sentence
            if cxt_src is not None and id == cxt_id + 1:
                pairs_to_parse.append((src, tgt, cxt_src, cxt_tgt))
            cxt_src, cxt_tgt, cxt_id = src, tgt, id
    # Parse subtitles from subtitle files
    # Parse source text
    src_tree = ET.parse(src_file)
    src_root = src_tree.getroot()
    # Parse using the original script; input: subtitle file. output: a list of subtitles with ID, text, time info
    """
    List must look something like this...
    0 : None # None is if there were no subs with this id
    1 : ['You like curry , right ?', 44054, 44705]
    
    
    """
    src_subtitles = parse_subtitles(src_root)
    pp.pprint(src_subtitles)
    # Parse target text
    tgt_tree = ET.parse(tgt_file)
    tgt_root = tgt_tree.getroot()
    tgt_subtitles = parse_subtitles(tgt_root)
    for pair in pairs_to_parse:
        # Can't find the 11. but it is in pairs to parse; it isn't in the dictionary
        src, tgt, cxt_src, cxt_tgt = pair
        cxt_time_end, src_time_start = src_subtitles[cxt_src[0]][2], src_subtitles[src[-1]][1]
        time_difference = src_time_start - cxt_time_end
        # Context and source sentence must be within 7 sec distance
        if time_difference < 7000: # in milliseconds
            write_to_file('src.txt', src_subtitles, src)
            write_to_file('tgt.txt', tgt_subtitles, tgt)
            write_to_file('cxt_src.txt', src_subtitles, cxt_src)
            write_to_file('cxt_tgt.txt', tgt_subtitles, cxt_tgt)
        # print(src_subtitles[src[0]])

        # Add to files
