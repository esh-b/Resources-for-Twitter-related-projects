# Resources-for-Twitter-related-projects
This repository contains code which might be required while working on projects related to Twitter data. You could use any module separately or start from processing your raw data (dataset with only Tweet IDs) in sequential order (order to be followed according to the directory's numbering).

### Modules
##### 1. Tweet extraction
##### 2. Group tweets
##### 3. Filtering tweet data
##### 4. Tweet preprocessing
##### 5. Extracting tweet's Noun Chunks
##### 6. Extracting tweet's Named Entities

### Tweet processing steps
* If you just have IDs of the tweets, you could follow the ordering given to the directories. You could start from:
	1. Collecting the tweets from their tweet IDs.
	2. Group collected tweets according to the number of hashtags (optional, needed depending on the project).
	3. Filter all the tweets' data from the tweet dump and put them in an organized format (CSV).
	4. Preprocess the tweet text (like removing emojis, usermentions, urls, text processing etc) before actually starting to work on your project.
	5. Extract the `noun chunks` from the processed tweet text (optional, depends on the project).
	6. Extract the `named entities` from the processed tweet text (optional, depends on the project).

### Requirements
* All the codes were written and tested on `python3.5.2`.
* The modules required to run the codes are put in the `requirements.txt` file.
* The modules can be installed by using the command `pip -r install requirements.txt`. Make sure to use `sudo` incase you are installing the modules in the root system (i.e. when not using `virtualenv`).
* Additional requirements for `tweet_preprocessing` task:
	* The `tweet_preprocessing_part2` task requires the `wordseg` module which can be installed only from source.
	* To install `wordseg` from source, goto the wordseg [homepage][https://github.com/jchook/wordseg] and clone or download the project.
	* Then, `cd` into cloned directory and run the command `python setup.py install`. This will successfully install the `wordseg` module.
* Additional requirements for `Spacy` module (`extract_noun_phrases` task):
	* The Spacy module requires the `en` ML model to be downloaded before using it. So, install it using the command `python -m spacy download en` before using spacy module.

### Future work
* We could extract additional information about the tweet content from the web using the tweet's noun phrases and named entities. I will add those codes later.

### Note
* Please read the modules' corresponding README files before running the code.
* Please feel free to play around with the code and send a PR incase you want to add any other module related to Twitter projects or you want to improve the existing modules.