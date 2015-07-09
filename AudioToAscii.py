# -*- coding: utf-8 -*-

#Note that Viewers are never exported
#This file was automatically generated by Natron PyPlug exporter version 1.
import NatronEngine

# extra lib added
import os, time
from os import *

def getPluginID():
    return "AudioToAscii"

def getLabel():
    return "AudioToAscii"

def getVersion():
    return 1

def getIconPath():
    return "AudioToAscii.png"

def getGrouping():
    return "Other"

def getDescription():
    return "Launch external bash script Audio2Ascii (only linux).\nIt convert audio file into ascii curve that you can import in the Natron curve editor.\You can download it at https://github.com/rcspam/audio2ascii)\nYou must have it in your $PATH."
    
# extra defs added

def audioToAscii(audioFileATA, asciiFileATA, dimATA, fpsATA, durationATA, xHeightATA, yHeightATA):
    # Change the call to audio2ascii executable here	
    exec_a2a = str("audio2ascii.sh ")
    # Files to pass
    files_a2a = str("'" + str(audioFileATA) + "' '" + str(asciiFileATA) + "' ")
    # Param to pass
    param_a2a = str(dimATA) + " " +  str(fpsATA) + " " +  str(durationATA) + " " +  str(xHeightATA)  + " " + str(yHeightATA)
    # Launch audio2ascii
    ret_a2a = os.system(exec_a2a + files_a2a + param_a2a )
    return ret_a2a

def animCurves(thisParam, fileAC, dimAC, fpsAC, durationAC ,frameStartAC):
    # ascii file
    asciiAC = open(fileAC, "r")
    # end frame
    lineAC = int(fpsAC) * int(durationAC) + int(frameStartAC)
    # anim x
    if dimAC == 0:
        # reset x before recalculate
        thisParam.removeAnimation(0)
        for frameC in range(int(frameStartAC),lineAC + int(frameStartAC)):
            x = asciiAC.readline()
            thisParam.setValueAtTime(float(x), frameC, 0)
    # anim y
    elif dimAC == 1:
        # reset y before recalculate
        thisParam.removeAnimation(1)
        for frameC in range(int(frameStartAC),lineAC):
            y = asciiAC.readline()
            thisParam.setValueAtTime(float(y), frameC, 1)
    # anim yx
    else:
        # reset x and y before recalculate
        thisParam.removeAnimation(0)
        thisParam.removeAnimation(1)
        for frameC in range(int(frameStartAC),lineAC):
            x, y = asciiAC.readline().split ("_")
            thisParam.setValueAtTime(float(x), frameC, 0)
            thisParam.setValueAtTime(float(y), frameC, 1)

def paramHasChanged(thisParam, thisNode, thisGroup, app, userEdited):
    # audio input file
    audio_file = thisNode.inputFile.get()
    # ascii output file
    ascii_file = thisNode.curveFile.get()
    # external editing app
    ext_edit_app = thisNode.editApp.get()
    ext_edit_app_param = thisNode.editParam.get()
    
    # convert dimension in comprehensive thing for audio2ascii script 
    dim = thisNode.dimEnsion.get()
    if dim == 0:
        dimension = "x"
    elif dim == 1:
        dimension = "y"
    elif dim == 2:
        dimension = "xy" 

    # edit with External app
    if audio_file and ext_edit_app and thisParam == thisNode.editAudio:
        os.system(ext_edit_app + " " + ext_edit_app_param + " '" + audio_file + "' &")
    # doesn't work ?!
    #else:
        #app.warningDialog("Audio File", "You need to set a audio editor to edit an audio file")

    # Import Curve
    if ascii_file is not None and audio_file is not None and thisParam == thisNode.importCurve:
        ret_exec = audioToAscii(audio_file, ascii_file, dimension, thisNode.framesPerSec.get(), thisNode.duraTion.get(), thisNode.xHeight.get(), thisNode.yHeight.get())
        # test and wait end of audio2ascii 
        if ret_exec == 0:
            # calculate animation 
            animCurves(thisNode.curveIn, ascii_file, thisNode.dimEnsion.get(), thisNode.framesPerSec.get(), thisNode.duraTion.get(), thisNode.atFrameNum.get())
            

## / extra defs

def createInstance(app,group):

    #Create all nodes in the group
    lastNode = app.createNode("fr.inria.built-in.Output", 1, group)
    lastNode.setScriptName("Output1")
    lastNode.setLabel("Output1")
    lastNode.setPosition(758.75, 325.125)
    lastNode.setSize(104, 44)
    lastNode.setColor(0.699992, 0.699992, 0.699992)
    groupOutput1 = lastNode

    param = lastNode.getParam("Output_layer_name")
    if param is not None:
        param.setValue("RGBA")
        param.setVisible(False)
        del param

    param = lastNode.getParam("highDefUpstream")
    if param is not None:
        param.setVisible(False)
        del param

    del lastNode



    lastNode = app.createNode("fr.inria.built-in.Input", 1, group)
    lastNode.setScriptName("Input1")
    lastNode.setLabel("Input1")
    lastNode.setPosition(758.75, 161.125)
    lastNode.setSize(104, 44)
    lastNode.setColor(0.300008, 0.500008, 0.2)
    groupInput1 = lastNode

    param = lastNode.getParam("Output_layer_name")
    if param is not None:
        param.setValue("RGBA")
        param.setVisible(False)
        del param

    param = lastNode.getParam("highDefUpstream")
    if param is not None:
        param.setVisible(False)
        del param

    del lastNode

    #Create the parameters of the group node the same way we did for all internal nodes
    lastNode = group
    param = lastNode.getParam("highDefUpstream")
    if param is not None:
        param.setVisible(False)
        del param

    param = lastNode.getParam("onParamChanged")
    if param is not None:
        param.setValue("AudioToAscii.paramHasChanged")
        del param


    #Create the user-parameters
    lastNode.userNatron = lastNode.createPageParam("userNatron", "Settings")
    param = lastNode.createFileParam("inputFile", "Audio File")
    param.setSequenceEnabled(False)

    #Add the param to the page
    lastNode.userNatron.addParam(param)

    #Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(False)
    lastNode.inputFile = param
    del param

    # Group /
    param = lastNode.createGroupParam("setEditor", "Editor setting")

    #Add the param to the page
    lastNode.userNatron.addParam(param)

    #Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setEvaluateOnChange(False)
    lastNode.setEditor = param
    del param

    param = lastNode.createFileParam("editApp", "Audio Editor")
    param.setSequenceEnabled(False)

    #Add the param to the group, no need to add it to the page
    lastNode.setEditor.addParam(param)

    #Set param properties
    param.setHelp("Set the Audio Editor path")
    param.setAddNewLine(True)
    param.setAnimationEnabled(False)
    param.setDefaultValue("audacity")
    lastNode.editApp = param
    del param

    param = lastNode.createStringParam("editParam", "Audio editor parameters")
    param.setType(NatronEngine.StringParam.TypeEnum.eStringTypeDefault)
    param.setDefaultValue("")

    #Add the param to the group, no need to add it to the page
    lastNode.setEditor.addParam(param)

    #Set param properties
    param.setHelp("Set the Audio Editor command line parameters")
    param.setVisible(True)
    param.setAddNewLine(False)
    param.setAnimationEnabled(True)
    lastNode.editParam = param
    del param
    # / Group
    
    param = lastNode.createButtonParam("editAudio", "Edit audio File")

    #Add the param to the page
    lastNode.userNatron.addParam(param)

    #Set param properties
    param.setHelp("Set an audio editor in the tab 'Editor Setting")
    param.setAddNewLine(False)
    param.setPersistant(False)
    param.setEvaluateOnChange(False)
    lastNode.editAudio = param
    del param

    param = lastNode.createFileParam("curveFile", "Curve File")
    param.setSequenceEnabled(False)

    #Add the param to the page
    lastNode.userNatron.addParam(param)

    #Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(False)
    param.setDefaultValue("/tmp/curve.ascii")
    lastNode.curveFile = param
    del param

    param = lastNode.createChoiceParam("dimEnsion", "Dimension")
    entries = [ ("x", ""),
    ("y", ""),
    ("xy", "")]
    param.setOptions(entries)
    del entries

    #Add the param to the page
    lastNode.userNatron.addParam(param)

    #Set param properties
    param.setHelp("Dimension curve folowing 'x axe', 'y axe' or 'x and y axes'")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    options = param.getOptions()
    foundOption = False
    for i in range(len(options)):
        if options[i] == "x":
            param.setValue(i)
            foundOption = True
            break
    if not foundOption:
        app.writeToScriptEditor("Could not set option for parameter dimEnsion of node AudioToAscii1")
    lastNode.dimEnsion = param
    del param

    param = lastNode.createIntParam("framesPerSec", "Frame Rate")
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(100, 0)
    param.setDefaultValue(24, 0)

    #Add the param to the page
    lastNode.userNatron.addParam(param)

    #Set param properties
    param.setHelp("Calculate curve with this frame rate")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.framesPerSec = param
    del param

    param = lastNode.createIntParam("duraTion", "Duration")
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(200, 0)
    param.setDefaultValue(3, 0)

    #Add the param to the page
    lastNode.userNatron.addParam(param)

    #Set param properties
    param.setHelp("Duration of the curve in seconds")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.duraTion = param
    del param

    param = lastNode.createIntParam("xHeight", "x curve height")
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(500, 0)
    param.setDefaultValue(100, 0)

    #Add the param to the page
    lastNode.userNatron.addParam(param)

    #Set param properties
    param.setHelp("Height of x deviation in pixels")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.xHeight = param
    del param

    param = lastNode.createIntParam("yHeight", "y curve height")
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(500, 0)
    param.setDefaultValue(100, 0)

    #Add the param to the page
    lastNode.userNatron.addParam(param)

    #Set param properties
    param.setHelp("Height of y deviation in pixels")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.yHeight = param
    del param

    param = lastNode.createIntParam("atFrameNum", "Start at frame")
    param.setDisplayMinimum(1, 0)
    param.setDisplayMaximum(500, 0)
    param.setDefaultValue(1, 0)

    #Add the param to the page
    lastNode.userNatron.addParam(param)

    #Set param properties
    param.setHelp("Start the generate curve at this frame on the time")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.atFrameNum = param
    del param

    param = lastNode.createButtonParam("importCurve", "Generate the curve")

    #Add the param to the page
    lastNode.userNatron.addParam(param)

    #Set param properties
    param.setHelp("Generate curve from parameters above")
    param.setAddNewLine(True)
    param.setPersistant(False)
    param.setEvaluateOnChange(False)
    lastNode.importCurve = param
    del param
    
    param = lastNode.createDouble2DParam("curveIn", "Curve ")
    param.setMinimum(-2.14748e+09, 0)
    param.setMaximum(2.14748e+09, 0)
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(500, 0)
    param.setMinimum(-2.14748e+09, 1)
    param.setMaximum(2.14748e+09, 1)
    param.setDisplayMinimum(0, 1)
    param.setDisplayMaximum(500, 1)

    #Add the param to the page
    lastNode.userNatron.addParam(param)

    #Set param properties
    param.setHelp("x and y curve generate by the Generate button")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.curveIn = param
    del param

    # extra callback added
    app.AudioToAscii1.onParamChanged.set("AudioToAscii.paramHasChanged")    

    #Refresh the GUI with the newly created parameters
    lastNode.refreshUserParamsGUI()
    del lastNode

    #Now that all nodes are created we can connect them together, restore expressions
    groupOutput1.connectInput(0, groupInput1)

