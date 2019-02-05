# Stanford Core NLP for Entity Extraction
The methods that I use to recommend hashtags requires entities from the tweet. So, one of the modules which I used to extract entities was the Stanford CoreNLP. It is a popular module used worldwide by the NLP community.

### Issues with extracting entities from tweets
In general, the entity extraction modules take into account the CASE of the first letter of the words to determine whether it is an entity. For instance, the output of the example tweet used in the preprocessing documentation was "Chris Cornell dies at sound garden concert in detroit". If this is directly sent to an entity recognition module, it may not detect the entity "sound garden" and "detroit" which are in LOWERCASES. 
So, inorder to process these tweets, we have two options:
* Pass the tweet to a TrueCase annotator (which recognizes the “true” case of tokens) and then send that TrueCase annotated text to other entity recognition modules.
* Use Stanford Caseless models which can recognize the entities even when the text cases are ill-formed.
I am using the first method since once TrueCase annotated, I could obtain the entities using various modules and aggregate the results (instead of just using one module which may not work well in all cases).

### First method - TrueCase Annotator followed by Entity extraction
* The Stanford CoreNLP module has various annotators (like pos tagging, ner, truecase etc.). We can load all the required annotators as params while starting the program. 
* Also, while recognizing entities, the CoreNLP even has an annotator ***entitylink*** which links the recognized entities with their wikipedia pages.

##### Ways to extract entities from the CoreNLP module
The coreNLP module provides various options to get entities for a given text:
* ***command-line tool (using Java)*** - Loads all models and then sends the text given in the command-line and prints the output.
* ***libs (for Java programs) and modules (for Python programs)*** - Running the program loads all the models, runs the query on it and then outputs the results.
* ***server-client architecture*** - Starts a server with all the required models loaded and then answers queries of the client. This approach is efficient incase entities have to be extracted for many tweets (millions) since the server loads the models only once (which has high time and space complexity) and then can answer queries in parallel from the client. By default, the server creates 'n_cores' (number of cores on the machine) number of threads to process the incoming requests.

##### The code
* I have written the codes in Java and Python. But there is some difference in the codes of the two languages.
* ***Java code:*** 
  * The code follows the second method described above. It used the CoreNLP libs to load all the modules and runs the query on it. All the loaded models are vanished once the program finishes it's execution.
* ***Python code:*** 
  * The Python code uses server-client architecture. First the server is loaded using the command ```java```.
  * Once the server is running, the client program is started (using multi-threads) which then queries the server and returns the result. The server loads all the required models only when a query is made by the client for the first time. So, it might take time for the first query to return the results (depending on the models loaded). For further info about which models take time and memory, [click here](https://stanfordnlp.github.io/CoreNLP/memory-time.html#where-does-all-the-time-go).
### Second method - Using caseless models
* I have not used this method for my project. Further details about this approach can be found [here](https://stanfordnlp.github.io/CoreNLP/caseless.html).