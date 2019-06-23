#!/bin/bash
export FLASK_APP=kido:app
export FLASK_DEBUG=1
export PYTHONPATH='./':PYTHONPATH
flask run
