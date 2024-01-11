#!/bin/bash

if [ -L "/usr/local/bin/helpme" ]; then
    sudo rm "/usr/local/bin/helpme"
fi

if [ -d "/usr/local/bin/helpme_files" ]; then
    sudo rm -r "/usr/local/bin/helpme_files"
fi

while : ; do
    echo -n "path to your guides: "
    read pathToGuides
    if [ -d "$pathToGuides" ]; then
        break
    else
        echo "$pathToGuides doesnt exists, try again."
    fi
done

wget http://github.com/lfm-dev/helpme/archive/master.zip -O helpme.zip
unzip helpme.zip
sed -i -e "s#GUIDES_PATH = '/path/to/your/guides/folder'#GUIDES_PATH = '$pathToGuides'#" helpme-main/src/helpme.py # add path to script
sudo cp -r helpme-main/src /usr/local/bin/helpme_files
rm -r helpme-main helpme.zip
cd /usr/local/bin
sudo ln -s /usr/local/bin/helpme_files/helpme.py helpme
sudo chmod a+rx helpme