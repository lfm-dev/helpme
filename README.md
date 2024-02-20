# helpme

Search through your How-to guides.

Have directories (and subdirectories) with all your how-to guides indexed and showed in rich table format.
You can search by name of directory or by the guide name.
Then, by selecting the ID shown in the table you can read the content of the guide with markdown formatting.

![screenshot-dev](./img/screenshot-dev.png)
![screenshot-example_guide](./img/screenshot-example_guide.png)

## Dependencies

- [rich](https://github.com/Textualize/rich)

## Installation

```bash
wget https://raw.githubusercontent.com/lfm-dev/helpme/main/install.sh && bash install.sh
```

## Usage

* All guides should be .md files.  

```bash
helpme query1 query2 ...
helpme all (shows all guides)
helpme -e query1 query2 ... [edit mode]
```
