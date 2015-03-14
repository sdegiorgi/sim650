# sim650 #

A humble approach for a Masters Course summer term 2010 at Stuttgart University of Applied Sciences.


---


## What ##

This is a python implementation of an IBM 650 simulator. This simulator implements the following operations:

```
00 NOP,01 HLT,10 AUP,11 SUP,14 DIV,15 ALO,16 SLO,19 MPY,20 STL,21 STU,24 STD,
44 NZU,45 NZE,46 BMI,60 RAU,61 RSU,64 DVR,65 RAL,66 RSL,69 LDD,71 PCH
```

The simulator is realized to a point, where all problems up to polynomials and heron's square root iteration were implementable and runnable with the simulator.

Missing operations:
```
22 SDA,23 SDI,30 SRT,31 SRD,35 SLT,36 SCT,47 BOV,84 TLU,17 AML,67 RAM,18 SML,68 RSM,90-99
```


---


## Why ##

The author was very unsatisfied with the capabilities of the available 650 simulators. Being very intrigued by this machine the idea to implement a fully working simulator came up.


---


## Proof of concept ##

Later that year the author actually went to Sindelfingen IBM Museum and punched the  codes to punchcards and tested them on a **real** IBM 650. (Yikes, what fun!!)


---


Implementations (where possible) based on Documentation and Bulletin
Collection at
  * http://www.piercefuller.com/collect/650man/index.html
especially
  * http://www.piercefuller.com/collect/650man/ibm-g24-5002.pdf


---


The following links might be of interest:
  * http://www.ibm.com/ibm/history/exhibits/650/650_album.html (images)
  * http://www.ibm.com/de/ibm/unternehmen/geschichte/museum.html ("Haus zur Geschichte der IBM Datenverarbeitung")
  * http://www.piercefuller.com/paul/index.html (Mr Pierce has an impressive collection of machines)