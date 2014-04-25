#!/usr/bin/python

#Simple python script to make SSOP (possibly TSSOP or other SMD footprints
#from basic dimensional data. Outputs a .mod file for use with kicad

#see loadConstants() for all the valid parameters. Note the only allowed
#string is NAME.
#Files should be formatted like this: (excluding the #'s)

#NAME SSOP14
#SPACING 0.65
#NUM_PINS = 14

#Any parameters left out will default to the ones specified in loadConstants

#This programs writes to stdout. If you want to write to a file use:
#python genSSOP.py configFile > outputFile.mod
import sys

FILE_HEADER = """
(module %s (layer F.Cu)
  (at 0 0)
  (tags "CMS SSOP SMD")
  (attr smd)
  (fp_text reference %s (at 0 -0.635) (layer F.SilkS)
    (effects (font (size 0.762 0.762) (thickness 0.127)))
  )
  (fp_text value Val** (at 0 0.635) (layer F.SilkS)
    (effects (font (size 0.762 0.762) (thickness 0.127)))
  )
"""

def main(argv):
    if len(argv) > 2:
        print_help();
        return;
    
    constants = loadConstants(None)
    printHeader(constants)
    printOutline(constants)
    printPads(constants)
    printTail()
    
def loadConstants(fileToLoad) :
    #defualt to values for SSOP14
    #all are metric in mm
    constants = {};
    constants["NAME"] = "SSOP14"
    constants["SPACING"] = 0.65
    constants["PAD_WIDTH"] = 0.40
    constants["PAD_HEIGHT"] = 1.20
    constants["TOTAL_LENGTH"] = 6.50
    constants["SPACE_BETWEEN_PADS"] = 5.70
    constants["NUM_PINS"] = 14

    if fileToLoad is None:
        return constants

    f = open(fileToLoad)
    for line in f:
        if f[0] == '#':
            continue
        words = line.split()
        if words[0] in constants:
            constants[word[0]] = float(words[1])
        elif word[0] == "NAME":
            constants["NAME"] = words[1]
        else:
            print ("INVALID PARAMETER:", words[0])
    return constants

"""
prints the outline to stdout
constants - the constants to use
"""
def printOutline(constants):
    halfLength = constants["TOTAL_LENGTH"] * 0.5
    halfHeight = constants["SPACE_BETWEEN_PADS"] * 0.5
    print("  (fp_line (start %f %f) (end %f %f) (layer F.SilkS) (width 0.12954))" % (-halfLength, -halfHeight,  halfLength, -halfHeight))
    print("  (fp_line (start %f %f) (end %f %f) (layer F.SilkS) (width 0.12954))" % ( halfLength, -halfHeight,  halfLength,  halfHeight))
    print("  (fp_line (start %f %f) (end %f %f) (layer F.SilkS) (width 0.12954))" % ( halfLength,  halfHeight, -halfLength,  halfHeight))
    print("  (fp_line (start %f %f) (end %f %f) (layer F.SilkS) (width 0.12954))" % (-halfLength,  halfHeight, -halfLength, -halfHeight))
    centerx = -halfLength+0.3*halfHeight
    centery = halfHeight*0.7
    radius = halfHeight*0.2
    print("  (fp_circle (center %d %d) (end %d %d) (layer F.SilkS) (width 0.12954))" % (centerx, centery, centerx, centery+radius))

def printPads(constants):
    distToPadCenter = (constants["PAD_HEIGHT"] + constants["SPACE_BETWEEN_PADS"]) / 2
    halfPins = constants["NUM_PINS"] / 2
    pos = 0
    pos2 = 0
    if halfPins % 2 == 0: #even
        pos = -(halfPins-1) * constants["SPACING"] / 2
        pos2 = (halfPins-1) * constants["SPACING"] / 2
    else :
        pos = -(halfPins//2) * constants["SPACING"]
        pos2 = (halfPins//2) * constants["SPACING"]
    for i in range(1,int(halfPins)+1):
        print("  (pad %d smd rect (at %f %f) (size %f %f) (layers F.Cu F.Paste F.Mask))" 
            % (i         ,pos , distToPadCenter,constants["PAD_WIDTH"],constants["PAD_HEIGHT"]))
        print("  (pad %d smd rect (at %f %f) (size %f %f) (layers F.Cu F.Paste F.Mask))"
            % (i+halfPins,pos2,-distToPadCenter,constants["PAD_WIDTH"],constants["PAD_HEIGHT"]))
        pos  += constants["SPACING"]
        pos2 -= constants["SPACING"] 

def printHeader(constants):
    print(FILE_HEADER % (constants["NAME"], constants["NAME"]))

def printTail():
    print(")")

def print_help():
    print ("Usage: python genSSOP.py configFile\n");

main(sys.argv)
