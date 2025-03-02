# lovense-api-wrapper

## Overview

This is a simple Python wrapper for the **[Lovense Standard API](https://developer.lovense.com/docs/standard-solutions/standard-api.html#game-mode)**, developed to use in my personal projects. It implements one of the several available API methods and provides basic functionality. The library is fully functional and documented, most of the code is from [catboy1357](https://github.com/catboy1357), with a few enhancements made by myself.

## Features

### **From lovense.api**

- **get_toys()**: Gets the toy(s) connect to the Lovense app
- **get_toys_name()**: Same as get_toys() but just the name of the devices
- **preset_request()**: Send one of the pre-made or user created patterns
- **function_request()**: Send a single Pattern immediately
- **pattern_request()**: Avoids network pressure of multiple function commands
- **stop()**: Sends a stop immediately command
- **decode_response()**: Make the return value of any command more readable.
- **pattern_request_raw()**: More api accurate version for patterns (advanced)
- **send_command()**: Send a JSON command directly to the app (advanced)

## Installation

You can install the library using pip:

```bash
pip install pylovense
```

## Usage

Here's a basic example of how to use the library:

```python
from pylovense.api import GameModeWrapper

love = GameModeWrapper("My Test App", "10.0.0.69", log=True) # will log output to terminal, alternatively wrap the functions inside print statements
love.get_toys()
love.preset_request(love.presets.PULSE, time=5)
```

> **Note: Setup the Lovense Remote App as follows:**
>
> 1. Lovense Remote App -> Discover -> Game Mode -> Enable LAN,
> 2. Take node of the Local IP, and Port. It should match the GameModeWrapper constructor

## Todo

If you are keen to add more to this library, here are the implemented API methods:

- [x] Standard API / By local application
- [ ] Standard API / By server qr code
- [ ] Standard Socket API / By local
- [ ] Standard Socket API / By server
- [ ] Events API

These are all the API endpoints in the Standard API solution. Other API solutions seam less useful in the context of python.

## MIT License

Copyright (c) 2025 jinxed-catgirl 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


## Disclaimer

This library was created for personal use and is provided "as-is" without any warranties or guarantees. Use it at your own risk.

---
