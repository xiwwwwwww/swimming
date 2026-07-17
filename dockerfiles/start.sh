#!/bin/bash
set -e

if [[ $@ ]]; then
    eval $@
else
    /bin/bash
fi