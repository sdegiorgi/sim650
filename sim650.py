"""
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
"""

class Operation():
    """Abstract baseclass for Operations"""
    def __init__(self,simRef,instructionRef):
        self.theApp = simRef
        self.instruction = instructionRef
    def getMnemonic(self): abstract
    def operate(self,instruction): abstract
    
class OperationDIV(Operation):
    def getMnemonic(self):
        return "DIV"
    def operate(self):
        self.theApp.dist.loadDistributor(self.instruction.getDAddress())
        uVal = self.theApp.acc.upper.getValue()
        lVal = self.theApp.acc.lower.getValue()        
        uHelper = "%010d"%(int(uVal))
        lHelper = "%010d"%(int(lVal))
        accVal = int(uHelper+lHelper)
        quot = accVal / int(self.theApp.dist.getDistributorValue())
        rema = accVal % int(self.theApp.dist.getDistributorValue())
        self.theApp.acc.upper.setValue(rema)
        self.theApp.acc.lower.setValue(quot)        
        return self.instruction.getIAddress()

class OperationDVR(Operation):
    def getMnemonic(self):
        return "DVR"
    def operate(self):
        self.theApp.dist.loadDistributor(self.instruction.getDAddress())
        uVal = self.theApp.acc.upper.getValue()
        lVal = self.theApp.acc.lower.getValue()        
        uHelper = "%010d"%(int(uVal))
        lHelper = "%010d"%(int(lVal))
        accVal = int(uHelper+lHelper)
        quot = accVal / int(self.theApp.dist.getDistributorValue())
        self.theApp.acc.resetLowerAndUpper()
        self.theApp.acc.lower.setValue(quot)        
        return self.instruction.getIAddress()

class OperationMPY(Operation):
    def getMnemonic(self):
        return "MPY"
    def operate(self):
        # this operation is implemented different to the info off ibm bulletin
        self.theApp.dist.loadDistributor(self.instruction.getDAddress())
        adder = int(self.theApp.dist.getDistributorValue()) * int(self.theApp.acc.upper.getValue())
        helper = "%020d"%(adder)
        self.theApp.acc.upper.setValue(helper[0:10])
        self.theApp.acc.lower.setValue(helper[10:])
        # TODO: combine upper acc with 0s (?)
        return self.instruction.getIAddress()

class OperationALO(Operation):
    def getMnemonic(self):
        return "ALO"
    def operate(self):
        self.theApp.dist.loadDistributor(self.instruction.getDAddress())
        # TODO: make sign analysis
        adder = int(self.theApp.dist.getDistributorValue()) + int(self.theApp.acc.lower.getValue())
        if adder > 9999999999:
            lowerVal = int(str(adder)[-10:])
            carryVal = int(str(adder)[:-10])
            self.theApp.acc.lower.setValue(lowerVal)
            self.theApp.acc.upper.setValue(int(self.theApp.acc.upper.getValue()) + carryVal)
        else:
            self.theApp.acc.lower.setValue(adder)
        # TODO: combine upper acc with 0s (?)
        return self.instruction.getIAddress()

class OperationAUP(Operation):
    def getMnemonic(self):
        return "AUP"
    def operate(self):
        self.theApp.dist.loadDistributor(self.instruction.getDAddress())
        # TODO: make sign analysis
        adder = int(self.theApp.dist.getDistributorValue()) + int(self.theApp.acc.upper.getValue())
        self.theApp.acc.upper.setValue(adder)
        # TODO: combine upper acc with 0s (?)
        return self.instruction.getIAddress()

class OperationSLO(Operation):
    def getMnemonic(self):
        return "SLO"
    def operate(self):
        self.theApp.dist.loadDistributor(self.instruction.getDAddress())
        adder = int(self.theApp.acc.lower.getValue()) - int(self.theApp.dist.getDistributorValue())
        self.theApp.acc.lower.setValue(adder)
        # TODO: combine upper acc with 0s (?)
        return self.instruction.getIAddress()

class OperationSUP(Operation):
    def getMnemonic(self):
        return "SUP"
    def operate(self):
        self.theApp.dist.loadDistributor(self.instruction.getDAddress())
        adder = int(self.theApp.acc.upper.getValue()) - int(self.theApp.dist.getDistributorValue())
        self.theApp.acc.upper.setValue(adder)
        # TODO: combine upper acc with 0s (?)
        return self.instruction.getIAddress()

class OperationRAL(Operation):
    def getMnemonic(self):
        return "RAL"
    def operate(self):
        self.theApp.dist.loadDistributor(self.instruction.getDAddress())
        self.theApp.acc.resetLowerAndUpper()
        # TODO: make sign analysis
        #adder = int(self.theApp.dist.getDistributorValue()) + int(self.theApp.acc.lower.getValue())
        self.theApp.acc.lower.setValue(int(self.theApp.dist.getDistributorValue()))
        # TODO: combine upper acc with 0s (?)
        return self.instruction.getIAddress()

class OperationRSL(Operation):
    def getMnemonic(self):
        return "RSL"
    def operate(self):
        self.theApp.dist.loadDistributor(self.instruction.getDAddress())
        self.theApp.acc.resetLowerAndUpper()
        # TODO: make sign analysis
        #adder = int(self.theApp.dist.getDistributorValue()) + int(self.theApp.acc.lower.getValue())
        self.theApp.acc.lower.setValue(int(self.theApp.dist.getDistributorValue()))
        self.theApp.acc.lower.getSign(False)
        # TODO: combine upper acc with 0s (?)
        return self.instruction.getIAddress()

class OperationNZE(Operation):
    def getMnemonic(self):
        return "NZE"
    def operate(self):
        if int(self.theApp.acc.lower.getValue()) == 0 and int(self.theApp.acc.upper.getValue()) == 0:
            return self.instruction.getIAddress()
        else:
            return self.instruction.getDAddress()

class OperationBMI(Operation):
    def getMnemonic(self):
        return "BMI"
    def operate(self):
        # should definately check on sign here rather then doing math
        if (int(self.theApp.acc.lower.getValue()) < 0) or (int(self.theApp.acc.upper.getValue()) < 0):
            return self.instruction.getDAddress()
        else:
            return self.instruction.getIAddress()

class OperationNZU(Operation):
    def getMnemonic(self):
        return "NZU"
    def operate(self):
        if int(self.theApp.acc.upper.getValue()) == 0:
            return self.instruction.getIAddress()
        else:
            return self.instruction.getDAddress()

class OperationLDD(Operation):
    def getMnemonic(self):
        return "LDD"
    def operate(self):
        self.theApp.dist.loadDistributor(self.instruction.getDAddress())
        return self.instruction.getIAddress()

class OperationSTD(Operation):
    def getMnemonic(self):
        return "STD"
    def operate(self):
        self.theApp.drum.storeData(self.instruction.getDAddress(),self.theApp.dist.getDistributorValue())
        return self.instruction.getIAddress()

class OperationSTL(Operation):
    def getMnemonic(self):
        return "STL"
    def operate(self):
        self.theApp.dist.loadDistributorLowerAcc()
        self.theApp.drum.storeData(self.instruction.getDAddress(),self.theApp.dist.getDistributorValue())
        return self.instruction.getIAddress()

class OperationSTU(Operation):
    def getMnemonic(self):
        return "STU"
    def operate(self):
        self.theApp.dist.loadDistributorUpperAcc()
        self.theApp.drum.storeData(self.instruction.getDAddress(),self.theApp.dist.getDistributorValue())
        return self.instruction.getIAddress()

class OperationRAU(Operation):
    def getMnemonic(self):
        return "RAU"
    def operate(self):
        self.theApp.dist.loadDistributor(self.instruction.getDAddress())
        self.theApp.acc.resetLowerAndUpper()
        self.theApp.acc.upper.setValue(self.theApp.dist.getDistributorValue())
        return self.instruction.getIAddress()

class OperationRSU(Operation):
    def getMnemonic(self):
        return "RSU"
    def operate(self):
        self.theApp.dist.loadDistributor(self.instruction.getDAddress())
        self.theApp.acc.resetLowerAndUpper()
        self.theApp.acc.upper.setValue(self.theApp.dist.getDistributorValue())
        self.theApp.acc.upper.setSign(False)
        return self.instruction.getIAddress()

class OperationPCH(Operation):
    def getMnemonic(self):
        return "PCH"
    def operate(self):
        self.theApp.drum.dumpPunchResult(self.instruction.getDAddress())
        return self.instruction.getIAddress()

class OperationHLT(Operation):
    def getMnemonic(self):
        return "HLT"
    def operate(self):
        self.theApp.setRunning(False)
        return 9999

class OperationNOP(Operation):
    def getMnemonic(self):
        return "NOP"
    def operate(self):
        return self.instruction.getIAddress()

class sim650():
    """Humble approach to simulate / interpret ibm650 / sdegiorgi"""
    def __init__(self):
        self.consoleInput = 23
        self.maxIter      = 1000
        self.drumSize     = 100
        self.debugIter    = 0
        self.debugPos     = 1
        self.traces       = False
        self.drum         = Drum(self.drumSize)
        self.acc          = Accumulator()
        self.dist         = Distributor(self)
        self.input        = Input(self)
        self.output       = Output()
        self.operations   = {00:OperationNOP,
                             01:OperationHLT,
                             10:OperationAUP,
                             11:OperationSUP,
                             14:OperationDIV,
                             15:OperationALO,
                             16:OperationSLO,
                             19:OperationMPY,
                             20:OperationSTL,
                             21:OperationSTU,
                             24:OperationSTD,
                             44:OperationNZU,
                             45:OperationNZE,
                             46:OperationBMI,
                             60:OperationRAU,
                             61:OperationRSU,
                             64:OperationDVR,
                             65:OperationRAL,
                             66:OperationRSL,
                             69:OperationLDD,
                             71:OperationPCH}
    def loadSource(self,filename):
        self.input.loadSource(filename)
    def checkSource(self,filename):
        self.input.checkSource(filename)
    def dumpDrumData(self):
        self.drum.dumpDrumData()
    def run(self):
        self.running = True
        self.iter = 0
        self.pos = 1
        while self.running and self.iter < self.maxIter:
            self.iter = self.iter + 1
            data = self.drum.readData(self.pos)
            currInstruction = Instruction(data)
            currOperation = self.operations[currInstruction.opCode](self,currInstruction)
            if self.traces:
                print "%5d | %04d | %s | %2s | %04d | %04d | %10s | %10s | %10s"%(self.iter,self.pos,currOperation.getMnemonic(),currInstruction.getOPCode(),int(currInstruction.getDAddress()),int(currInstruction.getIAddress()),self.dist.getDistributorValue(),self.acc.lower.getValue(),self.acc.upper.getValue())
            self.pos = currOperation.operate()
        print "finished after %s steps."%(self.iter)
    def setRunning(self,state):
        self.running = state
    def debug(self):
        self.debugIter = self.debugIter + 1
        print "doing step [%s], working on pos [%s]"%(self.debugIter,self.debugPos)
        data = self.drum.readData(self.debugPos)
        currInstruction = Instruction(data)
        currOperation = self.operations[currInstruction.opCode](self,currInstruction)
        print "executing %s [%s] [%04d] [%04d]"%(currOperation.getMnemonic(),currInstruction.getOPCode(),currInstruction.getDAddress(),currInstruction.getIAddress())
        self.debugPos = currOperation.operate()
        print "next calculated pos is [%s]"%(self.debugPos)
    def reset(self):
        self.debugIter = 0
        self.debugPos  = 1
        self.acc.resetLowerAndUpper()
        # maybe more here, distributor and drum reset or diff method
    def dumpPunchResult(self,address):
        self.drum.dumpPunchResult(address)
    def manualCMD(self,word):
        currentInstruction = Instruction(word)
        currOperation = self.operations[currInstruction.opCode](self,currInstruction)
        print "executing %s [%s] [%04d] [%04d]"%(currOperation.getMnemonic(),currInstruction.opCode,currInstruction.getDAddress(),currInstruction.getIAddress())
        self.debugPos = currOperation.operate()
        print "next calculated pos is [%s] (this is set also for debug mode)"%(self.debugPos)
    def dumpUpperAcc(self):
        print "Upper Acc Value [%s]"%(self.acc.upper.getValue())
    def dumpLowerAcc(self):
        print "Lower Acc Value [%s]"%(self.acc.lower.getValue())
    def dumpAcc(self):
        self.dumpLowerAcc()
        self.dumpUpperAcc()
    def runWithTraces(self):
        print " Step | Addr | Mne | OP | DAdd | IAdd | Distribut. | Lower Accu | Upper Accu"
        self.traces = True
        self.run()
        self.traces = False
    def explainDrumData(self):
        print " Addr | Mne | OP | DAdd | IAdd"
        for x in range(1,self.drumSize+1):
            currInstruction = Instruction(self.drum.readData(x))
            currOperation = self.operations[currInstruction.opCode](self,currInstruction)
            print " %04d | %s | %02d | %04d | %04d "%(x,currOperation.getMnemonic(),int(currInstruction.getOPCode()),int(currInstruction.getDAddress()),int(currInstruction.getIAddress()))
    def setConsoleInput(self,value):
        self.consoleInput = value
    def getConsoleInput(self):
        return self.consoleInput
            
class Instruction():
    """Representation of an instruction"""
    def __init__(self,data):
        self.opCode = int(data.getValue()[0:2])
        self.dAddress = int(data.getValue()[2:6])
        self.iAddress = int(data.getValue()[6:])
        self.sign = data.getSign()
    def getOPCode(self):
        return self.opCode
    def getDAddress(self):
        return self.dAddress
    def getIAddress(self):
        return self.iAddress
    def getSign(self):
        return self.sign
    
class Output():
    pass
   
class Input():
    """Input"""
    def __init__(self,simRef):
        self.theApp = simRef
    def readDataLines(self,filename):
        f = open(filename,'r')
        self.dataLines = f.readlines()
        f.close()
    def checkSource(self,filename):
        self.readDataLines(filename)
        for line in self.dataLines:
            str = line.rstrip()
            infoStr = "ERROR: Code line seems buggy"
            if self.validateIsCommentOrEmpty(str):
                infoStr = "Comment or too short, line will be ignored"
            elif self.validateCodeLine(str):
                infoStr = "Code line is ok"
            print "[%s] [%s]"%(str,infoStr)
                    
    def validateIsCommentOrEmpty(self,line):
        if len(line) < 10 or line[0] == "~":
            return True
        else:
            return False
    def validateCodeLine(self,line):
        if (len(line) == 10) or (len(line) == 11 and line[0] == "-"):
            try:
                dummyInt = int(line)
                return True
            except ValueError:
                print "Invalid Source Line [%s] (needs to be int)"%(line)
        return False
    def loadSource(self,filename):
        self.readDataLines(filename)
        instNum = 1
        for line in self.dataLines:
            str = line.rstrip()
            if  not self.validateIsCommentOrEmpty(line) and self.validateCodeLine(str):
                self.theApp.drum.storeData(instNum,str)
                instNum = instNum + 1

class Accumulator():
    """Accu"""
    def __init__(self):
        self.sign = "+"
        self.lower = Word()
        self.upper = Word()
    def resetLowerAndUpper(self):
        self.resetLower()
        self.resetUpper()
    def resetLower(self):
        self.lower.resetWord()
    def resetUpper(self):
        self.upper.resetWord()        

class Distributor():
    """Representation of Distributor"""
    def __init__(self,simRef):
        self.theApp = simRef
        self.value = Word()
    def loadDistributor(self,address):
        if address == 8002:
            self.loadDistributorLowerAcc()
        elif address == 8003:
            self.loadDistributorUpperAcc()
        elif address == 8000:
            self.loadConsoleInput()
        else:
            self.value = Word(self.theApp.drum.readData(address).getValue())
            self.value.setSign(self.theApp.drum.readData(address).getSign())
    def loadDistributorLowerAcc(self):
        self.value = Word(self.theApp.acc.lower.getValue())
        self.value.setSign(self.theApp.acc.lower.getSign())
    def loadDistributorUpperAcc(self):
        self.value = Word(self.theApp.acc.upper.getValue())
        self.value.setSign(self.theApp.acc.lower.getSign())
    def getDistributorValue(self):
        return self.value.getValue()
    def getDistributorSign(self):
        return self.value.getSign()
    def loadConsoleInput(self):
        self.value = Word(self.theApp.getConsoleInput())

class Drum():
    """The drum"""
    def __init__(self,drumSize):
        self.data = []
        for x in range(drumSize+1):
            self.data.append(Word())
    def dumpDrumData(self):
        for k,v in enumerate(self.data):
            print "%04d %s"%(k,v.getValue())
    def storeData(self,address,data):
        self.data[address].setValue(data)
    def readData(self,address):
        return self.data[address]
    def dumpPunchResult(self,address):
        for x in range(address,address+10):
            print "%04d %s"%(x,self.data[x].getValue())

class Word():
    """A ten digit word with sign"""
    def __init__(self,data=None):
        self.sign = True
        if data == None:
            self.resetWord()
        else:
            intData = int(data)
            if intData < 0:
                intData = intData * (-1)
                self.sign = False
            self.setValue(data)
    def setSign(self,sign):
        self.sign = sign
    def getSign(self):
        return self.sign
    def getValue(self):
        return self.value
    def setValue(self,value):
        self.value = "%010d"%(int(value))
    def resetWord(self):
        self.setValue("0000000000")
        self.setSign(True)
    def setWord(self,word): #troublesome, always need new instance ./
        intVal = int(word.getValue())
        if intVal < 0:
            intVal = intVal * (-1)
            word.setSign(False)
        word.setValue(intVal)
        self = word
    def getWord(self):
        return self
