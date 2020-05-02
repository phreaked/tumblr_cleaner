## TumblrCleaner 1.0

- Keep original: keeps only the original posts
- Keep relevant: keeps original posts and any posts with your username in it
- Delete all: deletes all posts

## Requirements

console

```
pip3 install mechanize lxml
```

gui

```
pip3 install mechanize lxml pyqt5
```

## Pyinstaller

install

```
pip3 install pyinstaller
```

console


```
pyinstaller file_console.py --name=TumblrCleaner_Console --onefile --console
```

gui

```
pyinstaller file.py --name=TumblrCleaner --onefile --noconsole
