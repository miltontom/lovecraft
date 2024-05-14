# LoveCraft

A simple CLI tool to package games made with LÖVE.

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

## Usage
```powershell
lovecraft path\to\project\directory
```
Running `lovecraft` with no path also works when you're in the project directory or by providing `.` as an argument.

## Config
```ini
; Sample conf.ini file
[Game]
name = myawesomegame
destination_path = C:\Users\John Doe
icon = C:\Users\John Doe\Love\games\myawesomegame\assets\icon\icon.ico
```
* The `name` and `icon` can be kept with a blank assignment
* Mention the absolute paths for the `destination_path` and `icon` fields
* Please use the keys as it is