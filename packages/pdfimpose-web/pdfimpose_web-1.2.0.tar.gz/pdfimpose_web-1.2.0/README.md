# pdfimpose-web 📕 The code powering https://pdfimpose.it

## Installation

```sh
python3 -m pip install pdfimpose-web
```

## Run the application

Run the application using the following command.

```sh
python3 -m flask --app pdfimposeweb run
```

You can now use pdfimpose-web at: http://localhost:5000.

Note that you might want to configure the application using the settings described in the following section.

## Settings

This application can be run with default settings (but with default settings, data might be reset if you restart it).

To configure it:

- download file [`pdfimposeweb/settings/default.py`](https://framagit.org/spalax/pdfimpose-web/-/raw/main/pdfimposeweb/settings/default.py?inline=false) to your disk,
- change it (it is self-documented),
- tell `pdfimpose-web` to use it:

  ```sh
  export PDFIMPOSEWEB_SETTINGS=/path/to/settings.py
  python3 -m flask --app pdfimposeweb run
  ```

## Cleaning

Files uploaded by users are stored during one hour by default. This can be changed in the setting file.

A thread is launched at startup to clean those files. This can be disabled in the setting file. If disabled, the script ``pdfimposeweb.clean`` can be run periodically (e.g. in a crontab) to remove old uploaded PDF files. Note that the very same configuration used to run the application must be used to run this script:

```sh
export PDFIMPOSEWEB_SETTINGS=/path/to/settings.py
python3 -m pdfimposeweb.clean
```
