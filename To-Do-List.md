### New Scripting
* Start the script to take the meta-data and download raw photos.

### Scripting Fixes
* Fix the `save_data.py` script to correctly ensure that all json information is saved. Currently, only the names of the first object's information is saved. If the first first object does not contain a field, then none of the objects with that field will save their data. EX: all the .csv's are missing o_url because of this, perhaps others. --MIGHT BE FIXED
* Eliminate duplicates from the json requets. Flickr will only give 4000 unique results per request. To get around this, add data fields to the request. See [this](<http://stackoverflow.com/questions/1994037/flickr-api-returning-duplicate-photos>) page for instructions, see last post.