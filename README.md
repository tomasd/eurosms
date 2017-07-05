eurosms
=======

Python API for http://www.eurosms.sk/

Installation
============

```
    pip install git+https://github.com/tomasd/eurosms.git
```

Usage
=====

```python
    from eurosms import EuroSms

    api = EuroSms(id='1-TB672G', key='5^Af-8Ss')
    api.send('John_Smith', '+421948123456', 'My message')
```

License
=======

MIT License
