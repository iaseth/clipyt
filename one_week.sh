START=$(date -d "7 days ago" +%s)
END=$(date +%s)

curl -X GET "http://localhost:5000/entries?start=$START&end=$END"
