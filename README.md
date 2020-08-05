sub_extractor
======
General information
------
This parser extracts parallel subtitles for any language pair (listed below) from the OpenSubtitles18 corpus[add link].

Guidelines for selecting subtitles are aligned with Voita et al. 18 and consist of the following:
1. Each sentence pair is coupled with the sentence which provides context for that pair, i.e. the immediate previous sentence spoken. Voita et al. 18 use only source side context (English, in their case) but for completeness the present script extracts both source- and target-side context.
2. Some cleaning is done on the dataset. The subtitles are extracted according to the alignment file (usually called align-$src-$tgt.xml), so that rather than many-to-many mappings there is always a sentence-to-sentence mapping. The .xml file provides overlap statistics for alignment and alignments with overlap below 0.9 are not considered for extraction.
3. For context, pairs of consecutive sentences with a break between them of more than 7 seconds are not considered.

Running
------
Install requirements.
If you haven't already downloaded OpenSubtitles, run the download script:
```bash runs/download.sh pl ru```
If you have downloaded the subtitles before, run the next script providing the path to them. If not, the script will load the downloaded subtitles by default.
```bash runs/extract.sh path```
(Make sure your path directory looks like this:
```path (e.g. OpenSubtitles)
|-xml
| |-pl
| |-en
|align.xml
```
The subtitles will be extracted and stored in `path/out`.

Available languages
------
The scripts should work for any language pair available for download on OpenSubtitles, but were only tested on the selected few.
Below is the table of language pairs available from OpenSubtitles. In bold are the pairs tested for. If the scripts don't work for your selected pair, please get in touch.
