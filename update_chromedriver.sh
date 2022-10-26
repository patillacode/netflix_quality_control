#!/bin/bash

VERSION_URL="https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
VERSION=$(curl -f --silent $VERSION_URL)
if [ -z "$VERSION" ]; then
  echo "Failed to read current version from $VERSION_URL. Aborting."
  exit 1
else
  echo "Current version is $VERSION"
fi

# Abort script if any of the next commands fails.
set -e
set -o pipefail

ZIPFILEPATH="/tmp/chromedriver-$VERSION.zip"
echo "Downloading to $ZIPFILEPATH"
curl -f --silent "https://chromedriver.storage.googleapis.com/$VERSION/chromedriver_mac_arm64.zip" > "$ZIPFILEPATH"

BINFILEPATH="/usr/local/bin/chromedriver-$VERSION"
echo "Extracting to $BINFILEPATH"
unzip -p "$ZIPFILEPATH" chromedriver > "$BINFILEPATH"

echo Setting execute flag
chmod +x "$BINFILEPATH"

echo Updating symlink
ln -nfs "$BINFILEPATH" /usr/local/bin/chromedriver

echo Removing ZIP file
rm "$ZIPFILEPATH"

echo "Done"
chromedriver -v
