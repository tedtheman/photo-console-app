# Photo Console Application

A python implementation of the Photo Console Application project.

## Overview

The application is written in Python version 3 and is deployed with pipenv, which combines package management and virtual environments.  It has a rich set of options for choosing one or more albums, interative mode, row filtering and output formatting.  

The code was rigoriously analyzed and tested using pylint and pytest, respectively.

* 100% test coverage.
* Mocking is utilized to cover all code paths.
* Lint is used to ensure best PEP8 practices for code complexity, structure and style.
* By using the suggested pytest options, a nicely formatted HTML report is created.  See htmlcov/index.html.  The starting page contains a summary with file links for drilling down.

## Getting Started

Install the following if not already:

* git from [git-scm.com]
* Python 3 if you don't already have it from [python.org/downloads].
* pipenv using pip, which comes with Python.

## Prerequistes

* git
* Python 3
* pipenv

## Dependencies - handled automatically by pipenv

* requests     # for accessing json photo album online
* prettytable  # for making tablular formatted console output
* pytest       # for unit and functional automated tests
* pytest-cov   # for test coverage data collection and reporting
* pylint       # for code complexity, structure and style analysis 

## Setup

* pip install pipenv
* pipenv --python 3.8  # this creates a virtual python 3.8 environment

## Installation

1. git clone https://github.com/tedtheman/photo-console-app.git
2. cd photo-console-app
3. pipenv shell    # this activates the virtual environment
4. pipenv install  # this installs the dependencies

## Running the tests - with coverage collection and reporting

* pytest -v --cov --cov-report=html

## Running lint - on both application and test code

* python -m pylint photos.py
* python -m pylint test_photos.py

## Usage - use -h/--help

* python photos.py -h
* python photos.py --help

## Running the application - examples

* python photos.py 1
* python photos.py 2 -n 10
* python photos.py 3 -n 10 --pretty
* python photos.py 4 5 6 --pretty --rows --grep qui
* python photos.py 7 -i
