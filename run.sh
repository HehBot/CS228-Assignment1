#!/usr/bin/bash

if [[ "$1" = "-h" ||  ! ( $# -eq 0 || $# -eq 1 || $# -eq 3 ) ]]; then
    Z="test/input.txt test/specimen.txt"
    echo "Usage 1: $0"
    echo "    Uses existing testcase in $Z"
    echo
    echo "Usage 2: $0 <dir>"
    echo "    Uses existing testcase in <dir>/input.txt <dir>/specimen.txt"
    echo
    echo "Usage 3: $0 <N> <T> <sat|unsat>"
    echo "    Generates and uses new testcase in $Z"
    exit
fi

PY=python3

TEST=test
if [ $# -eq 1 ]; then
    if [ -e $1/input.txt ]; then
        TEST=$1
    else
        echo "Invalid test files in dir \"$1\""
        exit
    fi
fi

INPUT=$TEST/input.txt
OUTPUT=$TEST/output.txt
SPECIMEN=$TEST/specimen.txt

mkdir -p $TEST

CODE=210050018_210050038_210050085_tile_loop.py

if [ $# -eq 3 ]; then
    $PY generator.py $1 $2 $3 $INPUT | tail -n +3 > $SPECIMEN
fi

time $PY $CODE $INPUT > $OUTPUT

X=$(head -1 $OUTPUT)
Y=$(cat $SPECIMEN)
if [ "$Y" = "" ]; then
    Y="unsat"
else
    Y="sat"
fi
if ! [ "$X" = "$Y" ]; then
    echo "Output is $X whereas board is $Y"
fi
if [ "$Y" = "sat" ]; then
    $PY verifier.py $INPUT $OUTPUT
else
    echo "Given solution is CORRECT"
fi
