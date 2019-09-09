# Controller Web App
=====
Test
Introduction
-----
Rhis is a user interface to a python script/API that will ultimately let the user remotely send IR commands to 1-16 devices simultaneously or individually. The concepts used to develop this app were primarily an application of skills learned Udacity's Full Stack Web Developer course. 


Setup
-----
1. vagrant
  ```
  cd controller-app
  vagrant up
  vagrant ssh
  cd ..
  cd ..
  cd vagrant
  ```
2. python
```
python main.py
```

3. Front-end on local machine

http://localhost:5000/





Resources
-----
Udacity (https://www.udacity.com/)


Limitations
----
1. If the python API takes unreasonably long to respond, the web app will appear stuck and does not notify the user that there is an error case.

