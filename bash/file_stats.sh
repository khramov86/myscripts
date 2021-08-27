#!/usr/bin/env bash

# ./file_stats.sh [-l location|--location location] [-e extension|--extension extension] [-h|--help] [-s|--stats]

function usage() {
  echo "USAGE: $0 [-l location|--location location] [-e extension|--extension extension] [-h|--help] [-s|--stats]"
  echo "Examples:"
  echo "$0 -l /mypath -e txt -s"
  echo "$0 -e img --stats"
}

LOC_SET=0   #0-location not set, use current location 1-location set
STATS=0     #0-do not display statistics, 1-display statistics
while [ $# -gt 0 ]
  do
    case $1 in
      -l|--location )
        LOCATION="$2"
        if ! [ -d "$LOCATION" ]; then
          echo "It's not directory"
          usage
        fi
        LOC_SET=1
        shift
        shift
        ;;
      -e|--extension )
        EXT="$2"
        shift
        shift
        ;;
      -s|--stats )
        STATS=1
  if ($5 > max){
    max=$5
    max_name=$NF
  }
  if ($5 < min){
  min=$5
  min_name=$NF
  }
  }
  END{
    print "SUM:", sum/1024/1024, " MB"
    print "Files: ", NR
    if (stats==1) {
    print "Min file is:", min_name, ",size is:", min/1024, "KB"
    print "Max file is:", max_name, ",size is:", max/1024, "KB"
    }
  }
  '
else
  ls -l $LOCATION | awk '/^-/' | awk -v stats=$STATS '{
  sum+=$5
  if (NR==1) {
    min=$5
    max=$5
    min_name=$NF
    max_name=$NF
    }
  if ($5 > max){
    max=$5
    max_name=$NF
  }
  if ($5 < min){
  min=$5
  min_name=$NF
  }
  }
  END{
    print "SUM:", sum/1024/1024, " MB"
    print "Files: ", NR
    if (stats==1) {
    print "Min file is:", min_name, ",size is:", min/1024, "KB"
    print "Max file is:", max_name, ",size is:", max/1024, "KB"
    }
  }'
fi
