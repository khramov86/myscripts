#!/usr/bin/env bash

# ./files.sh [-l location|--location location] [-e extension|--extension extension] [-h|--help] [-s|--stats]

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
  esac
done

if [ $FIX -eq 1 ] && [ -f "$FILE" ]; then
  echo "Fixing spaces"
  sed -i 's/[[:blank:]]\+$//' "$FILE"
  sed -i 's/^[[:blank:]]\+//' "$FILE"
  echo "DONE"
fi

if [ -f "$FILE" ]; then
  LINES=0
  REGEX_START="^[[:blank:]]+"
  REGEX_END="[[:blank:]]+$"
  while IFS= read -r line
  do
    let LINES++
    #if there is no space issue on a line, just print the line
    echo "$line" | sed -e '/[[:blank:]]\+$/q9' -e '/^[[:blank:]]\+/q7' >/dev/null
    if [ $? -eq 0 ]; then
      printf %4s "$LINES:" >> temp.txt
      echo "$line" >> temp.txt
      continue
    fi
    printf %4s "$LINES:" >> temp.txt
    if [[ "$line" =~ $REGEX_START ]]; then
      MATCH=`echo "$BASH_REMATCH" | sed 's/\t/|__TAB__|/g'`
      echo -e -n "\e[41m$MATCH\e[49m" >> temp.txt
    fi
    echo -e -n "$line" | sed -e 's/^[[:blank:]]\+//' -e 's/[[:blank:]]\+$//' >> temp.txt
    if [[ "$line" =~ $REGEX_END ]]; then
      MATCH=`echo "$BASH_REMATCH" | sed 's/\t/|__TAB__|/g'`
      echo -e "\e[41m$MATCH\e[49m" >> temp.txt
    else
      echo "" >> temp.txt
    fi
  done < "$FILE"
  cat temp.txt
  rm temp.txt
fi

if [ $FIX -eq 1 ]; then
  echo
  echo -e "\e[42mDONE\e[49m"
fi
