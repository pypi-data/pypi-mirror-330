![Logo](https://codeberg.org/screwery/pawpyrus/raw/branch/main/logo.svg)

## Description

![PyPI - Version](https://img.shields.io/pypi/v/pawpyrus?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pawpyrus?style=flat-square)
![PyPI - Status](https://img.shields.io/pypi/status/pawpyrus?style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pawpyrus?style=flat-square)
![PyPI - License](https://img.shields.io/pypi/l/pawpyrus?style=flat-square)
![Gitea Issues](https://img.shields.io/gitea/issues/open/screwery/pawpyrus?gitea_url=https%3A%2F%2Fcodeberg.org&style=flat-square)
![Gitea Last Commit](https://img.shields.io/gitea/last-commit/screwery/pawpyrus?gitea_url=https%3A%2F%2Fcodeberg.org&style=flat-square)

Pawpyrus is a minimalist open-source paper data storage based on QR codes and ArUco.
It generates a PDF from any small-sized binary file (recommended size <100kb).
Further, the paper data storage can be scanned and decoded (recommended resolution 300dpi).

It can be useful if you need to backup data on paper:

* Encryption keys (e.g. [GnuPG](https://gnupg.org))
* File-based password databases (e.g. [KeePassXC](https://keepassxc.org))
* Cryptocurrency wallets

## Installation

The script is pure Python and a part of [PyPI](https://pypi.org/project/pawpyrus), so can be installed via *pip*:

```bash
python3 -m pip install pawpyrus
```

## Usage

Encoder:

```bash
pawpyrus Encode -n "Description" -i  "input.file" -o "output.pdf"
```

Also, pawpyrus can read data from stdin.
For example, encoding GPG public keys:

```bash
gpg --export 0xDEADBEEF | pawpyrus Encode -n "My pubkey" -i - -o "my-pubkey.pdf"
```

Decoder:

```bash
pawpyrus Decode -i "scan1.jpg" "scan2.png" "scan3.jpg" "masked/too/*.png" -o "output.file"
```

## Data Format

Pawpyrus uses a custom alphanumeric encoding, which is designed to store information in QR code quite effectively.
For now, that makes 4.3kb per A4 page (pixel size 0.6 mm).

## Got a Trouble?

**QR and ArUco detectors may fail on one or several blocks.**
The situation is totally normal, although uncomfortable.
It's fixed for now, with two detectors ([opencv](https://github.com/opencv/opencv-python) and [pyzbar](https://github.com/NaturalHistoryMuseum/pyzbar)) instead of one, but the bug may reappear in some circumstances.
That's why Debug Mode was implemented:

```bash
pawpyrus Decode -d "debug_dir" -i "scan1.jpg" "scan2.jpg" "scan3.jpg" -o "output.file"
```

With Debug Mode, you can inspect undetected QR codes, read them manually with any device you have, and create a file with text blocks which can be processed as well:

```bash
pawpyrus Decode "scan1.jpg" "scan2.jpg" "scan3.jpg" -t "unrecognized_codes.txt" -o "output.file"
```

If you have any idea how to fix the bug better, [give me a clue](https://codeberg.org/screwery/pawpyrus/issues).

## Similar Projects

1. [intra2net/paperbackup](https://github.com/intra2net/paperbackup)
2. [Paperback by Olly](https://ollydbg.de/Paperbak/) and [Wikinaut/paperback-cli](https://github.com/Wikinaut/paperback-cli)
3. [colorsafe/colorsafe](https://github.com/colorsafe/colorsafe)
4. [Twibright Optar](http://ronja.twibright.com/optar)
5. [Paperkey](https://www.jabberwocky.com/software/paperkey)
6. [4bitfocus/asc-key-to-qr-code](https://github.com/4bitfocus/asc-key-to-qr-code)
