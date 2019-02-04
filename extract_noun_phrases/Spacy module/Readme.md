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

