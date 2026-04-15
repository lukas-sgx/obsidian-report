mapfile -t report_array < Data/status_report.txt

for report in "${report_array[@]}"; do
    if [ "$report" != "Encoded Status Report:" ]; then
        echo "$report" | base64 -d
    fi
done