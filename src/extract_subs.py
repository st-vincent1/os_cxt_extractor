import xml.etree.ElementTree as ET
import os
import sys

from utils import *

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
        try:
            lg1_tree = ET.parse(lg1_file)
            lg1_root = lg1_tree.getroot()
            lg1_subtitles = parse_subtitles(lg1_root)
            lg2_tree = ET.parse(lg2_file)
            lg2_root = lg2_tree.getroot()
            lg2_subtitles = parse_subtitles(lg2_root)
        except FileNotFoundError:
            print("Error when parsing source file")
            continue

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
    l1, l2 = min(l1, l2), max(l1, l2)
    pairname = "{}-{}".format(l1, l2)
    parse_documents(os.path.join(os.getcwd(), "OpenSubtitles/{}/{}.xml".format(pairname, pairname)), pairname, l1, l2)
