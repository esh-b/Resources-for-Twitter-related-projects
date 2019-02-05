# Grouping tweets based on the number of hashtags

For the purpose of hashtag recommendation for tweets, all the tweets with 2 to 4 hashtags were considered as training dataset. It is said that the tweet engagement really decreases when the number of hashtags in the tweet is more than 2 ([source](https://blog.bufferapp.com/a-scientific-guide-to-hashtags-which-ones-work-when-and-how-many)). So, we tried to extract all the tweets containing 2 hashtags. Since the number of tweets containing 2 hashtags were less in number, we also considered tweets with 3 and 4 hashtags. 
> Tip: If you are about work on recommending hashtags for Twitter, you may want to have precision-2 as the validation metric as it will help to recommend accurate hashtags while also helps in user engagement.


# The code
- The code which groups the tweets based on the number of hashtags was written in python2.
- It takes the output of the previous directory as input (```news_outlets.jsonl```) and generates 3 files: tweets containing 1 hashtag (```news_outlets_1h.jsonl```), tweets containing 2, 3 and 4 hashtags (```news_outlets_234h.jsonl```) and another file containing tweets with no hashtags or greater than 5 hashtags (```news_outlets_other.jsonl```). For my purpose, I considered only the dataset containing tweets with 2 or 3 or 4 hashtags.