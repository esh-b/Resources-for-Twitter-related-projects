# Entity Extraction using the Tagme module
Tagme is yet another entity extraction module which recognizes entities from text and also links those entities with the wikipedia pages. For example, if the tweet talks about the Indian Parliament but just contains the word 'Parliament' in it's text, the module correctly links that parliament entity with the Indian Parliament wikipage.
Along with Stanford CoreNLP module, I am using Tagme and TwitterNLP modules to extract entities which are then aggregated.

### Using the module
* Tagme provides an API service to query and get the entities (along with their wikipages). So, you will have to signup, get the token and use it to query the service. You will get two types of tokens: personal token and qualified token. You can use both for querying (which could speedup the querying process for large datasets) but be sure about which token to use in what context.
* ***Note:*** Sometimes Tagme gives the error "MAX LIMIT EXCEEDED" when there are many parallel client threads (using the same token). So, it would be better not to use more than 10 threads (in my opinion) while querying. The Tagme documentation does not talk about the API limits though.