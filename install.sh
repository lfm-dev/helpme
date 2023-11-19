#!/bin/bash

while : ; do
    echo -n "path to your guides: "
    read pathToGuides
    if [ -d "$pathToGuides" ]; then
        break
    else
        echo "$pathToGuides doesnt exists, try again."
    fi
done

wget https://raw.githubusercontent.com/lfm-dev/helpme/main/helpme.py
sed -i -e "s#    guides_path = '/path/to/your/guides/folder'#    guides_path = '$pathToGuides'#" helpme.py # add path to script

sudo mv helpme.py /usr/local/bin/helpme
sudo chmod a+rx /usr/local/bin/helpme
rm install.sh