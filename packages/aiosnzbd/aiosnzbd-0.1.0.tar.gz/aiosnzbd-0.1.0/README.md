# aiosnzbd

`aiosnzbd` is a lightweight and easy-to-use Asynchronous Python library that simplifies interactions with the SABnzbd API. It provides a convenient way to integrate SABnzbd functionality into your asynchronous Python applications, allowing you to manage and automate NZB downloads programmatically.

## Features

- Authenticate using your API key.
- Access SABnzbd's API endpoints with minimal setup.
- Includes All Functionalities


## Installation

Install the library using pip:

```bash
pip install aiosnzbd
```

## Usage

Here's a quick example of how to use the library:

```python

from aiosnzbd import SabnzbdClient
import asyncio

async def add_download_(file_path):
	client = SabnzbdClient(host="http://localhost", api_key="your_api_key")

	add_nzb = await client.add_uri(file=nzb_file)

	progress = await client.get_downloads(nzo_ids=add_nzb.get("nzo_ids")[0])

	print(progress)

	await client.close()


nzb_file = "file.nzb"
asyncio.run(add_download_(nzb_file))

```

## Requirements

- Python 3.9+

## Credits

This package was inspired by and built upon the work of **anasty17**.
