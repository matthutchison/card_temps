## Summary
This is a set of scripts used to parse and display the FPGA processor temperature information for a Gatan K3 camera server as reported in the Digital Micrograph (DM) logs.  This is useful for determining if there are overheating problems and to see if the fans on any of the FPGAs has died (indicated by a sustained increase in the temperature of one processor).

## Requirements
This script requires a python installation of version 3.6 or higher. Matplotlib is required to use the --plot/-p option but is not required for the summary or csv output.

## Usage
The script can be run pointing at DM log files and/or zip files containing DM logs. These are located by default at c:\ProgramData\Gatan\Logs\. The default zipfile is DM.Archive.log and the log for the current day is <date>.DM.log, filling in the date in YYYY-MM-DD format for <date>. This makes the command to look at the log for 2021-07-27 `python3 c:\ProgramData\Gatan\Logs\2021-07-27.DM.log`.  When run without any parameters as `python3 card_temps.py` it will search the default log path for any .DM.log files and operate on them automatically.

This mode (no flags) will output a min/max/avg summary for each processor, calculated over the entirety of the input data. In some versions of DM the logged values are the same for both of the processors on a card, in newer versions the temperature of each processor is reported independenly.

Specifying --output <file> will write a csv file. The output will contain summary rows for each processor for each day in the input data. This can the be manipulated in other programs to further slice or analyze the data.

Specifying --plot (requires matplotlib) will plot the data on a per-processor basis in time-series, showing the min/max/avg values for each day.

Any day that has a zero is the result of a communication error occurring between DM and the card, during which it records 0.00 as the temperature.

## Notes
I've only been able to test this on microscopes that are maintained in very similar condition and which run nearly-identical versions of DM. I'm fairly sure that other versions may cause bugs. If you suspect there's a bug related to the DM version, please contact me and I'll try to take a look at it.
