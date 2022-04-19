# SOFT7003 - Sphera

> Jorge El Busto
> 

> Josh Woodward
> 

> Ben Lapidge
> 

> Alex McDonough
> 

> Rohit Rathod
> 

> Adebayo Aromolaran
> 


# Software and tools used for this project

- Python
- Flask
  - Flask-Login
  - WTForms
  - Werkzeug 
- SQLAlchemy
- jQuery
- Bootstrap
- Gunicorn
  - Service worker
  - Manifest.json  

# Pre-requirements

- Python needs to be installed in order to run the software.

[Welcome to Python.org](https://www.python.org/)

# Creating tables

- Note that this part can be skipped if the tables have already been created. This part will be used just in case the indexes of a table get updated.
- Open the Python IDLE from the project folder and run the following code.

```python
>> import wsgi
>> wsgi.create_tables()
```

# Instructions

<aside>
⚠️ Make sure that the command line is running from the project folder.

</aside>

- Install the required libraries for Python. This can be done by copying and pasting the following code in the command line.

```jsx
python -m pip install -r requirements.txt
```

- In order to run the program, once the required libraries have been installed, the following code needs to be run from the command line.

```jsx
python -m flask run

```
-for macOS
```jsx
python3 -m flask run

```

- Once the program is running, open your browser and go to [https://127.0.0.1:5000](https://127.0.0.1:5000).
