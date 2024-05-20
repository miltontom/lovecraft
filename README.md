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
* `craft.ini` file with the necessary [configurations](#config) avaiable in the root of the project directory.
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
  --version  Show the version and exit.
  --help     Show this message and exit.
```
Running `lovecraft` with no path provided also works when you're in the project directory or by providing `.` as an argument.

## Config
```ini
; Sample craft.ini file
[Game]
name = myawesomegame
destination = .\
icon = assets\icon\icon.ico
```
* Certain assignments can be omitted, either comment or remove them.
* If no config file is found or certain assignments are omitted, there are fallback values:
    * `name` - Project directory name
    * `destination` - Home directory
* The `icon` is optional.
