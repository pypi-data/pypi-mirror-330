# IMG2GIF_package

## Table of Contents
- [IMG2GIF\_package](#img2gif_package)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Quick start](#quick-start)
  - [Features](#features)
  
## Installation

Download using pip via pypi.

```bash
$ pip install 'package' --upgrade
  or
$ pip install git+'repository'
```
(Mac/homebrew users may need to use ``pip3``)


## Quick start
```python
 >>> from IMG2GIF_package.converter import GifConverter
 >>> c = GifConverter("your original images path", 'your gif output path', (320,240))
 >>> c.convert_gif()
```

## Features
  * Python library to convert single oder multiple frame gif images
  * OpenCV does not support gif images.