#!/usr/bin/bash

if [[ "$1" = "-h" || ! ( $# -eq 1 || $# -eq 4 ) ]]; then
    Z="<dir>/input.txt <dir>/specimen.txt"
    echo "USAGE:"
    echo
    echo "    $0 <dir>"
    echo "        Uses existing testcase in $Z"
    echo
    echo "    $0 <dir> <N> <T> <sat|unsat>"
    echo "        Generates and uses new testcase in $Z"
    echo
    exit
fi

PY=python3

TEST=$1
if [ $# -eq 1 ]; then
    if ! [ -e $1/input.txt ]; then
        echo "Invalid test files in dir \"$1\""
        exit
    fi
else
    rm -rf $TEST
    mkdir -p $TEST
fi

INPUT=$TEST/input.txt
OUTPUT=$TEST/output.txt
SPECIMEN=$TEST/specimen.txt

CODE=210050018_210050038_210050085_tile_loop.py

if [ $# -eq 4 ]; then
    $PY generator.py $2 $3 $4 $INPUT | tail -n +3 > $SPECIMEN
fi

time $PY $CODE $INPUT > $OUTPUT

X=$(head -1 $OUTPUT)
Y="no_specimen"
if [ -e $SPECIMEN ]; then
    if [ "$(cat $SPECIMEN)" = "" ]; then
        Y="unsat"
    else
        Y="sat"
    fi
fi

if ! [ "$X" = "$Y" ] && ! [ "$Y" = "no_specimen" ]; then
    echo "Output is $X whereas board is $Y"
    exit
fi
if [ "$Y" = "sat" ]; then
    $PY verifier.py $INPUT $OUTPUT
elif [ "$Y" = "unsat" ]; then
    echo "Given solution is CORRECT"
else
    echo "Output is $X"
fi
