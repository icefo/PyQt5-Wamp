# PyQt5-Wamp

Here is a example PyQt5 app that
* can use wamp's RPC to add two numbers
* can subscribe to a wamp topic that publish the time every 2 seconds

![capture-pyqt5-wamp](https://cloud.githubusercontent.com/assets/7746352/12374901/ea684d9c-bcab-11e5-87fd-9f2a5d5ce7f2.png)

## Requirements:
* Python >= 3.4
* PyQt5 (use your package manager to install this lib)
* [Quamash](https://github.com/harvimt/quamash) (asyncio event loop for pyqt)
* [autobahn|python](http://autobahn.ws/python/) (the wamp client)
* [the crossbar wamp router](http://crossbar.io/)

## Usage
1. Run the ```launch_crossbar.sh``` script.
2. Launch the ```Wamp_Backend.py``` file.
3. Launch the ```PyQt5_GUI.py````file.

## Note
I tried to keep it simple but non-trivial so you can build something out of this, if something is not clear just open an issue.
