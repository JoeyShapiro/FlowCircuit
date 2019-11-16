import math
from tkinter import *
def main():
    SIZE = 0
    end = False

    print("hello world")
    SIZE = input("Size of the circtui (n*n)")
    #createTable(SIZE)

    circuit = grid(SIZE)
    circuit.print_grid()

    while end != True:
        cmd = input("debug console, enter valid command, type help or end: ")
        cmdList = cmd.split()

        if cmdList[0] == "changeSize":
            circuit.changeSize()

        if cmdList[0] == "changeElement":
            location = cmdList[1]
            newShape = cmdList[2]
            circuit.changeElement(int(location), newShape)

        if cmdList[0] == "print":
            circuit.print_grid()

        if cmdList[0] == "printGrid":
            circuit.printGrid()

        if cmdList[0] == "compile":
            circuit.compile()
        
        if cmdList[0] == "scan":
            circuit.scan()
        
        if cmdList[0] == "changeConns": # find better way to do, input each connection
            location = cmdList[1]
            connUp = cmdList[2]
            connDown = cmdList[3]
            connLeft = cmdList[4]
            connRight = cmdList[5]
            circuit.changeConns(location, connUp, connDown, connLeft, connRight)

        if cmdList[0] == "displayElements":
            circuit.displayElements()
        
        if cmdList[0] == "help":
            print("changeSize")
            print("changeElement")
            print("print")
            print("printGrid")
            print("compile")
            print("scan")
            print("changeConns")
            print("displayElements")
            print("help")
            print("end")

        if cmdList[0] == "end":
            print("exiting debug console")
            end = True
    
class grid:
    dimensions = 16 # size of grid in length by width, default 4 * 4
    elements = [] * dimensions

    class element:
        connections = [0, 0, 0, 0] # up down left right
        shape = "null.png" # from ./images

        def __init__(self):
            self.connections = [0, 0, 0, 0] # default connections for element, by default no connections
            self.shape = "null.png" # default image used by default

        def changeShape(self, s):
            if s == "capacitor":
                self.shape = "capacitor.png"
                self.connections = [1, 1, 0, 0]
            if s == "inductor":
                self.shape = "inductor.png"
                self.connections = [1, 1, 0,0]
            if s == "resistor":
                self.shape = "resistor.png"
                self.connections = [1, 1, 0,0]
            if s == "source":
                self.shape = "source.png"
                self.connections = [1, 1, 0, 0]
            if s == "wire":
                self.shape = "wire.png"
                self.connections = [0, 0, 0, 0] # for wire connections must be sest later by user
        
        def changeWire(self, cu, cd, cl, cr):
            if self.shape == "wire.png":
                self.connections = [int(cu), int(cd), int(cl), int(cr)]
            else:
                print("shape is not a wire")


    def __init__(self, s):
        self.dimensions = int(s) * int(s)
        self.elements = [self.element() for i in range(self.dimensions)]

    # a whole new can of worms, will open it later
    def compile(self):
        sources = 0
        
        # search every point in the grid for a source, there should only be one
        for i in range(len(self.elements)):
            if self.elements[i].shape == "source.png":
                sources += 1
        if sources > 1:
            print("you have ", sources, " sources which is more than the one the circuit can have")
            return
        if sources < 1:
            print("you have ", sources, " sources which is less than the one the circuit needs")
            return
        print("you have a valid source")
        # follow connection of source to next element
        # continue to follow connection to next element until back at source or circuit breaks
        # if every "electron" returns to the source procede to next step
        # go back through the circuit doing all the math

    def print_grid(self):
        print(self.dimensions)
        print(self.elements)
    
    def printGrid(self):
        print(self.dimensions)
        k = 0
        for i in range(int(math.sqrt(len(self.elements)))):
            for j in range(int(math.sqrt(len(self.elements)))):
                print(self.elements[k].shape, end=' ')
                k += 1
            print("")

    def changeSize(self):
        newSize = input("Enter new grid size: ")
        self.dimensions = int(newSize) * int(newSize)
        self.elements = [self.element() for i in range(self.dimensions)] # grid has to be remade when size is changed, look into this

    def changeElement(self, i, e):
        currentElement = self.elements[i]
        currentElement.changeShape(e)

    def scan(self):
        sources = 0
        sourceIndex = 0
        
        # search every point in the grid for a source, there should only be one
        for i in range(len(self.elements)):
            if self.elements[i].shape == "source.png":
                sources += 1
                sourceIndex = i # if there is more than one it will throw an error anyway so it does not matter if it overlaps
        if sources > 1:
            print("you have ", sources, " sources which is more than the one the circuit can have")
            return
        if sources < 1:
            print("you have ", sources, " sources which is less than the one the circuit needs")
            return
        print("you have a valid source")

        # move to the next element
        nextElement = sourceIndex + int(math.sqrt(len(self.elements))) # move to the element under the source
        if self.elements[nextElement].shape == "null.png":
            print("there is no valid element at index:", nextElement)
            return
        # set the currentElement to the nextElement moving to the next element in the circuit
        currentElement = nextElement
        toPrevElementConn = 0 # the connection to go to the element before it, for a source at this point it should always be above it, TODO give better name
        while currentElement != sourceIndex: # TODO clean up can do this more efficiently
            currentConns = self.elements[currentElement].connections # pulls the array of connections for the current element
            nextElement = currentElement + int(math.sqrt(len(self.elements))) # TODO change to bool array to make easier to understand
            if (currentConns[0] == 1) and (0 != toPrevElementConn): # testing up connection
                nextElement = currentElement - int(math.sqrt(len(self.elements)))
                if nextElement > len(self.elements) - 1: # checks if the next element is out of range and returns
                    print("element connection goes out of range")
                    return
                if self.elements[nextElement].connections[1] == 1:
                    toPrevElementConn = 1
                    currentElement = nextElement # this does not account for multipathing, TODO after this works setup a way to deal with multipathing
            elif (currentConns[1] == 1) and (1 != toPrevElementConn): # testing down connection
                nextElement = currentElement + int(math.sqrt(len(self.elements)))
                if nextElement > len(self.elements) - 1:
                    print("element connection goes out of range")
                    return
                if self.elements[nextElement].connections[0] == 1:
                    toPrevElementConn = 0
                    currentElement = nextElement
            elif (currentConns[2] == 1) and (2 != toPrevElementConn): # testing left connection
                nextElement = currentElement - 1
                if nextElement > len(self.elements) - 1:
                    print("element connection goes out of range")
                    return
                if self.elements[nextElement].connections[3] == 1:
                    toPrevElementConn = 3
                    currentElement = nextElement
            elif (currentConns[3] == 1) and (3 != toPrevElementConn): # testing right connection
                nextElement = currentElement + 1
                if nextElement > len(self.elements) - 1:
                    print("element connection goes out of range")
                    return
                if self.elements[nextElement].connections[2] == 1:
                    toPrevElementConn = 2
                    currentElement = nextElement
            else: # default option if no valid connections
                print("no valid connections at index:", currentElement)
                return
            print("all connections valid")
    
    def changeConns(self, i, cu, cd, cl, cr):
        currentElement = self.elements[int(i)]
        currentElement.changeWire(cu, cd, cl, cr)

    def createGUI(self):
        master = Tk()
        for i in range(len(self.elements)):
            print("")

    # displays the elements of the array in a 2D format in the command prompt
    def displayElements(self):
        k = 0
        for j in range(int(math.sqrt(len(self.elements)))):
            # prints the top row of the elements in that row
            for i in range(int(math.sqrt(len(self.elements)))):
                print(" ", end='')
                if self.elements[k+i].connections[0] == 1:
                    print("|", end='')
                else:
                    print(" ", end='')
                print(" ", end='')
            print("")
            # prints the middle row of the elements in that row
            for i in range(int(math.sqrt(len(self.elements)))):
                if self.elements[k+i].connections[2] == 1:
                    print("_", end='')
                else:
                    print(" ", end='')
                if self.elements[k+i].shape == "source.png":
                    print("s", end='')
                elif self.elements[k+i].shape == "capacitor.png":
                    print("c", end='')
                elif self.elements[k+i].shape == "inductor.png":
                    print("i", end='')
                elif self.elements[k+i].shape == "resistor.png":
                    print("r", end='')
                elif self.elements[k+i].shape == "wire.png":
                    print("w", end='')
                else:
                    print("n", end='')
                if self.elements[k+i].connections[3] == 1:
                    print("_", end='')
                else:
                    print(" ", end='')
            print("")
            # prints the bottom row of the elements in that row
            for i in range(int(math.sqrt(len(self.elements)))):
                print(" ", end='')
                if self.elements[k+i].connections[1] == 1:
                    print("|", end='')
                else:
                    print(" ", end='')
                print(" ", end='')
            print("")
            k += int(math.sqrt(len(self.elements)))


def createTable(s):
    dimensions = int(s) * int(s)

    grid = [0] * dimensions
    connections = ["0000"] * dimensions # up down left right
    shape = ["null.png"] * dimensions # from ./images

    print(grid)
    print(connections[0])
    print(shape[0])

main()