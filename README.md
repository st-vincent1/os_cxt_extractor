Extracting OpenSubtitles18 data for Context-Aware NMT
======
General information
------
This parser extracts parallel subtitles for any language pair (listed below) from the OpenSubtitles18 corpus [OpenSubtitles18 corpus page](http://opus.nlpl.eu/OpenSubtitles-v2018.php). This dataset is a scrape of TV and movie subtitles available at http://www.opensubtitles.org/.

Guidelines for selecting subtitles are aligned with Voita et al. (2018) and consist of the following:
1. Each sentence pair is coupled with the sentence which provides context for that pair, i.e. the immediate previous sentence spoken. Voita et al. (2018) use only source side context (English, in their case) but for completeness the present script extracts both source- and target-side context.
2. Some cleaning is done on the dataset. The subtitles are extracted according to the alignment file (usually called align-$src-$tgt.xml), so that rather than many-to-many mappings there is always a sentence-to-sentence mapping. The .xml file provides overlap statistics for alignment and alignments with overlap below 0.9 are not considered for extraction.
3. For context, pairs of consecutive sentences with a break between them of more than 7 seconds are not considered.

Example: running for EN and FR
------
1. Clone the repository.
2. Navigate to the repository.
3. Type `./run.sh en fr`. The order of languages doesn't matter.
    - The script runs `download.sh` which downloads subs from the website, `extract_subtitles.py` which extracts the subtitles from xml files, aligns and filters them and `prepare_dataset.py` which compiles them into a usable train/dev/test split.
    - By nature the procedures are bidirectional, at train time you may specify the source and target languages and adjust context files accordingly (e.g. if you want to only use source context). 
4. Once the script is done, the files are saved in the following hierarchy:
```
OpenSubtitles
|-xml
| |-en
| |-fr
|-en-fr
| |-en-fr.xml
| |-parsed
| | |-raw sentences...
| |-cxt_dataset
| | |-train, dev, test files...
```

Available languages
------
The scripts should work for any language pair available for download on the [OpenSubtitles18 corpus page](http://opus.nlpl.eu/OpenSubtitles-v2018.php).


References
------

Lison, P. and Tiedemann, J. (2016) 'OpenSubtitles2016: Extracting Large Parallel Corpora from Movie and TV Subtitles.', In Proceedings of the 10th International Conference on Language Resources and Evaluation (LREC 2016).

Voita, E. et al. (2018) ‘Context-aware neural machine translation learns anaphora resolution’, ACL 2018 - 56th Annual Meeting of the Association for Computational Linguistics, Proceedings of the Conference (Long Papers), 1, pp. 1264–1274.
