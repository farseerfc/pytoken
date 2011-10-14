#!/bin/sh
ls -l $1 | awk  '{printf $5" " $9" "}'
(time cat $1 | python ../../st.py >/dev/zero) 2>&1 | head -n2 | tail -n1 | sed 's/^.*m//' | sed 's/s$//'
