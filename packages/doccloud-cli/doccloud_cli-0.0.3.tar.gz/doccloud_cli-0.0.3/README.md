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
</div>

A simple CLI tool to enable interacting with DocumentCloud from the comfort of the terminal. Uses the [python-documentcloud](https://github.com/muckrock/python-documentcloud) wrapper of the DocumentCloud API, as well as the excellent [Typer](https://github.com/fastapi/typer) CLI library.

## Features ##
- Logging into DocumentCloud
- Searching for documents (with hyperlinking!)
- Uploading documents
- Viewing/saving the full text of documents as parsed by DocumentCloud (your mileage may vary)

## TODO (last updated Feb 16 2025) ##
- Improve uploading functionality (uploading from URL)
- Support for viewing/adding/deleting annotations
- Improve search functionality (ability to fetch more metadata)

## Contributing
1. Fork it (<https://github.com/leadbraw/doccloud-tool/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
