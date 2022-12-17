#Ledtrix
An abbreviation of matrix and led (as in light emitting diode). It is a module consisting of four smaller 8x8 cheap led modules. This repo provides some necessities to drive the module, as it is put together in a confusing way.

It consists of three parts:

 - Firmware (not yet developed as no driver circuit has been made. An Arduino will do for now)
 - A tool to generate graphics. This is a simple HTML page with some Javascript to visualize the leds being on or off. The output is a python formatted array which can be added to patterns.py
 - A translator that translates the row and column patterns generated with the tool into a C-formatted code. This code is used by a driver to shift bits into the four shift registers in the correct way.