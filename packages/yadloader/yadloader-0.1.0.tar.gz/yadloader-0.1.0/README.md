## Description

![PyPI - Version](https://img.shields.io/pypi/v/yadloader?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/yadloader?style=flat-square)
![PyPI - Status](https://img.shields.io/pypi/status/yadloader?style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/yadloader?style=flat-square)
![PyPI - License](https://img.shields.io/pypi/l/yadloader?style=flat-square)
![Gitea Issues](https://img.shields.io/gitea/issues/open/screwery/yadloader?gitea_url=https%3A%2F%2Fcodeberg.org&style=flat-square)
![Gitea Last Commit](https://img.shields.io/gitea/last-commit/screwery/yadloader?gitea_url=https%3A%2F%2Fcodeberg.org&style=flat-square)

**yadloader** is yet another downloader for those poor souls who have to use Yandex.Disk shared folders to receive big data. With the tool, huge files require much less micromanagement than they do with standard Yandex download system.

## Usage

Get metadata for the whole shared folder:

```bash
yadloader metadata -o metadata.json -l https://disk.yandex.ru/d/XXXXXXXXXXXXXX
```

Or for a subfolder:

```bash
yadloader metadata -o metadata.json -l https://disk.yandex.ru/d/XXXXXXXXXXXXXX -s /Shared/Subfolder
```

Then download:

```bash
yadloader download -m metadata.json -d /local/root/directory
```

## Bugs

Feel free to report bugs and request features [here](https://codeberg.org/screwery/yadloader/issues).
