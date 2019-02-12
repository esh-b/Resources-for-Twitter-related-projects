### Filter Tweet Metadata
* The file `filter_tweet_data.py` extracts the data for every tweet in the tweet_dump file and writes them onto a CSV file (in an organized way).
* The code was written in `python2` and can be run using the command `python filter_tweet_data.py <TWEET_DUMP_FILEPATH>`
* **Input file format:**
	* The code assumes that every line if the input file contains the JSON dump of a tweet (obtained from the Twarc module - described in `tweet_extraction` module).
	* **E.g.** Line 1 of the input file contains `{'tweet_id': 123456789, ....}` which is the JSON dump of the tweet with tweet_id `123456789`.
* **Output file format:**
	* The output file has the filename `<TWEET_DUMP_FILENAME>_data.csv` (The TWEET_DUMP_FILENAME containing the tweet dump is extracted automatically from the filepath).
	* The output CSV file has the following columns:
		* `tweet_id` - Tweet ID
		* `tweet_date` - Tweet posted date
		* `tweet_favCount` - Favourite count for the tweet (till the time tweet was extracted using Twitter API)
		* `tweet_RTCount` - Retweet count for the tweet (till the time tweet was extracted using Twitter API)
		* `tweet_text` - The actual tweet text
		* `hashtagsStr` - All the hashtags of a tweet are delimited by `$$$`
		* `usermentionsStr(screen_name#$#name$$$)` - All the usernames mentioned in the tweet are delimited by `$$$` while for a particular user, the screen_name and the actual name is delimited by `#$#`.
		* `urlsStr(url#$#expanded_url$$$)` - All the URLs mentioned in the tweet are delimited by `$$$` while for a particular URL, the mentioned URL (short URL) and the expanded URL is delimited by `#$#`.
		* `hashtags_jsondump` - JSON dump of the `hashtags` key.
		* `usermentions_jsondump` - JSON dump of the `usermentions` key.
		* `urls_jsondump` - JSON dump of the `urls` key.
		* `user_id` - ID of the user who posted the tweet.
		* `user_name` - User name.
		* `user_since` - Twitter user since.
		* `user_utcoffset` - User's location offset
		* `user_description` - User profile description.
		* `user_verified` - Whether this user is a verified profile.
		* `user_listedCount` - The number of public lists that the user is a member of.
		* `user_follCount` - The number of followers this user currently has.
		* `user_statusesCount` - The number of Tweets (including retweets) issued by this user.
		* `user_friendsCount` - The number of users this user is following (AKA their "followings").
		* `user_favoritesCount` - The number of Tweets this user has liked in the account’s lifetime.
* **Applications:**
	* **1. Hashtag Recommendation:**
		* Incase of an hashtag recommendation system for Twitter, apart from just considering the text to recommend hashtags, the user history can also be considered while recommending hashtags.
		* Intuition: The intuition behind it is that a popular user will have many followers on the network. So, all the hashtags used by him/her will be known by many people and it's highly likely that people will use the same hashtags. So, I planned to prioritize those hashtags which have been used by popular users in our algorithm.
		* **Tip:** One example of using the above data is checking whether a hashtag has been used by any verified user (```user_verified``` attribute) and thereby giving higher priority to those hashtags. Another alternative is to rank users based on the number of friends and followers count and prioritize the hashtags used by people in higher ranks.