<div align="center">
<pre>                                         

██████╗  ██████╗  ██████╗ ██████╗██╗      ██████╗ ██╗   ██╗██████╗        ██████╗██╗     ██╗
██╔══██╗██╔═══██╗██╔════╝██╔════╝██║     ██╔═══██╗██║   ██║██╔══██╗      ██╔════╝██║     ██║
██║  ██║██║   ██║██║     ██║     ██║     ██║   ██║██║   ██║██║  ██║█████╗██║     ██║     ██║
██║  ██║██║   ██║██║     ██║     ██║     ██║   ██║██║   ██║██║  ██║╚════╝██║     ██║     ██║
██████╔╝╚██████╔╝╚██████╗╚██████╗███████╗╚██████╔╝╚██████╔╝██████╔╝      ╚██████╗███████╗██║
╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝        ╚═════╝╚══════╝╚═╝                                                                                                                                                       
python cli program for the DocumentCloud platform
</pre>
[![PyPI](https://img.shields.io/pypi/v/doccloud-cli.svg)](https://pypi.org/project/doccloud-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
</div>

A simple CLI tool to enable interacting with DocumentCloud from the comfort of the terminal. Uses the [python-documentcloud](https://github.com/muckrock/python-documentcloud) wrapper of the DocumentCloud API, as well as the excellent [Typer](https://github.com/fastapi/typer) CLI library.

## Installation
```
pip install doccloud-cli
```

## Examples
See all commands
```
doccloud-cli --help
```
Output:
```
 Usage: doccloud-cli.exe [OPTIONS] COMMAND [ARGS]...                                                       

╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                 │
│ --show-completion             Show completion for the current shell, to copy it or customize the        │
│                               installation.                                                             │
│ --help                        Show this message and exit.                                               │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────╮
│ search         Search DocumentCloud for a query. Optionally specify the number of results shown.        │
│ upload         Upload a document on your machine to DocumentCloud. Will prompt for username and         │
│                password if not entered initially.                                                       │
│ upload-dir     Upload a directory of documents on your machine to DocumentCloud as a Project. Will      │
│                prompt for project name, username, and password if not entered initially.                │
│ get-document   Fetches a document from the numeric ID and displays its metadata.                        │
│ view-text      View the text of a document as parsed by DocumentCloud. Your mileage may vary.           │
│ save-text      Saves the text of a document to a .txt file.                                             │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
Searching for documents with the term "Los Angeles". Optional argument to limit the amount of results displayed
```
doccloud-cli search "Los Angeles" 5
```
Output:
```
                                  Search Results                                  
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃  Contributor  ┃                Title                ┃ Creation Date ┃    ID    ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│  Rosanna Xia  │ 801 S. Los Angeles St., Los Angeles │  Jul 02 2013  │  723521  │
│  Rosanna Xia  │ 817 S. Los Angeles St., Los Angeles │  Jun 28 2013  │  719140  │
│  Rosanna Xia  │ 824 S. Los Angeles St., Los Angeles │  Jun 28 2013  │  719138  │
│ Online Staff  │         Los Angeles County          │  Aug 24 2021  │ 21048519 │
│ Cheryl Miller │        Los Angeles Response         │  Apr 26 2018  │ 4448284  │
└───────────────┴─────────────────────────────────────┴───────────────┴──────────┘

```
Uploading a document on your machine to DocumentCloud. You will be prompted for credentials if they are not included.
```
doccloud-cli upload C:\Users\name\Downloads\document.pdf username password
``` 
## Features ##
- Logging into DocumentCloud
- Searching for documents (with hyperlinking!)
- Uploading documents
- Viewing/saving the full text of documents as parsed by DocumentCloud (your mileage may vary)

## TODO ##
- Improve uploading functionality (uploading from URL)
- Support for viewing/adding/deleting annotations
- Improve search functionality (ability to fetch more metadata)

## Contributing
1. Fork it (<https://github.com/leadbraw/doccloud-cli/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
