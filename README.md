# LoveCraft

A simple CLI tool to package games made with LÖVE on Windows.

## Features
* Package games with just one command
* Easily add icon to the executable

## Requirements
* [LÖVE](https://love2d.org/) framework available in `PATH`
* [ResourceHacker](https://www.angusj.com/resourcehacker/) available in `PATH` 
* `conf.ini` file with the necessary [configurations](#config) avaiable in the root of the project directory.
* Optional `.avoid` file in the root of the project directory with files and folders in relative paths to avoid archiving before packaging the game.
* Paths specified in `conf.ini` and `.avoid` should use '\\' as the path separator.

**NOTE**: *Look inside the demo folder for a sample game project*

## Installation
1. [Download](https://github.com/miltontom/lovecraft/releases) the binary.
2. Add the path to the binary location to the `PATH` environment variable.

## Usage
```
Usage: lovecraft.py [OPTIONS] [SRC]

  Packages LÖVE game for distribution.

  SRC - Path to project directory

Options:
  --help  Show this message and exit.
```
Running `lovecraft` with no path provided also works when you're in the project directory or by providing `.` as an argument.

## Config
```ini
; Sample conf.ini file
[Game]
name = myawesomegame
destination = C:\Users\John Doe
icon = C:\Users\John Doe\Love\games\myawesomegame\assets\icon\icon.ico
```
* Certain assignments can be omitted, either comment or remove them.
* There are fallback values for, 
    * `name` - Project folder name
    * `destination` - Project folder 
* The `icon` is optional.