#!/usr/bin/env bash
cd layer
zip -r9 ../layer.zip .
cd ..
zip -g function.zip -r app