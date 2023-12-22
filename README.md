# Installation
Note: This installation is for beginners who do not have programming experience and no intent to modify this software. Consequently, this installation does not use a virtual environment but instead installs programs system-wide.
## 1. Installation of prerequisites
### 1.1 Install Git
Open a terminal window and enter the following command to check if you have Git installed on your system:
```
git --version
```
If Git is installed, this command will display the installed version of Git. Otherwise, go to https://git-scm.com/downloads and download the Git version for your operating system.
### 1.2 Install Python
Now, perform the same for Python. In a terminal window, enter the following command to check if you have Python installed on your system:
```
python --version
```
If Python is installed, this command will display the installed version. Otherwise, go to https://www.python.org/downloads/ and download Python for your operating system.
### 1.3 Install Flask
Flask is the web framework that this software is based on. To install it, enter the following command:
```
pip install flask
```
## 2. Installation of this software
To install this software, you have to clone this repository to your system. First, open a terminal window and go to the folder where you want it installed:
```
cd path\to\folder
```
Replace 'path\to\folder' with the respective path to the desired folder.
Then, clone this repository to your system with the following command in the same terminal window:
```
git clone https://github.com/nicklas-rn/liquid-handler
```
Now, when you go to the previously specified path in your explorer/finder, you should find a folder with the name liquid-handler. The installation was successful!

# Running the software
First, go to the folder 'liquid-handler' in a terminal window. To achieve that, open a terminal window and enter the following command:
```
cd path\to\folder\liquid-handler
```
To run the software, enter:
```
flask run
```
Then, open your browser and open the following domain: http://127.0.0.1:5000
You're good to go!
