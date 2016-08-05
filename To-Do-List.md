### Project Overview
* Add documentation to all scripts/functions.


### TO DO LAST DAY:
* Turn back on pdg.set_trace() and see why graphs no longer working.
* Add an array of images in index page showing what software stack you used, get their icons online.
* Finish Model Page. Just hard code some numbers in and use some of the the .png's produced.
* Fix graphs on overview page - remember that the functions on the .js file should be corrected like how I did on the .js page for prevoius photos.
* Add an empty picture box on the submit photo page.
* Add a picture of me to the front index page.
* UPDATE the model that is used for prediction to the all-categories model, if possible.



### Scripting Fixes
* ~~Fix the `save_data.py` script to correctly ensure that all json information is saved. Currently, only the names of the first object's information is saved. If the first first object does not contain a field, then none of the objects with that field will save their data. EX: all the .csv's are missing o_url because of this, perhaps others. --MIGHT BE FIXED~~
* ~~Tried to run download script. Every photo fails to download. Need to fix. --MIGHT BE FIXED~~
* Verify that the reason I'm only finding a few hundred pages for each search term is the license selection field.
* ~~Still need to save column names in feature data database. ALSO, bring in more features, AND attach the label data!!!~~
* ~~When saving image features, need to add columns for images name/id/owner to track which image it is.--DONE~~


### Models to Try to Implement
* sklearn OneVersusRest

In addition to trying to predict num_views, create additional target columns like: (this data still needs to be joined to feature matrices)
* log(views)
* view_quartile_class (essentially becomes a classification problem by predicting which quartile the picture is in)
* view_decile_class (more precise, etc...)


### Features to Add
* ~~number of tags~~
* quality/length/sentiment of description written
* ~~content of pictures (NN)~~

### Notes on Bugs:
