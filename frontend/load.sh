#!/bin/bash

# Define the source and destination paths
src_file="./call_loader.js"
dest_dir="$HOME/frappe-bench/apps/vulero_dialer/vulero_dialer/public/frontend"
assets_dir="${dest_dir}/assets"

# Copy the call_loader.js to the destination directory
cp "$src_file" "$dest_dir/call_loader.js"

# Find the latest .js and .css files in the assets directory
latest_js=$(ls -Art ${assets_dir}/*.js | tail -n 1)
latest_css=$(ls -Art ${assets_dir}/*.css | tail -n 1)

# Extract the base names
latest_js_file=$(basename $latest_js)
latest_css_file=$(basename $latest_css)

# Use sed to replace the script src and link href in the copied call_loader.js
sed -i "s|index-29895d2c.js|$latest_js_file|" "$dest_dir/call_loader.js"
sed -i "s|index-0ac285a5.css|$latest_css_file|" "$dest_dir/call_loader.js"

