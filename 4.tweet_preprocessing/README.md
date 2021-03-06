# Tweet preprocessing
Tweets in general do not have good sentence structure (users use contractions, emojis etc. to express their thoughts). So, its important to preprocess these tweets correctly so as to use the text to recommend hashtags accurately.

### Terminologies
* ***Usermentions:*** Twitter users tag other users in their tweets while discussing about any topic concerning others. These are denoted by ```@username``` in the tweet. These are called `usermentions`.

### Preprocessing stages
* I have split the preprocessing phase of the tweets into two parts:
  * **Part 1**: The usermentions and hashtags which are not part of the sentence are discarded. Also, urls and emojis are discarded.  
  * **Part 2**: The major processing in this part is that all the hashtags and usermentions which are part of the sentence are converted to word forms (like #independenceday becomes independence<SPACE>day and @trump becomes Donald<SPACE>Trump). Also, all contractions are expanded (like 'it's' to 'it is').

### Preprocessing - Part 1
* ***Usermentions (at the end of the tweet):*** The usermentions at the end of the tweet (which are not part of the sentence) are generally not useful. So, it's better to remove these usermentions (which are at the end of the tweet and also not part of the sentence).
* ***Hashtags (at the end of the tweet):*** The hashtags at the end of the tweet is not necessary for further text processing as it's not a part of the tweet text (But these hashtags may be helpful in getting some info about the tweet incase we are unable to extract any useful entity from the tweet).
* >***Example tweet:*** "Grunge rock icon @chriscornell dies after #Soundgarden concert in #Detroit 🎵🎸 #ChrisCornell https://t.co/bAdYWi0IbL"
First, the usermention *@chriscornell* must be converted to its actual username "Chris cornell". Then, the url and the symbols must be removed. Then, the hashtag at the end of the sentence (#ChrisCornell) is removed. At the end of part-1 processing, the above tweet will become "Chris Cornell dies at #soundgarden concert in #Detroit". As it can be seen, the hashtags (in the sentence) have to be processed yet.

### Preprocessing - Part 2
* ***Usermentions (part of the sentence):***
* ***Hashtags (part of the sentence):*** The hashtags present as a part of the sentence must be converted into normal wordforms inorder to extract the tweet information later. As from the example above, the hashtags (part of the sentence) cannot be ignored since they make up an important part of the text. The following steps are followed to process these hashtags:
  *  First, the hash (`#`) is removed from the hashtag ("#soundgarden" becomes "soundgarden").
  * Then, an hashtag splitter module is used to split the hashtag keyword if possible ("soundgarden" becomes "sound<SPACE>garden"). The splitter module that was used can be found [here](https://github.com/jchook/wordseg). 
  * As a last step, the contractions in the text (if any) are expanded. For example, "it's" will become "it is" while Tonight's party will remain Tonight's party i.e. only verb-based contractions are expanded. The contractions module used can be found [here](https://github.com/kootenpv/contractions).
  * After processing a tweet using part-1 and part-2 phases, the example tweet above becomes ***"Chris Cornell dies at sound garden concert in detroit."***
  * As it can be seen, the text after processing can be used for further processing (cosine similarity can be found for a test tweet with other tweets to find similar tweets and recommending hashtags of the most similar tweet to the test tweet). This would have not been possible had the proprocessing part is not performed properly.

### Steps to run the codes

### Further info
* There is one other python module ```pycontractions``` which can be used for contractions expansions. It uses Google News pre-trained model. So, it is expected to perform better. But I am not sure about it's space and time complexity. The module can be found [here](https://github.com/ian-beaver/pycontractions).