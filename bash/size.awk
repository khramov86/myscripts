{
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
}
