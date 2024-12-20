# nuitrack-touchdesigner-bridge

This is a Python script that sends skeleton data obtained using the [Nuitrack SDK](https://github.com/3DiVi/nuitrack-sdk) via the OSC protocol.

## Installation

1. Install the required Python packages.

   ```bash
   pip install -r requirements.txt
   pip install [*.whl] # replace with filepath or URL for Nuitrack whl file

   # example
   # pip install https://github.com/3DiVi/nuitrack-sdk/raw/65662c9067a831c928e7300e427651e0dbe2ed9c/PythonNuitrack-beta/pip_packages/dist/windows/py_nuitrack_windows_python3.10-0.1.0-py3-none-any.whl
   ```

   You can download the whl file from [here](https://github.com/3DiVi/nuitrack-sdk/tree/master/PythonNuitrack-beta/pip_packages/dist).

1. Copy the `.env.sample` file to create a `.env` file and enter the necessary information.

   ```bash
   cp .env.sample .env
   ```

   The `.env` file should include the following information:

   ```
   REALSENSE_SERIAL_NUMBER="Your camera's serial number"
   NUITRACK_API_KEY="Your Nuitrack API key"
   ```

## Usage

1. Run the script.

   ```bash
   python nuitrack.py
   ```

1. By default, OSC messages containing data for all joints are sent to `127.0.0.1:12345`.  
You can change this using the `-ip`, `-port`, and `-j` options as needed.

   ```bash
   python nuitrack.py -ip 192.168.1.10 -port 9000 -j head neck left_hand
   ```

1. To stop the script, press `Ctrl+C`.

## OSC Message Specification

OSC messages are structured as follows:

- **Address Pattern**: `/p{user_id}/{joint_name}:{axis}`
  - `user_id`: User ID of the skeleton
  - `joint_name`: Name of the joint (e.g., `head`, `neck`, `left_hand`, etc.)
  - `axis`: Coordinate axis (`tx`, `ty`, `tz`)

- **Arguments**: Sends the position data (x, y, z coordinates) of each joint in meters.

Example:
```
/p1/head:tx 0.5
/p1/head:ty 1.2
/p1/head:tz 0.8
```

## License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2024 @nariakiiwatani, @funatsufumiya (Anno Lab. Inc.)

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
```