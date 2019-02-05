# Resources-for-Twitter-related-projects
This repository contains code which might be required when working on projects related to Twitter data.

### Requirements
* The modules required to run the codes are put in the `requirements.txt` file.
* The modules can be installed by using the command `pip -r install requirements.txt`. Make sure to use `sudo` incase you are installing the modules in the root system (i.e. when not using `virtualenv`).
* Additional requirements for `tweet_preprocessing` task:
	* The `tweet_preprocessing_part2` task requires the `wordseg` module which can be installed only from source.
	* To install `wordseg` from source, goto the wordseg [homepage][https://github.com/jchook/wordseg] and clone or download the project.
	* Then, `cd` into cloned directory and run the command `python setup.py install`. This will successfully install the `wordseg` module.
* Additional requirements for `Spacy` module (`extract_noun_phrases` task):
	* The Spacy module requires the `en` ML model to be downloaded before using it. So, install it using the command `python -m spacy download en` before using spacy module.
* Additional requirements for `twitterNLP` module (`extract_entities` task):
