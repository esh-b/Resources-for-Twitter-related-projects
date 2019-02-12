# Tweet data extraction from Tweet IDs
* This module shows the method to extract the tweet content given the tweet ID.
* `History`: In general, people share only tweet IDs while sharing tweet datasets (owing to Twitter restrictions). So, users have to extract the tweet data from tweet IDs before starting to work on their Twitter-based project.

### Steps to run the code
* All the codes were written in `python3`.
* The `Twarc` module (used in the code to retrieve tweet data) internally uses Twitter API to extract the tweet data from tweet IDs. Twarc requires the Twitter app credentials before you can run the program. You will have to create an app in the Twitter developer console and copy the app credentials in the `twitter_app_config.py` file before running the code. 
* The code `extract_tweets.py` can be run using the command `python extract_tweets.py <INPUT_FILEPATH>`. The `INPUT_FILEPATH` must be a file where every row is assumed to contain a tweet ID. See the sample input (in the `input` directory).
