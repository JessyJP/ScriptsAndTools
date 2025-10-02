#!/bin/bash

# Temporary files for curl output
curl_format_file=$(mktemp)
response_file=$(mktemp)
headers_file=$(mktemp)
status_file=$(mktemp)

# Cleanup function to remove temporary files
cleanup() {
    rm -f "$curl_format_file" "$response_file" "$headers_file" "$status_file"
}
trap cleanup EXIT

# Write curl format configuration to temporary file
cat <<EOF > "$curl_format_file"
time_namelookup:  %{time_namelookup}\n
time_connect:  %{time_connect}\n
time_appconnect:  %{time_appconnect}\n
time_pretransfer:  %{time_pretransfer}\n
time_redirect:  %{time_redirect}\n
time_starttransfer:  %{time_starttransfer}\n
time_total:  %{time_total}\n
EOF

# Function to convert seconds to milliseconds
convert_to_ms() {
    awk '{ printf "%.3f", $1 * 1000 }'
}

# Capture all arguments passed to the script
args=("$@")

# Extract the endpoint from arguments
endpoint="${args[-1]}"
unset 'args[${#args[@]}-1]'

# Ensure the endpoint has a protocol
if ! [[ "$endpoint" =~ ^https?:// ]]; then
    endpoint="http://$endpoint"
fi

# Perform the curl command and capture the output, response, and headers
output=$(curl "${args[@]}" -w "@$curl_format_file" -o "$response_file" -s -D "$headers_file" "$endpoint" 2> "$status_file")
response=$(cat "$response_file")
headers=$(cat "$headers_file")
status=$(cat "$status_file")

# Extract the HTTP status code from the headers
http_status=$(echo "$headers" | grep -oP '(?<=HTTP/1.1 )\d{3}')

# Check if the HTTP status code is empty and set a default value if necessary
if [ -z "$http_status" ]; then
    http_status="Unknown"
fi

# Allow for 200, 301, and other successful status codes
if [ "$http_status" != "Unknown" ] && [ "$http_status" -ge 400 ]; then
    echo "Error: HTTP status $http_status"
    exit 1
fi

# Extract values and convert to milliseconds
time_namelookup=$(echo "$output" | grep 'time_namelookup' | awk '{print $2}' | convert_to_ms)
time_connect=$(echo "$output" | grep 'time_connect' | awk '{print $2}' | convert_to_ms)
time_appconnect=$(echo "$output" | grep 'time_appconnect' | awk '{print $2}' | convert_to_ms)
time_pretransfer=$(echo "$output" | grep 'time_pretransfer' | awk '{print $2}' | convert_to_ms)
time_redirect=$(echo "$output" | grep 'time_redirect' | awk '{print $2}' | convert_to_ms)
time_starttransfer=$(echo "$output" | grep 'time_starttransfer' | awk '{print $2}' | convert_to_ms)
time_total=$(echo "$output" | grep 'time_total' | awk '{print $2}' | convert_to_ms)

# Print the results in milliseconds
echo "Endpoint: $endpoint"
echo "HTTP Status: $http_status"
echo "time_namelookup:  ${time_namelookup:-0} ms"
echo "time_connect:  ${time_connect:-0} ms"
echo "time_appconnect:  ${time_appconnect:-0} ms"
echo "time_pretransfer:  ${time_pretransfer:-0} ms"
echo "time_redirect:  ${time_redirect:-0} ms"
echo "time_starttransfer:  ${time_starttransfer:-0} ms"
echo "time_total:  ${time_total:-0} ms"

# Print the response and headers
echo -e "\nResponse:"
if [ -z "$response" ]; then
    echo "(empty response)"
else
    echo "$response"
fi

echo -e "\nHeaders:"
if [ -z "$headers" ]; then
    echo "(empty headers)"
else
    echo "$headers"
fi

# Print the curl status output for debugging
echo -e "\nCurl Status Output:"
if [ -z "$status" ]; then
    echo "(no status output)"
else
    echo "$status"
fi
