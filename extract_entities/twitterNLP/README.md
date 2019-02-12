# Extracting Named Entities and Noun phrases from `twitter_nlp` module
* The `twitter_nlp` module([source](https://github.com/aritter/twitter_nlp)) can be used to extract noun phrases and named entities from the tweet text. The module is expected to work well in general for Twitter text data.

### Steps to run the code
* Open a terminal and run the command `export TWITTER_NLP=<TWITTER_NLP_CLONE_PATH>`. Here, the clone path is the path of the twitter_nlp_clone directory which contains all the dependencies. E.g. Running `export TWITTER_NLP=./twitter_nlp_clone` from the `twitterNLP` module directory will add the `twitter_nlp_clone` dir path to the sys path. Note that there must not be any leading `/` at the end of the directory path. If the code is run without exporting the `twitter_nlp_clone` path, then the code will throw out errors like `ImportError: No module named 'extractEntities'`.
* Then, the `extract_twitterNLP_np.py` (written in `python3`) can be run using the command `python extract_twitterNLP_np_entities.py <INPUT_FILEPATH> <COLUMN_NUMBER_CONTAINING_TEXT>`.

### Python compatibility
* The `extract_twitterNLP_np.py` code was written in `python3` **BUT** the `twitter_nlp` module (from the source) was written in `python2`. 
* To add compatibility for `python3`, I have modified few files in the original `twitter_nlp` module and added the resulting `twitter_nlp` module directory in this repo.
* If you are about to replace the current `twitter_nlp` directory (containing the dependencies) in this repo with any future version from the source `twitter_nlp` repo, make sure to modify the files so that it is compatible with `python3`.