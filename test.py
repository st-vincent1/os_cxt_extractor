import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import os

"""
Parsing .ids file
"""
# df = pd.read_csv('datasets/OpenSubtitles.en-pl.ids_sample.txt', delimiter='	', header=None)
# df.columns = ['Source file', 'Target file', 'Source ID', 'Target ID']
#
# df = df.to_numpy()
# NUM_COL_SRC_ID = 2
# NUM_COL_TGT_ID = 3
# for num_col in range(NUM_COL_SRC_ID, NUM_COL_TGT_ID+1):
#     for num_row in range(len(df)):
#         df[num_row][num_col] = [s for s in df[num_row][num_col].split()]
#


"""
Parsing .xml overlap file
"""

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
        if 'overlap' in alignment.attrib.keys() and float(alignment.attrib.keys['overlap']) > 0.9:
            src, tgt = alignment.attrib['xtargets'].split(';')
            src, tgt = src.split(), tgt.split()
            id = int(alignment.attrib['id'][2:])
            # Check for context; context sentence must exist and it must be the immediate previous sentence
            if cxt_src is not None and id == cxt_id+1:
                pairs_to_parse.append((src, tgt, cxt_src, cxt_tgt))
            cxt_src, cxt_tgt, cxt_id = src, tgt, id





            overlap = alignment.attrib['overlap']
            overlap_index[src[0]] = (src, tgt, overlap)
    # Parse subtitles from subtitle files
    src_tree = ET.parse(src_file)
    tgt_tree = ET.parse(tgt_file)
    # Need to investigate the 7 second rule

