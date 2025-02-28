#!/bin/bash

set -e


# Use environment variables passed from Python
PACKAGE_ROOT=${PACKAGE_ROOT:-$(pwd)}
BACKBONE_DIR=${BACKBONE_DIR:-"${PACKAGE_ROOT}/Package_Backbone"}
TESTING_SCRIPT=${TESTING_SCRIPT:-"${PACKAGE_ROOT}/scripts/testing.py"}

# Create required directories
mkdir -p "${BACKBONE_DIR}"


cd "${BACKBONE_DIR}"

FILES=(
    "modeling_auto.py"
    "processing_auto.py"
    "tokenization_auto.py"
    "image_processing_auto.py"
    "feature_extraction_auto.py"
)

all_exist=true
for file in "${FILES[@]}"; do
    if [ ! -f "${BACKBONE_DIR}/${file}" ]; then
        all_exist=false
        break
    fi
done

if [ "$all_exist" = true ]; then
    exit 0
fi
# Download HuggingFace files
echo "📥 Downloading required Hugging Face files..."

for file in "${FILES[@]}"; do
    if [ ! -f "$file" ]; then
        wget -q "https://raw.githubusercontent.com/huggingface/transformers/main/src/transformers/models/auto/${file}"
        echo "✅ Downloaded: ${file}"
    else
        echo "✅ File exists: ${file}"
    fi
done

# Run testing on downloaded files
echo "🛠 Running testing on downloaded files..."
for file in *.py; do
    echo "🔍 Testing: ${file}"
    python "${TESTING_SCRIPT}" "${file}"
done

echo "✅ All operations completed successfully!"