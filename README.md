Main conversion code forked from [powpingdone/mbotmake] https://github.com/powpingdone/mbotmake.

This project adds a GUI for the mbotmake program to hopefuly make it more accessable to a wider audience. Most origional warnings still apply. I have personally tested this tool on a Makerbot Replicator+ with a Smart Extruder+ and had good results, but do not have access to any other physical machines for testing.

# Original Author's Note
This repository is unstable. Until I add basic stable support (full support for G0/1, G92, G90/91, bed, chamber, and nozzle heating) for all Makerbot Gen5 Printers, please use with caution. I am not responsible for any broken printers, but do feel free to [make an issue](https://github.com/sckunkle/mbotmake/issues) with what happened.

# mbotmake
A gcode to .makerbot (Gen 5+) conversion tool, compatable with marlin gcode.

# HOW TO USE 
## Windows/Mac
Download appropriate file from the [releases](https://github.com/chrys-the-flower/mbotmake_gui/releases/tag/release) page. Unzip and execute.
## Linux
Install Python 3.8 by your preferred means, then run the mbotmake_main.py file in the root of this repository.

## PrusaSlicer
Change these two settings in PrusaSlicer:
* Runs mbotmake automatically after exporting G-Code.<br><strong>[Print Settings] &rarr; [Output options] &rarr; [Post-processing scripts]:</strong><br>'[path to python] [.../]mbotmake -prusa'
* Generates the thumbnails for the Makerbot Replicator Gen5 display.<br><strong>[Printer Settings] &rarr; [General] &rarr; [G-code thumbnails]:</strong><br>
'55x40, 110x80, 320x200'

# PLANNED FEATURES

* Create a Ultimaker Cura plugin
* Add M600 (filament change) support
* Refactor the script into readable code
* Add working PursaSlicer config
* Add makerbot slice ending wipe

# REPORTING BUGS
Please supply a copy of your printer config, the generated .makerbot file, the gcode from your slicer, the makerbot you're using, and a detailed description of the bug you're experiencing. 

# CURRENTLY SUPPORTED PRINTERS
If you have a makerbot that use .makerbot files that isn't in this list, contact me at aidanzcase@gmail.com so that I can test how to properly convert to the printer specifications. 

* Makerbot Replicator Generation 5
