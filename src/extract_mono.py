import xml.etree.ElementTree as ET
import os
import sys
import glob
from pprint import pprint
from utils import *


def parse_xml(lang):
    """
    The path is like this:
    xml -> directory -> directory -> xml files

    """
    path_to_xml = os.path.join(os.getcwd(), f'../data/OpenSubtitles/xml/{lang}')

    out_dir = f'../data/{lang}'
    out_file = f'mono.{lang}'

    for xml_filename in glob.iglob(rf'{path_to_xml}/*/*/*.xml'):
        xml_tree = ET.parse(xml_filename)
        subtitles = parse_subtitles(xml_tree.getroot(), return_type=list)
        documents = []
        cur_doc = subtitles[0][0]
        """ sub, start_stamp, end_stamp """
        for k in range(1, len(subtitles)):
            _, prev_start, prev_end = subtitles[k - 1]
            cur_sub, cur_start, cur_end = subtitles[k]
            if cur_start - prev_end < 7000:
                cur_doc = cur_doc + " __BR__ " + cur_sub
            else:
                if len(cur_doc.split("__BR__")) > 1:  # one-sentence documents don't count
                    documents.append(cur_doc)
                cur_doc = cur_sub
        documents.append(cur_doc)

        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        with open(os.path.join(out_dir, out_file), 'a+') as f:
            for line in documents:
                f.write(line + '\n')


if __name__ == '__main__':
    lang = sys.argv[1]
    parse_xml(lang)
