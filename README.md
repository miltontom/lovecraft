<p align="center">
  <img src="logo/logo.png"/>
</p>

___
# LöveCraft

A simple CLI tool to package games made with LÖVE on Windows.

## Features
* Package games with just one command
* Easily add icon to the executable
* Each project can have it's own **LöveCraft** config file
* Great tool for consistent packaging

## Requirements
* [LÖVE](https://love2d.org/) framework available in `PATH`
* [ResourceHacker](https://www.angusj.com/resourcehacker/) available in `PATH` 
* Optional `craft.ini` file with the preferred [configurations](#config) avaiable in the root of the project directory.
* Optional `.exclude` file in the root of the project directory with files and folders in relative paths to avoid archiving before packaging the game.

**NOTE**: *Look inside the example folder for a sample game project*

## Installation
1. [Download](https://github.com/miltontom/lovecraft/releases) the binary.
2. Add the path to the binary location to the `PATH` environment variable.

## Usage
```
Usage: lovecraft.exe [OPTIONS] [SRC]

  Packages LÖVE game for distribution.

  SRC - Path to project directory

Options:
  -n, --name TEXT  Name for the game
  -i, --icon PATH  Path to '.ico' file
  --crafts-dir     Show the packaging location and exit.
  --version        Show the version and exit.
  --help           Show this message and exit.
```
* The packaged game is created in the `%USERPROFILE%\crafts` directory.
* The `--name` and `--icon` are optional and there are fallback values for them if not provided.
* Running `lovecraft` with no path provided also works when you're in the project directory or by providing `.` as an argument.

## Config
* You can create a config for the name and icon in the project's root if you're packaging
the game consistently.
* If `--name` or `--icon` is provided, the config file is not considered.
```ini
; Sample craft.ini file
[Game]
name = MyAwesomeGame
icon = assets\icon\icon.ico
```