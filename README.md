# Price-Predicition-Tensorflow deployment manual Mac OS
1.  Download project files and store on your desktop.
2.  Download Python 3.6.x e.g. Python 3.6.8. Use this link and click on ‘macOS 64-bit installer’. https://www.python.org/downloads/release/python-368/
3.  Check that you have the correct version of Python installed. Open terminal and type: `python3`, check that it says Python 3.6.8.
4.  Open terminal and move into your desktop. Usually something like: `cd Desktop`
5.  Unzip the downloaded project files from step one from terminal: `unzip Price_Prediction_Tensorflow.zip`
6.  Move into your new unzipped code_29 directory:  `cd Price_Prediction_Tensorflow`
7.  Install pip3. This is used to install the project dependencies: `curl https:// bootstrap.pypa.io/get-pip.py -o get-pip.py` then type `python3 get-pip.py`
8.  Set up your virtual environment:  `pip3 install virtualenv` followed by `virtualenv -p python3 env`. This last command creates a virtual environment called 'env'.
9.  Now, let's activate our virtual environment:  `source env/bin/activate`
10. Install the project dependencies. This may take several minutes, do not interrupt this process: `pip3 install -r requirements.txt`
11. Replace the following files inside your virtual environment ('env' directory) with the ones that are
present in the Price_Prediction_Tensorflow folder. The following locations are from within the Price_Prediction_Tensorflow directory.
Replace these files:
env/lib/python3.6/site-packages/tensorflow/python/util/deprecation.py
env/lib/python3.6/site-packages/tensorflow/contrib/learn/python/learn/datasets/mnist.py
env/lib/python3.6/site-packages/tensorflow/python/client/session.py
... With these files, respectively:
env-changes/deprecation.py
env-changes/mnist.py
env-changes/session.py
12. Finally, we are now ready to run the server. From within the Price_Prediction_Tensorflow directory: `python3 manage.py runserver`
13. Once finished, deactivate your virtual environment: `deactivate`
