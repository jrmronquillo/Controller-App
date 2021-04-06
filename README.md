# Controller Web App

This is a user interface to a python script/API that will ultimately let the user remotely send IR commands to 1-16 devices simultaneously or individually. The concepts used to develop this app were primarily an application of skills learned Udacity's Full Stack Web Developer course.


## Development Environment Setup (Mac OS)
### Install Vagrant v2.2.14
https://www.vagrantup.com/downloads


### Install Virtualbox 6.1.18
https://www.virtualbox.org/wiki/Downloads

### Clone git repo
git clone https://github.com/jrmronquillo/controller-app.git

# Setup
  ```
  cd controller-app
  vagrant up
  vagrant ssh
  cd /vagrant/main/
  python3 main.py
```

### Check Front-end on browser from local machine

http://localhost:5000/


## Production Build Instructions
Coming soon.


## Resources
Udacity (https://www.udacity.com/)
No flask module error - https://stackoverflow.com/questions/31252791/flask-importerror-no-module-named-flask
https://stackoverflow.com/questions/52394543/e-unable-to-locate-package-python3-pip

## Troubleshooting
1. If the python API takes unreasonably long to respond, the web app will appear stuck and does not notify the user that there is an error case.
2.
```
Stderr: VBoxManage: error: The virtual machine '...' has terminated unexpectedly during startup with exit code 1 (0x1)
VBoxManage: error: Details: code NS_ERROR_FAILURE (0x80004005), component MachineWrap, interface IMachine
```
If you see the error above, try checking "Security & Privacy" for Mac settings to see if you need to allow Virtualbox permissions - happens on first install of Vagrant/Virtualbox

3.
```Traceback (most recent call last):
  File "/usr/local/bin/pip3", line 7, in <module>
    from pip._internal.cli.main import main
  File "/usr/local/lib/python3.5/dist-packages/pip/_internal/cli/main.py", line 60
    sys.stderr.write(f"ERROR: {exc}")
                                   ^
SyntaxError: invalid syntax
```
This issue appeared after python 2.7 was depecrated. Need to upgrade and use Python3 -
```
    python3 main.py
```


