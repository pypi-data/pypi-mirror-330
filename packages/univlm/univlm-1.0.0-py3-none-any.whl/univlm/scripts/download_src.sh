#!/bin/bash

# Determine the root of the univlm package (assuming script is in univlm/scripts/)
PACKAGE_ROOT="$(dirname "$(dirname "$(realpath "$0")")")"
TARGET_DIR="$PACKAGE_ROOT/src"  # Target directory is univlm/src

# Check if the target directory (src) already exists
if [ -d "$TARGET_DIR" ]; then
  echo "Target directory '$TARGET_DIR' already exists. Please remove it or choose a different name."
  exit 1
fi

# Remove any existing depthProSrc directory to avoid confusion
if [ -d "$PACKAGE_ROOT/depthProSrc" ]; then
  rm -rf "$PACKAGE_ROOT/depthProSrc"
  echo "Removed existing 'depthProSrc' directory."
fi

# Define the repository URL
REPO_URL="https://github.com/apple/ml-depth-pro.git"

# Navigate to the package root and create a temporary directory for cloning
TEMP_DIR="$PACKAGE_ROOT/temp_clone"
mkdir -p "$TEMP_DIR"

# Clone the repository into the temporary directory with sparse checkout
cd "$TEMP_DIR" || exit 1
git clone "$REPO_URL" .
git config core.sparsecheckout true
echo "src/*" >> .git/info/sparse-checkout
git checkout main  # Use 'main' or replace with the desired branch if needed

# Move the contents of src directly to univlm/src, then clean up
mv "src/"* "$TARGET_DIR/"
rm -rf "$TEMP_DIR"

echo "Successfully downloaded the contents of 'src' to '$TARGET_DIR'."

exit 0  # Successful completion