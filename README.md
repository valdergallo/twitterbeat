Django Twitter Beat
====================

Twitter Beat subprocess to follow Twitters from one username


TO INSTALL
----------

	pip install twitterbeat
	
	or
	
	1. Download zip file 
	2. Extract it
	3. Execute in the extracted directory: python setup.py install

	Add on project settings 
	
	INSTALLED_APPS = (
	    ...
	    'twitterbeat'
	)
	
	
USAGE
-----

- Starting subprocess to get Twitters


```python
python manage.py twitter_beat --start	
```

- Restart subprocess

```python
python manage.py twitter_beat --restart	
```

- Stop subprocess

```python
python manage.py twitter_beat --stop	
```

Requirements
------------
- django 1.2.x or higher
- python-twitter==0.8.2
- feedparser==5.1.2

