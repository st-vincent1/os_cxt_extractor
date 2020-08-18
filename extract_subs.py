import xml.etree.ElementTree as ET
import os
import math
import sys
import re


def time_converter(time_str):
    time_str = time_str.replace(',', ':').replace('.', ':').replace(' ', '')
    time_str = re.split(r'[^0-9]', time_str)
    # Bugproofing
    if len(time_str) < 4:
        time_str.append('000')
    try:
        hours, mins, secs, msecs = list(time_str)
    except:
        print("Can't unpack values correctly")
        hours, mins, secs, msecs = ['00','00', '00', '00']
    msecs = int(msecs) + int(hours) * 3600000 + int(mins) * 60000 + int(secs) * 1000

    return msecs


def parse_subtitles(tree_root):
    """
    Extract subtitles from xml files as text
    :param tree_root: root of the xml tree
    :return: subtitles : a dictionary where key is subtitle ID and value is text and timestamps
    """
    time_start = -1
    sub_count = 0
    group_buffer = []
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
                # Assigning time fragments to subs
                stamp = time_start
                for single_sub, sub_id in group_buffer:
                    subtitles[sub_id] = (single_sub, stamp, stamp + fragment - 80)
                    stamp = stamp + fragment + 80
                group_buffer = []
    # Bugproofing: if last sub is not closed
    if group_buffer:
        time_end = time_start + 1000
        duration = time_end - time_start
        fragment = math.floor(duration / sub_count)
        for single_sub, sub_id in group_buffer:
            subtitles[sub_id] = (single_sub, stamp, stamp + fragment - 80)
            stamp = stamp + fragment + 80
        group_buffer = []
    return subtitles


def write_to_file(filename, subs, indices):
    """

    :param filename: name of file to write to
    :param subs: dictionary containing subtitles
    :param indices: a list of idcs (str) to access subtitles from subs
    :return:
    """
    with open(filename, 'a+') as f:
        buffer = ''
        for index in indices:
            try:
                buffer = buffer + subs[index][0]
            except KeyError:
                buffer = buffer + "-"
        f.write(buffer + '\n')
    return


def parse_documents(alignment_filename, pairname, lg1_name, lg2_name):
    """
    Given a file with alignments of subtitles between source and target language, produce contextualised
    sentences in .txt format of overlap of at least 0.9
    :param alignment_filename: file which contains alignment of subtitles and paths to them
    :return:
    """
    print(alignment_filename)
    """
    Part 1: Parse alignments
    """
    align_tree = ET.parse(alignment_filename)
    collection = align_tree.getroot()
    # Identify aligned files
    for document in collection:
        path_to_xml = 'OpenSubtitles/xml'
        path_to_output = 'OpenSubtitles/{}/parsed'.format(pairname)

        lg1_file = os.path.join(os.getcwd(), path_to_xml, document.attrib['fromDoc'][:-3])
        lg2_file = os.path.join(os.getcwd(), path_to_xml, document.attrib['toDoc'][:-3])
        print("Parsing the alignment of \n {} and \n {}...".format(lg1_file, lg2_file))
        cxt_lg1 = None
        cxt_lg2 = None
        cxt_id = None
        pairs_to_parse = []
        for alignment in document:
            # if it is a pair and it has the overlap of at least 0.9
            if 'overlap' in alignment.attrib.keys() and float(alignment.attrib['overlap']) > 0.9:
                lg1, lg2 = alignment.attrib['xtargets'].split(';')
                lg1, lg2 = lg1.split(), lg2.split()
                id = int(alignment.attrib['id'][2:])
                # Check for context; context sentence must exist and it must be the immediate previous sentence
                if cxt_lg1 is not None and id == cxt_id + 1:
                    pairs_to_parse.append((lg1, lg2, cxt_lg1, cxt_lg2))
                cxt_lg1, cxt_lg2, cxt_id = lg1, lg2, id
        """
        Part 2: print context and main sentences to files
        """
        # Parse subtitles from subtitle files
        # Parse source text
        try:
            lg1_tree = ET.parse(lg1_file)
        except:
            print("Error when parsing source file")
            pass
        lg1_root = lg1_tree.getroot()
        lg1_subtitles = parse_subtitles(lg1_root)
        # Parse target text
        try:
            lg2_tree = ET.parse(lg2_file)
        except:
            print("Error when parsing target file")
            pass
        lg2_root = lg2_tree.getroot()
        lg2_subtitles = parse_subtitles(lg2_root)
        for pair in pairs_to_parse:
            lg1, lg2, cxt_lg1, cxt_lg2 = pair
            cxt_time_end, lg1_time_start = lg1_subtitles[cxt_lg1[0]][2], lg1_subtitles[lg1[-1]][1]
            time_difference = lg1_time_start - cxt_time_end
            # Context and source sentence must be within 7 sec distance
            if time_difference < 7000:  # in milliseconds
                write_to_file(os.path.join(os.getcwd(), path_to_output, lg1_name), lg1_subtitles, lg1)
                write_to_file(os.path.join(os.getcwd(), path_to_output, lg2_name), lg2_subtitles, lg2)
                write_to_file(os.path.join(os.getcwd(), path_to_output, '{}.context'.format(lg1_name)), lg1_subtitles, cxt_lg1)
                write_to_file(os.path.join(os.getcwd(), path_to_output, '{}.context'.format(lg2_name)), lg2_subtitles, cxt_lg2)


if __name__ == '__main__':
    l1, l2 = sys.argv[1:3]
    pairname = "{}-{}".format(min(l1, l2), max(l1, l2))
    parse_documents(os.path.join(os.getcwd(), "OpenSubtitles/{}/{}.xml".format(pairname, pairname)), pairname, l1, l2)
