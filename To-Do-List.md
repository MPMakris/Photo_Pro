### Project Overview
* Need to start a task manager. See any of the task manage websites that Ben mentioned in his Agile slideshow.
* Add documentation to all scripts/functions.


### New Scripting
* Implement a print_status class object - it will take parameters to guide the print status - model off the printing work happening in download_pics() in flicker_download.py

### Scripting Fixes
* ~~Fix the `save_data.py` script to correctly ensure that all json information is saved. Currently, only the names of the first object's information is saved. If the first first object does not contain a field, then none of the objects with that field will save their data. EX: all the .csv's are missing o_url because of this, perhaps others. --MIGHT BE FIXED~~
* ~~Tried to run download script. Every photo fails to download. Need to fix. --MIGHT BE FIXED~~
* Verify that the reason I'm only finding a few hundred pages for each search term is the license selection field.
* ~~Still need to save column names in feature data database. ALSO, bring in more features, AND attach the label data!!!~~
* ~~When saving image features, need to add columns for images name/id/owner to track which image it is.--DONE~~


### Models to Try to Implement
* Lasso
* Random Forest
* KNN Boosted

In addition to trying to predict num_views, create additional target columns like: (this data still needs to be joined to feature matrices)
* log(views)
* view_quartile_class (essentially becomes a classification problem by predicting which quartile the picture is in)
* view_decile_class (more precise, etc...)


### Things to Research
* colorthief - already downloaded python version
