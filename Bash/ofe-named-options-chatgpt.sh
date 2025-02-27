# sh function generated by ChatGPT

parse_params() {
    while [ $# -gt 0 ]; do
        if [[ $1 == --* ]]; then
            param="${1/--/}"
            param_name="${param%%=*}"
            param_value="${param#*=}"
            declare -g "$param_name"="$param_value"
        fi
        shift
    done
}

fit() {
    # Parse named parameters
    parse_params "$@"

    # Set default values if not provided
    logx="${logx:-no}"
    logy="${logy:-no}"
    autox="${autox:-no}"
    autoy="${autoy:-no}"

    # Ensure required parameters are set
    if [[ -z "$file" || -z "$function" ]]; then
        echo "Error: 'file' and 'function' parameters are required."
        return 1
    fi

    # Construct curl command
    curl_cmd=(
        curl -F "file=@$file"
        -F "function=$function"
        -F "logx=$logx"
        -F "logy=$logy"
        -F "autox=$autox"
        -F "autoy=$autoy"
    )

    # Include 'download' parameter if provided
    if [[ -n "$download" ]]; then
        curl_cmd+=(-F "download=$download")
    fi

    # Add the URL
    curl_cmd+=("http://192.92.147.107:8142/fit")

    # Execute the curl command
    "${curl_cmd[@]}"
}

