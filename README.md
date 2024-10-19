# info-viz-app-watcher
Simple Python script to watch a file for changes and notify a browser via websockets to reload the page. This is just to make some homework easier ;)

# How to use it
1. Install the only depedency of the script   
````
pip install websockets
````
2. Put watch.py into the directory where index.html and the file that needs to be watched are located   
    
3. Use this command to start the watcher
````
python watch.py {file that needs to be watched!}
````

# How it works
After starting up, watch.py will inject some javascript into index.html, which it expects to find in the same directory. Before closing watch.py should remove the javascript by itself.   
While running watch.py will listen for a websocket connection on port 8756, once a browser connects it will watch the file for some changes using the last modified timestamp. After some changes have been detected, watch.py will notify the browser which will reload the page.




The intended use is to edit some javascript and then see the changes directly in the browser after saving the file.
Made for some homework at the Universität Stuttgart ;)   
