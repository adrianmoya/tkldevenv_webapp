#!/bin/bash

wget -O /tmp/Django-1.2.3.tar.gz http://www.djangoproject.com/download/1.2.3/tarball/
tar xzvf /tmp/Django-1.2.3.tar.gz -C /tmp
cd /tmp/Django-1.2.3
python setup.py install
