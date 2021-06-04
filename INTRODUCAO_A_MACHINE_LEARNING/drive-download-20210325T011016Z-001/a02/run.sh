#!/bin/bash

filename=$1

pdflatex "$filename".tex
evince "$filename".pdf &
