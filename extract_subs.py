# -*- coding: utf-8 -*-
import math


"""
tree = ET.parse('sample_xml.xml')
root = tree.getroot()

for child in root:
    print(child.tag, child.attrib)

[elem.tag for elem in root.iter()]
# print(ET.tostring(root, encoding='utf8').decode('utf8'))


for movie in root.iter('movie'):
    print(movie.attrib)

for description in root.iter('description'):
    print(description.text)

# Trying out with subs

tree = ET.parse('sub.xml')
root = tree.getroot()

# s for subtitle, w for word

for sub in root:
    # New sub; reset timestamps & strings.
    # for element in sub:
    #   print(sub.attrib)
    if sub.tag == 's':
        if (sub.attrib['id'] == '514'):
            for element in sub:
                print(element.tag)
            time_start = sub[0].attrib['value']
            # time_end = sub[-1].attrib['value']
            print(time_start)
        #
        # print(word.tag, word.attrib, word.text)

print(ET.tostring(root, encoding='utf8').decode('utf8'))
"""
"""Types of situations:
1. Subtitle starts, TS, subtitle, TE, subtitle ends
    Expected outcome: standard case, assign TE-TS to subtitle
2. Subtitle starts, TS, subtitle, subtitle ends, another subtitle starts, subtitle, TE, subtitle ends  (can repeat n times)
    Expected outcome: Split into however many distinct subtitles there are, then broadcast time across them uniformly.
3. Subtitle starts, TS, subtitle, TE,  TS, subtitle, TE, subtitle ends (can repeat n times)
    Expected outcome: intermittent timestamps ignored.

There are 3 different situations because the TS-TE is the time of showing 
a subtitle on screen while the subtitle start and end is the sentence.
What I want is to extract the subtitle as a unit regardless of how it's shown
on screen.

w = tokens; the data is already tokenised.

I need to extract the data so that each subtitle is in its own line and has a timestamp to it.  


"""
"""
Testing
Example #1:
s
  time start
  w
  w
  w
  time end
\s

time_start = time start
sub_count = 1
time_end = time end
sub_text collects all words
split time across subs (1 time only so no splitting)
time assigned to subtitle
single buffer cleared to group buffer
group buffer cleared to collection
TEST SUCCESSFUL

Example #2:
s
  time start
  w
  w
  w
\s
s
  w
  w
  w
  time end
\s

time_start = time start
sub_count = 1
time_end = -1
sub_text contains all words from 1st sub

sub_count = 2
sub_text cleared to group buffer
sub_text empty
time_end = time end
sub_text contains all words from 2nd sub
split time across subs; 2 subs so:
e.g. if time_start = 5, time_end = 10
sub1: time_start = 5, time_end = 7.5-70ms
sub2: time_start = 7.5 + 70ms, time_end = 10
sub2 to group buffer
group buffer to collection

TEST SUCCESSFUL

Example #3:
s
  time start1
  w
  w
  time end1
  time start2
  w
  w
  w
  time end2
\s

time_start = time start1
time_end = time end2
other time stamps simply ignored.

TEST SUCCESSFUL



Pseudocode:

for subtitle in xml:
  take first and last element.
  if first is time:
    assign time to time_start
    sub_count = 1
  else:
    we're in a previous show; time_start stays
    sub_count +=1
    clear single_buffer to group_buffer
    start a new sub_text
  if last is time:
    assign time to time_end
  else:
    this show will continue. time_end = -1

  for element in subtitle:
    if word: # only want to read words, ignore the rest
      add word to sub_text
  # All words in subtitle parsed.
  if time_end: # we're finished with this time now
    split time across subs (#subs = sub_count) and create time stamps, assign start and end time to each subtitle (for overlap check)
      duration = time_end - time_start
      piece = duration / sub_count

      #assign stamps to subs
      stamp = time_start
      for sub in group_subs:
        sub[start] = stamp
        sub[end] = stamp + piece - 80ms
        stamp = stamp + piece + 80ms

    clear single buffer to group buffer
    clear group buffer for collection
  if time_end == -1:
    will check out itself; do nothing

"""


def time_converter(time_str):
    time_str = time_str.replace(',', ':')
    time_str = time_str.split(':')
    hours, mins, secs, msecs = list(time_str)
    msecs = int(msecs) + int(hours) * 3600000 + int(mins) * 60000 + int(secs) * 1000
    return msecs


def extract_subtitles(subs_xml):
    time_start = -1
    time_end = -1
    sub_count = 0
    single_buffer = ''
    group_buffer = []
    for sub in src:
        if sub[0].tag == 'time':
            time_start = time_converter(sub[0].attrib['value'])
            sub_count = 1
        else:
            sub_count += 1

        # Clearing single_buffer for new text
        single_buffer = ''
        if sub[-1].tag == 'time':
            time_end = time_converter(sub[-1].attrib['value'])
        else:
            time_end = -1
        # Collecting subtitles
        for element in sub:
            if element.tag == 'w':
                single_buffer = single_buffer + ' ' + element.text
        group_buffer.append(single_buffer)
        # Subtitles collected. Flush with time stamps if done
        if time_end != -1:
            print(time_end)
            duration = time_end - time_start
            fragment = math.floor(duration / sub_count)
            # print("CLEARING GROUP BUFFER")
            # print(group_buffer)
            # Assigning time fragments to subs
            stamp = time_start
            for single_sub in group_buffer:
                collection.append((single_sub, stamp, stamp + fragment - 80))
                stamp = stamp + fragment + 80
            group_buffer = []
    return subs_txt


def parse_subtitles(src, tgt):
    """
    Given src and tgt subs in xml format, extract the actual subtitles and time stamps
    :param root:
    :return:
    """

    # Capturing time stamps
    parsed_src = extract_subtitles(src)
    parsed_tgt = extract_subtitles(tgt)

    return parsed_src, parsed_tgt


"""
1. Open .ids file
2. Open .xml alignment file
Read line 1, and take both file names.
will try to use df and numpy for this. 
while file1 != read_file1 and file2 != read_file2:
    ASSUME IDS ARE PARSED AND AS LISTS
    overlap = #extract from xml file
    if overlap > 0.9:
        
        src_txt = ''
        for id in id_src:
            txt_src += file1(where id == id))
            txt_src += '\n'
        for id in id_tgt:
            txt_tgt += file1(where id == id))
            txt_tgt += '\n'
        
        # Parse subtitles from xml to text format
        parsed_src, parsed_tgt = parse_subtitles(src, tgt)
        if cxt_src and cxt_tgt:
            if dist(cxt_src, parsed_src) < 7000: # Distance in msec
                update_collection(cxt_src, cxt_tgt, parsed_src, parsed_txt)
        cxt_src = parsed_src
        cxt_tgt = parsed_tgt
        
    #Read next line
    line = f.readline().split("   ") # or something, maybe if we use dataframe I won't need to do that
    # Below needs investigation
    read_file2 = read from next line
    read_file1 = read from next line
    id_src = read
    id_tgt = read

"""

