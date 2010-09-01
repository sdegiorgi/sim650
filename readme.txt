IBM 650 Simulator v 0.4 beta

A humble approach for Concepts of Programming Languages
lecture Masters Course Software Technology summer term 2010
Stuttgart University of Applied Sciences.

Implementations (where possible) based on Documentation and Bulletin
Collection at http://www.piercefuller.com/collect/650man/index.html
especially http://www.piercefuller.com/collect/650man/ibm-g24-5002.pdf
(IBM 650 Data Processing System Bulletin, Basic Opertation Codes,
Program Optimizing, Program Loading).

Simulation includes Accumulator (upper,lower), Distributor, Drum and Input.
There is also a Word class to reflect a 10 byte word with sign. During the
process of execution there is also a class Instruction used (holds methods
like getOPCode, getDAddress and getIAddress). Please see provided demo
sources for more information.

Usage
Use the Python interpreter and import sim650. See runner.py for a demo run.
Make sure you are in the correct directory to be able to import (think of
it like the Java classpath).

Basic steps
x = sim650.sim650()                      # instantiate
x.loadSource("path/to/your/source.650")  # load source
x.run()                                  # executes source

Debugging
By issuing x.debug() you can step through the program with traceprints. Also
see description of x.manualCMD() for further details on how to debug.

Further Methods
x.dumpDrumData()           # dumps the whole drum to console
x.dumpPunchResult(address) # dump 10 words off drum starting at address to console
x.reset()                  # reset the machine (more or less) -
                           # e.g. to begin debug steps from 0000
x.manualCMD(word)          # manual issue a 10 byte word "0000000000" (with quotes!)
                           # to be executed as if it was the next instruction
                           # e.g. useful in debug mode
                           # please note that the resulting address of next instruction
                           # is saved in debugPos, so you can continue programm execution
                           # with x.debug() and the "new" next address then
x.dump[Lower|Upper]?Acc()  # Dumps the Value for lower, upper or the whole acc
x.checkSource(filename)    # Checks source code plausibility of given filename
x.runWithTraces()          # run()s the program but prints every step info on
                           # Step | Addr | Mne | OP | DAdd | IAdd | Distribut.
                           # Lower Accu and Upper Accu in a table
x.explainDrumData()        # dumps drum and tries to explain each word in a
                           # tabular form
x.setConsoleInput(value)   # sets the console input value (in theory use it before running
                           # a program, though a default value is set to 23)
x.getConsoleInput()        # reads the console input (that is address 8000)

Everything is public. So in console you can access for example
x.acc.lower.getValue() to get Lower Acc Value or
x.dist.getDistributorValue() to get Distributor Value or
x.drum.readData(address).getValue() to get the Value on drum position address.
When loading data to distributor (almost every data passes the distributor) the
simulation tries to detect addresses 8002 (Lower Acc) and 8003 (Upper Acc).
Find your way through the source code of this sim to find further methods.

Source Code
The sim expects one 10 byte word per line. Introduce a line with "~" (without the
quotes) to make a comment. You can prefix your 10 byte word with "-" to signal
a negative Value. See Known issues on negative values please. Please see provided
source codes to get the impression.

Implemented Operations
00 NOP,01 HLT,10 AUP,11 SUP,14 DIV,15 ALO,16 SLO,19 MPY,20 STL,21 STU,
24 STD,44 NZU,45 NZE,46 BMI,60 RAU,61 RSU,64 DVR,65 RAL,66 RSL,69 LDD,
71 PCH

Missing Operations
22 SDA Store Data Addy of Lower Acc
23 SDI Store Instr. Addy of Lower Acc
30 SRT Shift Right
31 SRD Shift Right and Round
35 SLT Shift Left
36 SCT Shift Left and Count
47 BOV Branch on Overflow
84 TLU Table Lookup
17 AML Add Magnitude to Lower
67 RAM Reset and Add Magnitude to Lower
18 SML Subtract Magnitude from Lower
68 RSM Reset and Subtract Magnitude from Lower
90-99 BD0-9 Branch on Digit 8 in a Distributor Pos

Further considerations
You can set maxIter and drumSize in class sim650 to define the maximum
number of iterations (sanity check contra endless loop) and the size
of the drum. Please be careful when submitting data to the system. This
sim relies heavily on design by contract thinking, so it will definately
follow the GIGO (Garbage in, Garbage out) principle :)

Known Issues
Sign checking is not really done consequently. Not all Operations have
been tested. Not all operations have been implemented. Output Layer
does not exist yet. Working with negatives values might cause problems,
not tested and used.

License
Implementation by Sandro Degiorgi, sandro@degiorgi.de

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

If you use it - pleae send me an email :)

