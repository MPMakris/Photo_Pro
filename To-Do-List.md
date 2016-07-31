### Project Overview
* Need to start a task manager. See any of the task manage websites that Ben mentioned in his Agile slideshow.
* Add documentation to all scripts/functions.

### Current EC2 Processes
* all 500-image feature sets DONE
* 5000-image feature sets done for landscape, portrait, and sports
* all-image feature sets done for building, sports, portrait, animals
* all-image feature sets **in-progress** for landscape
* target-data complete for: all 500-image feature sets except portrait, 5000-image set of sports and landscape
* See error notes below for target error problems in the portrait feature files


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

### Features to Add
* number of tags
* quality/length/sentiment of description written
* content of pictures (NN)

### Notes on Bugs:
* When running target script on the EC2, working on the feature data data/modeling/PORTRAIT/feature_data_PORTRAIT_469.csv, I keep getting the following error:
```
Begining Image Target Download:
Downloading Target Info for 469 Images...

User Target Info Download COMPLETE
Run: 212 for Image: 6865204379Traceback (most recent call last):
  File "src/target/run_get_image_targets.py", line 57, in <module>
    main(feature_info_file_path)
  File "src/target/run_get_image_targets.py", line 35, in main
    image_info = df_target['id'].reset_index().apply(get_image_data, axis=1)
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/pandas/core/frame.py", line 4061, in apply
    return self._apply_standard(f, axis, reduce=reduce)
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/pandas/core/frame.py", line 4157, in _apply_standard
    results[i] = func(v)
  File "/home/ubuntu/efs/GIT/Photo_Pro/common/flickr_api_functions.py", line 87, in get_image_data
    image_nfavs = soup.photo.get('total')
AttributeError: ("'NoneType' object has no attribute 'get'", u'occurred at index 212')
```
* Need to see what's happening with image `6865204379`, and why it involves an object of `NoneType.` Open csv in padas in .ipynb and see what the owner and id columns are, and why the API is having issues with it. Or see what fails in my script.
* Recieve a similar error at:
```
Run: 270 for User: 15426517@N07Traceback (most recent call last):
  File "src/target/run_get_image_targets.py", line 57, in <module>
    main(feature_info_file_path)
  File "src/target/run_get_image_targets.py", line 29, in main
    user_info = df_target['owner'].reset_index().apply(get_user_data, axis=1)
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/pandas/core/frame.py", line 4061, in apply
    return self._apply_standard(f, axis, reduce=reduce)
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/pandas/core/frame.py", line 4157, in _apply_standard
    results[i] = func(v)
  File "/home/ubuntu/efs/GIT/Photo_Pro/common/flickr_api_functions.py", line 49, in get_user_data
    is_pro = int(soup.person.get('ispro'))
AttributeError: ("'NoneType' object has no attribute 'get'", u'occurred at index 270')
```
* Recieved a similar error at when running BUILDING:
```User Target Info Download COMPLETE
Run: 9017 for Image: 22888815373Traceback (most recent call last):
  File "src/target/run_get_image_targets.py", line 57, in <module>
    main(feature_info_file_path)
  File "src/target/run_get_image_targets.py", line 35, in main
    image_info = df_target['id'].reset_index().apply(get_image_data, axis=1)
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/pandas/core/frame.py", line 40
61, in apply
    return self._apply_standard(f, axis, reduce=reduce)
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/pandas/core/frame.py", line 41
57, in _apply_standard
    results[i] = func(v)
  File "/home/ubuntu/efs/GIT/Photo_Pro/common/flickr_api_functions.py", line 82, in get_i
mage_data
    soup = BeautifulSoup(requests.get(url, params=params).content, 'lxml')
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/requests/api.py", line 71, in
get
    return request('get', url, params=params, **kwargs)
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/requests/api.py", line 57, in
request
    return session.request(method=method, url=url, **kwargs)
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/requests/sessions.py", line 47
5, in request
    resp = self.send(prep, **send_kwargs)
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/requests/sessions.py", line 58
5, in send
    r = adapter.send(request, **kwargs)
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/requests/adapters.py", line 47
7, in send
    raise SSLError(e, request=request)
requests.exceptions.SSLError: (SSLError(SSLEOFError(8, u'EOF occurred in violation of pro
tocol (_ssl.c:590)'),), u'occurred at index 9017')
```
* Same for Landscape:
```
Begining Image Target Download:
Downloading Target Info for 44173 Images...

User Target Info Download COMPLETE
Run: 21481 for Image: 7434718266Traceback (most recent call last):
  File "src/target/run_get_image_targets.py", line 57, in <module>
    main(feature_info_file_path)
  File "src/target/run_get_image_targets.py", line 35, in main
    image_info = df_target['id'].reset_index().apply(get_image_data, axis=1)
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/pandas/core/frame.py", line 4061, in apply
    return self._apply_standard(f, axis, reduce=reduce)
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/pandas/core/frame.py", line 4157, in _apply_standard
    results[i] = func(v)
  File "/home/ubuntu/efs/GIT/Photo_Pro/src/target/common/flickr_api_functions.py", line 87, in get_image_data
    image_nfavs = soup.photo.get('total')
AttributeError: ("'NoneType' object has no attribute 'get'", u'occurred at index 21481')
```
