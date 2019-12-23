# Photo Console Application

A python implementation of the Photo Console Application project.

## Introduction

The application is written in Python 3.  
It has a rich set of options for choosing one or more albums, row filtering and output formatting.

The code was rigoriously tested and analyzed.

* 100% test coverage.
* Mocking employed to ensure all code paths are tested.
* Lint is used to ensure best practices for structure and style.

## Getting Started

Install the following if you don't already have them.

* git from [git-scm.com]
* Python 3 if you don't already have it from [python.org/downloads].
* pipenv using pip ('pip install pipenv'), which now comes with Python.

## Prerequistes

* git
* Python 3
* pipenv

## Setup

* pip install pipenv
* pipenv --python 3.8.1

## Installation

1. git clone https://github.com/tedtheman/photo-console-app.git
2. cd photo-console-app
3. pipenv shell
4. pipenv install

## Running the tests

* pytest -v --cov --cov-report=html

## Running Lint

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
