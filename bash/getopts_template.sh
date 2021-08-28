#!/usr/bin/env bash

while getopts a:b:cd param;do
  case $param in
    a)  echo ""
        echo "parameter 'a' with argument: $OPTARG"
        ;;

    b)  echo ""
        echo "parameter 'b' with argument: $OPTARG"
        ;;

    c)  echo "parameter 'c' selected (no colon, no argument)"
        ;;
    d)  echo "parameter 'd' selected (no colon, no argument)"
        ;;
    esac
done
