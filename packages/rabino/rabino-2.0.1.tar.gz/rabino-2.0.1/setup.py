import os
import re
from setuptools import setup,find_packages

requires = ["aiohttp","aiofiles","asyncio","tqdm","pathlib","rubiran"]
_long_description = """


### How to import the rubino library

``` bash
from rabino import rubino
```

## An example:
```python
from rabino import rubino
import asyncio
async def main():
    async with rubino("auth") as bot:
        
        data = await bot.search_username("@super_god1")
        print(data)
asyncio.run(main())
```


### How to install the library

``` bash
pip install rabino==2.0.1 aiofiles aiohttp asyncio tqdm pathlib
```

### My ID in Telegram

``` bash
https://t.me/RMSource
```
## And My ID Channel in Telegram

``` bash
https://t.me/RMSource
```
### My site
<a href="https://anime.api-vison.workers.dev" style="text-decoration : none;">سایت ما</a>
"""

setup(
    name = "rabino",
    version = "2.0.1",
    author = "mamadcoder",
    author_email = "x.coder.2721@gmail.com",
    description = ("rubino Library Bot"),
    license = "MIT",
    keywords = ["rubika","bot","rubino","robot","library","rubikalib","rubikalib.ml","rubikalib.ir","rabino","Rabino","libraryrobiran","Rubika","Python","rubiran","pyrubi","telebot"],
    url = "https://github.com/vs-mamad/rabino/",
    packages=find_packages(),
    install_requires = requires,
    long_description=_long_description,
    long_description_content_type="text/markdown",
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    "Programming Language :: Python :: Implementation :: PyPy",
    'Programming Language :: Python :: 3',   
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
	'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
    'Programming Language :: Python :: 3.13',
    ],
)