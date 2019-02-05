# Getting Noun chunks using the spacy module

The spacy module has methods to extract noun chunks from any given sentence. The noun chunks are different from noun phrases in that noun chunks are "base noun phrases" – flat phrases that have a noun as their head (according to spacy). For further details, [click here](https://spacy.io/usage/linguistic-features#noun-chunks).

# Why spacy?
Spacy is an active open-source project which provides methods for entity and noun phrase extractions, pos tagging and so on. It has support for even training custom models (tokenizers, taggers etc.). For our purpose, spacy is found to recognise the noun phrases from any given text with good accuracy.

# Steps to run the code
- The spacy noun phrase extraction code was written in Python3.
- The program can be run using the command ```python3 spacyNP.py```
- This will read the output files from the previous directory and generate a file with tweet IDs and the corresponding noun phrases in the text of that tweet.

### Noun phrase extraction using `Spacy` module
* The file `extract_spacy_np.py` extracts the noun phrases for the given set of texts and writes them onto a new CSV file.
* The code was written in `python2`. The code can be run using the following command `python extract_spacy_np.py <INPUT_FILEPATH> <COLUMN_NUMBER_CONTAINING_TEXT>"`.
* **Input file format:**
    *  The input file is expected to be a CSV file where the first column is assumed to be the `tweet_id`.
    *  Also, suppose the column number containing text (for which the noun phrases have to be extracted) is `X` (X > 1 since X=1 means the tweet_id column). Then the number `X` must be given as an argument (<COLUMN_NUMBER_CONTAINING_TEXT>) while running the code.
* **Output file format:**
    * Once the code is run, it will create a new file `<INPUT_FILE_NAME>_spacyNP.csv` where INPUT_FILE_NAME was the filename given as argument to the code.
    * The output CSV contains two columns: `tweet_id` and `spacy_np`. Every row contains the tweet_id and the corresponding text's extracted noun phrases.
    * Note that the text for a single tweet_id may contain multiple noun phrases. Every noun phrase of a given text is delimited by the `$$$` symbol.
    * E.g. If one of the input row (from the input file) has `tweet_id` as 123 and text as "I want a skate board and Apple ipad", then the output file will have a row with `tweet_id` as 123 and `spacy_np` column value as "skate board$$$Apple ipad$$$". Here, the two noun phrases are delimited by `$$$` symbol.
