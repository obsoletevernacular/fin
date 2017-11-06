#!/bin/bash

# Generate goldenfiles for testing

pushd testfiles
tests="checking credit savings"
for t in ${tests}; do
  fin import "fin_import_${t}_oct.test" > "fin_import_${t}_oct.golden"
done
