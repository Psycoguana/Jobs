# Jinja2 to Django Converter
This script will search the entirety of a file and change it's jinja2 format to django. So this:


```
<script src="{{ url_for('static', filename='dist/file.js') }}"></script>

<link href="{{ url_for('static', filename='dist/file.css') }}" rel="stylesheet">

href="{{url_for('something.comics')}}"

{{ some_variable_name }}

```

will be converted to:

```
<script src="{% static 'dist/file.js' %}"></script>

<link href="/static/dist/file.css" rel="stylesheet">

href="/something/comics"

{% page_attribute "some_variable_name" %}
```




## 📦 Requirements
```
- Python 3
```

## 🔧 Installation

You just need to install Python! 😊

## 🖥️ Usage

You need to run `python3 main.py input_file.html` and the script will return a file in the same directory called `djangoinput_file.html`.

You can also input a folder name, and a folder called `foldername_django` will be created, which will contain the files with the same name, but the formatting changed.


## 📚 Dependencies

* No dependecies are needed. Just pure Python! 🐍