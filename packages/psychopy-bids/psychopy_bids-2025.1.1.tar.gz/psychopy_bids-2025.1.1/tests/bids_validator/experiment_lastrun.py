#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2024.2.5),
    on February 15, 2025, at 11:44
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
prefs.hardware['audioLib'] = 'ptb'
prefs.hardware['audioLatencyMode'] = '4'
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout, hardware
from psychopy.tools import environmenttools
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER, priority)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard
from psychopy_bids.bids import BIDSBehEvent
from psychopy_bids.bids import BIDSTaskEvent
from psychopy_bids.bids import BIDSError
from psychopy_bids.bids import BIDSHandler

# --- Setup global variables (available in all functions) ---
# create a device manager to handle hardware (keyboards, mice, mirophones, speakers, etc.)
deviceManager = hardware.DeviceManager()
# ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# store info about the experiment session
psychopyVersion = '2024.2.5'
expName = 'experiment'  # from the Builder filename that created this script
# information about this experiment
expInfo = {
    'participant': f"{randint(1, 4):06.0f}",
    'session': f"{randint(1, 3):03.0f}",
    'date|hid': data.getDateStr(),
    'expName|hid': expName,
    'psychopyVersion|hid': psychopyVersion,
}

# --- Define some variables which will change depending on pilot mode ---
'''
To run in pilot mode, either use the run/pilot toggle in Builder, Coder and Runner, 
or run the experiment with `--pilot` as an argument. To change what pilot 
#mode does, check out the 'Pilot mode' tab in preferences.
'''
# work out from system args whether we are running in pilot mode
PILOTING = core.setPilotModeFromArgs()
# start off with values from experiment settings
_fullScr = True
_winSize = [1440, 960]
# if in pilot mode, apply overrides according to preferences
if PILOTING:
    # force windowed mode
    if prefs.piloting['forceWindowed']:
        _fullScr = False
        # set window size
        _winSize = prefs.piloting['forcedWindowSize']

def showExpInfoDlg(expInfo):
    """
    Show participant info dialog.
    Parameters
    ==========
    expInfo : dict
        Information about this experiment.
    
    Returns
    ==========
    dict
        Information about this experiment.
    """
    # show participant info dialog
    dlg = gui.DlgFromDict(
        dictionary=expInfo, sortKeys=False, title=expName, alwaysOnTop=True
    )
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    # return expInfo
    return expInfo


def setupData(expInfo, dataDir=None):
    """
    Make an ExperimentHandler to handle trials and saving.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    dataDir : Path, str or None
        Folder to save the data to, leave as None to create a folder in the current directory.    
    Returns
    ==========
    psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    # remove dialog-specific syntax from expInfo
    for key, val in expInfo.copy().items():
        newKey, _ = data.utils.parsePipeSyntax(key)
        expInfo[newKey] = expInfo.pop(key)
    
    # data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    if dataDir is None:
        dataDir = _thisDir
    filename = u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        dataDir = os.path.commonprefix([dataDir, filename])
        filename = os.path.relpath(filename, dataDir)
    
    # an ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(
        name=expName, version='',
        extraInfo=expInfo, runtimeInfo=None,
        originPath='C:\\Users\\Lukas\\Desktop\\psychopy\\psychopy-bids\\tests\\bids_validator\\experiment_lastrun.py',
        savePickle=True, saveWideText=True,
        dataFileName=dataDir + os.sep + filename, sortColumns='time'
    )
    thisExp.setPriority('thisRow.t', priority.CRITICAL)
    thisExp.setPriority('expName', priority.LOW)
    # return experiment handler
    return thisExp


def setupLogging(filename):
    """
    Setup a log file and tell it what level to log at.
    
    Parameters
    ==========
    filename : str or pathlib.Path
        Filename to save log file and data files as, doesn't need an extension.
    
    Returns
    ==========
    psychopy.logging.LogFile
        Text stream to receive inputs from the logging system.
    """
    # set how much information should be printed to the console / app
    if PILOTING:
        logging.console.setLevel(
            prefs.piloting['pilotConsoleLoggingLevel']
        )
    else:
        logging.console.setLevel('debug')
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log')
    if PILOTING:
        logFile.setLevel(
            prefs.piloting['pilotLoggingLevel']
        )
    else:
        logFile.setLevel(
            logging.getLevel('debug')
        )
    
    return logFile


def setupWindow(expInfo=None, win=None):
    """
    Setup the Window
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    win : psychopy.visual.Window
        Window to setup - leave as None to create a new window.
    
    Returns
    ==========
    psychopy.visual.Window
        Window in which to run this experiment.
    """
    if PILOTING:
        logging.debug('Fullscreen settings ignored as running in pilot mode.')
    
    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=_winSize, fullscr=_fullScr, screen=0,
            winType='pyglet', allowGUI=False, allowStencil=False,
            monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height',
            checkTiming=False  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [0,0,0]
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'height'
    win.hideMessage()
    # show a visual indicator if we're in piloting mode
    if PILOTING and prefs.piloting['showPilotingIndicator']:
        win.showPilotingIndicator()
    
    return win


def setupDevices(expInfo, thisExp, win):
    """
    Setup whatever devices are available (mouse, keyboard, speaker, eyetracker, etc.) and add them to 
    the device manager (deviceManager)
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window in which to run this experiment.
    Returns
    ==========
    bool
        True if completed successfully.
    """
    # --- Setup input devices ---
    ioConfig = {}
    
    # Setup iohub keyboard
    ioConfig['Keyboard'] = dict(use_keymap='psychopy')
    
    # Setup iohub experiment
    ioConfig['Experiment'] = dict(filename=thisExp.dataFileName)
    
    # Start ioHub server
    ioServer = io.launchHubServer(window=win, **ioConfig)
    
    # store ioServer object in the device manager
    deviceManager.ioServer = ioServer
    
    # create a default keyboard (e.g. to check for escape)
    if deviceManager.getDevice('defaultKeyboard') is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='iohub'
        )
    if deviceManager.getDevice('keyRespImage') is None:
        # initialise keyRespImage
        keyRespImage = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='keyRespImage',
        )
    # return True if completed successfully
    return True

def pauseExperiment(thisExp, win=None, timers=[], playbackComponents=[]):
    """
    Pause this experiment, preventing the flow from advancing to the next routine until resumed.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    timers : list, tuple
        List of timers to reset once pausing is finished.
    playbackComponents : list, tuple
        List of any components with a `pause` method which need to be paused.
    """
    # if we are not paused, do nothing
    if thisExp.status != PAUSED:
        return
    
    # start a timer to figure out how long we're paused for
    pauseTimer = core.Clock()
    # pause any playback components
    for comp in playbackComponents:
        comp.pause()
    # make sure we have a keyboard
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        defaultKeyboard = deviceManager.addKeyboard(
            deviceClass='keyboard',
            deviceName='defaultKeyboard',
            backend='ioHub',
        )
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # sleep 1ms so other threads can execute
        clock.time.sleep(0.001)
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, win=win)
    # resume any playback components
    for comp in playbackComponents:
        comp.play()
    # reset any timers
    for timer in timers:
        timer.addTime(-pauseTimer.getTime())


def run(expInfo, thisExp, win, globalClock=None, thisSession=None):
    """
    Run the experiment flow.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    psychopy.visual.Window
        Window in which to run this experiment.
    globalClock : psychopy.core.clock.Clock or None
        Clock to get global time from - supply None to make a new one.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    # mark experiment as started
    thisExp.status = STARTED
    # make sure window is set to foreground to prevent losing focus
    win.winHandle.activate()
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = deviceManager.ioServer
    # get/create a default keyboard (e.g. to check for escape)
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='ioHub'
        )
    eyetracker = deviceManager.getDevice('eyetracker')
    # make sure we're running in the directory for this experiment
    os.chdir(_thisDir)
    # get filename from ExperimentHandler for convenience
    filename = thisExp.dataFileName
    frameTolerance = 0.001  # how close to onset before 'same' frame
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    # get frame duration from frame rate in expInfo
    if 'frameRate' in expInfo and expInfo['frameRate'] is not None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess
    
    # Start Code - component code to be run after the window creation
    bidsLogLevel = 24
    logging.addLevel('BIDS', 24)
    if expInfo['session']:
        bids_handler = BIDSHandler(dataset='bids',
         subject=expInfo['participant'], task=expInfo['expName'],
         session=expInfo['session'], data_type='func', acq='',
         runs=True)
    else:
        bids_handler = BIDSHandler(dataset='bids',
         subject=expInfo['participant'], task=expInfo['expName'],
         data_type='func', acq='', runs=True)
    bids_handler.createDataset()
    bids_handler.addLicense('CC-BY-SA-4.0', force=True)
    bids_handler.addTaskCode(force=True)
    bids_handler.addEnvironment()
    
    # --- Initialize components for Routine "visualStimuliText" ---
    textWord = visual.TextStim(win=win, name='textWord',
        text='',
        font='Open Sans',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "visualStimuliImage" ---
    imagePresentation = visual.ImageStim(
        win=win,
        name='imagePresentation', 
        image='default.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=None,
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    textImage = visual.TextStim(win=win, name='textImage',
        text='Please continue by pressing Space or wait for 8 seconds.',
        font='Open Sans',
        pos=(0, -0.4), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    keyRespImage = keyboard.Keyboard(deviceName='keyRespImage')
    
    # --- Initialize components for Routine "movieStimuli" ---
    moviePresentation = visual.MovieStim(
        win, name='moviePresentation',
        filename=None, movieLib='ffpyplayer',
        loop=False, volume=5.0, noAudio=True,
        pos=None, size=(-0.6667,-0.5), units=win.units,
        ori=180.0, anchor='center',opacity=None, contrast=1.0,
        depth=0
    )
    
    # --- Initialize components for Routine "sliderResponse" ---
    textSlider = visual.TextStim(win=win, name='textSlider',
        text='Did you like the example experiment?',
        font='Open Sans',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    sliderResp = visual.Slider(win=win, name='sliderResp',
        startValue=3, size=(1.0, 0.1), pos=(0, -0.2), units=win.units,
        labels=['not at all', 'very much'], ticks=(1, 2, 3, 4, 5), granularity=1.0,
        style='rating', styleTweaks=(), opacity=None,
        labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
        font='Open Sans', labelHeight=0.05,
        flip=False, ori=0.0, depth=-1, readOnly=False)
    
    # --- Initialize components for Routine "goodbyeScreen" ---
    textGoodbye = visual.TextStim(win=win, name='textGoodbye',
        text='Never forget...\n\nYou look great\n\nYou are enough\n\nNice butt',
        font='Open Sans',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # create some handy timers
    
    # global clock to track the time since experiment started
    if globalClock is None:
        # create a clock if not given one
        globalClock = core.Clock()
    if isinstance(globalClock, str):
        # if given a string, make a clock accoridng to it
        if globalClock == 'float':
            # get timestamps as a simple value
            globalClock = core.Clock(format='float')
        elif globalClock == 'iso':
            # get timestamps in ISO format
            globalClock = core.Clock(format='%Y-%m-%d_%H:%M:%S.%f%z')
        else:
            # get timestamps in a custom format
            globalClock = core.Clock(format=globalClock)
    if ioServer is not None:
        ioServer.syncClock(globalClock)
    logging.setDefaultClock(globalClock)
    # routine timer to track time remaining of each (possibly non-slip) routine
    routineTimer = core.Clock()
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo['expStart'] = data.getDateStr(
        format='%Y-%m-%d %Hh%M.%S.%f %z', fractionalSecondDigits=6
    )
    
    # set up handler to look after randomisation of conditions etc
    loop = data.TrialHandler2(
        name='loop',
        nReps=1.0, 
        method='sequential', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=data.importConditions('materials/stimulusfile.csv'), 
        seed=None, 
    )
    thisExp.addLoop(loop)  # add the loop to the experiment
    thisLoop = loop.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisLoop.rgb)
    if thisLoop != None:
        for paramName in thisLoop:
            globals()[paramName] = thisLoop[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisLoop in loop:
        currentLoop = loop
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisLoop.rgb)
        if thisLoop != None:
            for paramName in thisLoop:
                globals()[paramName] = thisLoop[paramName]
        
        # --- Prepare to start Routine "visualStimuliText" ---
        # create an object to store info about Routine visualStimuliText
        visualStimuliText = data.Routine(
            name='visualStimuliText',
            components=[textWord],
        )
        visualStimuliText.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        textWord.setText(WordStimuli)
        # store start times for visualStimuliText
        visualStimuliText.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        visualStimuliText.tStart = globalClock.getTime(format='float')
        visualStimuliText.status = STARTED
        thisExp.addData('visualStimuliText.started', visualStimuliText.tStart)
        visualStimuliText.maxDuration = None
        # keep track of which components have finished
        visualStimuliTextComponents = visualStimuliText.components
        for thisComponent in visualStimuliText.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "visualStimuliText" ---
        # if trial has changed, end Routine now
        if isinstance(loop, data.TrialHandler2) and thisLoop.thisN != loop.thisTrial.thisN:
            continueRoutine = False
        visualStimuliText.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 1.0:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *textWord* updates
            
            # if textWord is starting this frame...
            if textWord.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                textWord.frameNStart = frameN  # exact frame index
                textWord.tStart = t  # local t and not account for scr refresh
                textWord.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(textWord, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'textWord.started')
                # update status
                textWord.status = STARTED
                textWord.setAutoDraw(True)
            
            # if textWord is active this frame...
            if textWord.status == STARTED:
                # update params
                pass
            
            # if textWord is stopping this frame...
            if textWord.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > textWord.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    textWord.tStop = t  # not accounting for scr refresh
                    textWord.tStopRefresh = tThisFlipGlobal  # on global time
                    textWord.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'textWord.stopped')
                    # update status
                    textWord.status = FINISHED
                    textWord.setAutoDraw(False)
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                visualStimuliText.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in visualStimuliText.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "visualStimuliText" ---
        for thisComponent in visualStimuliText.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for visualStimuliText
        visualStimuliText.tStop = globalClock.getTime(format='float')
        visualStimuliText.tStopRefresh = tThisFlipGlobal
        thisExp.addData('visualStimuliText.stopped', visualStimuliText.tStop)
        try:
            if textWord.tStopRefresh is not None:
                duration_val = textWord.tStopRefresh - textWord.tStartRefresh
            else:
                duration_val = thisExp.thisEntry['visualStimuliText.stopped'] - textWord.tStartRefresh
            bids_event = BIDSTaskEvent(
                onset=textWord.tStartRefresh,
                duration=duration_val,
                event_type=type(textWord).__name__,
                trial_type=WordStimuli,
            )
            if bids_handler:
                bids_handler.addEvent(bids_event)
            else:
                loop.addData('bidseventTextWord.event', bids_event)
        except BIDSError as e:
            print(f"An error occurred when creating BIDS event: {e}")
        logging.log(level=24, msg={k: v for k, v in bids_event.items() if v is not None})
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if visualStimuliText.maxDurationReached:
            routineTimer.addTime(-visualStimuliText.maxDuration)
        elif visualStimuliText.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-1.000000)
        
        # --- Prepare to start Routine "visualStimuliImage" ---
        # create an object to store info about Routine visualStimuliImage
        visualStimuliImage = data.Routine(
            name='visualStimuliImage',
            components=[imagePresentation, textImage, keyRespImage],
        )
        visualStimuliImage.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        imagePresentation.setImage(ImageStimuli)
        # create starting attributes for keyRespImage
        keyRespImage.keys = []
        keyRespImage.rt = []
        _keyRespImage_allKeys = []
        # store start times for visualStimuliImage
        visualStimuliImage.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        visualStimuliImage.tStart = globalClock.getTime(format='float')
        visualStimuliImage.status = STARTED
        thisExp.addData('visualStimuliImage.started', visualStimuliImage.tStart)
        visualStimuliImage.maxDuration = None
        # keep track of which components have finished
        visualStimuliImageComponents = visualStimuliImage.components
        for thisComponent in visualStimuliImage.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "visualStimuliImage" ---
        # if trial has changed, end Routine now
        if isinstance(loop, data.TrialHandler2) and thisLoop.thisN != loop.thisTrial.thisN:
            continueRoutine = False
        visualStimuliImage.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 3.0:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *imagePresentation* updates
            
            # if imagePresentation is starting this frame...
            if imagePresentation.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                imagePresentation.frameNStart = frameN  # exact frame index
                imagePresentation.tStart = t  # local t and not account for scr refresh
                imagePresentation.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(imagePresentation, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'imagePresentation.started')
                # update status
                imagePresentation.status = STARTED
                imagePresentation.setAutoDraw(True)
            
            # if imagePresentation is active this frame...
            if imagePresentation.status == STARTED:
                # update params
                pass
            
            # if imagePresentation is stopping this frame...
            if imagePresentation.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > imagePresentation.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    imagePresentation.tStop = t  # not accounting for scr refresh
                    imagePresentation.tStopRefresh = tThisFlipGlobal  # on global time
                    imagePresentation.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'imagePresentation.stopped')
                    # update status
                    imagePresentation.status = FINISHED
                    imagePresentation.setAutoDraw(False)
            
            # *textImage* updates
            
            # if textImage is starting this frame...
            if textImage.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                textImage.frameNStart = frameN  # exact frame index
                textImage.tStart = t  # local t and not account for scr refresh
                textImage.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(textImage, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'textImage.started')
                # update status
                textImage.status = STARTED
                textImage.setAutoDraw(True)
            
            # if textImage is active this frame...
            if textImage.status == STARTED:
                # update params
                pass
            
            # if textImage is stopping this frame...
            if textImage.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > textImage.tStartRefresh + 3-frameTolerance:
                    # keep track of stop time/frame for later
                    textImage.tStop = t  # not accounting for scr refresh
                    textImage.tStopRefresh = tThisFlipGlobal  # on global time
                    textImage.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'textImage.stopped')
                    # update status
                    textImage.status = FINISHED
                    textImage.setAutoDraw(False)
            
            # *keyRespImage* updates
            waitOnFlip = False
            
            # if keyRespImage is starting this frame...
            if keyRespImage.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                keyRespImage.frameNStart = frameN  # exact frame index
                keyRespImage.tStart = t  # local t and not account for scr refresh
                keyRespImage.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(keyRespImage, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'keyRespImage.started')
                # update status
                keyRespImage.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(keyRespImage.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(keyRespImage.clearEvents, eventType='keyboard')  # clear events on next screen flip
            
            # if keyRespImage is stopping this frame...
            if keyRespImage.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > keyRespImage.tStartRefresh + 3-frameTolerance:
                    # keep track of stop time/frame for later
                    keyRespImage.tStop = t  # not accounting for scr refresh
                    keyRespImage.tStopRefresh = tThisFlipGlobal  # on global time
                    keyRespImage.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'keyRespImage.stopped')
                    # update status
                    keyRespImage.status = FINISHED
                    keyRespImage.status = FINISHED
            if keyRespImage.status == STARTED and not waitOnFlip:
                theseKeys = keyRespImage.getKeys(keyList=['space'], ignoreKeys=None, waitRelease=False)
                _keyRespImage_allKeys.extend(theseKeys)
                if len(_keyRespImage_allKeys):
                    keyRespImage.keys = _keyRespImage_allKeys[-1].name  # just the last key pressed
                    keyRespImage.rt = _keyRespImage_allKeys[-1].rt
                    keyRespImage.duration = _keyRespImage_allKeys[-1].duration
                    # a response ends the routine
                    continueRoutine = False
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                visualStimuliImage.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in visualStimuliImage.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "visualStimuliImage" ---
        for thisComponent in visualStimuliImage.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for visualStimuliImage
        visualStimuliImage.tStop = globalClock.getTime(format='float')
        visualStimuliImage.tStopRefresh = tThisFlipGlobal
        thisExp.addData('visualStimuliImage.stopped', visualStimuliImage.tStop)
        # check responses
        if keyRespImage.keys in ['', [], None]:  # No response was made
            keyRespImage.keys = None
        loop.addData('keyRespImage.keys',keyRespImage.keys)
        if keyRespImage.keys != None:  # we had a response
            loop.addData('keyRespImage.rt', keyRespImage.rt)
            loop.addData('keyRespImage.duration', keyRespImage.duration)
        try:
            if imagePresentation.tStopRefresh is not None:
                duration_val = imagePresentation.tStopRefresh - imagePresentation.tStartRefresh
            else:
                duration_val = thisExp.thisEntry['visualStimuliImage.stopped'] - imagePresentation.tStartRefresh
            bids_event = BIDSTaskEvent(
                onset=imagePresentation.tStartRefresh,
                duration=duration_val,
                event_type=type(imagePresentation).__name__,
                trial_type=WordStimuli,
                stim_file=ImageStimuli,
            )
            if bids_handler:
                bids_handler.addEvent(bids_event)
            else:
                loop.addData('bidseventImagePresentation.event', bids_event)
        except BIDSError as e:
            print(f"An error occurred when creating BIDS event: {e}")
        try:
            if textImage.tStopRefresh is not None:
                duration_val = textImage.tStopRefresh - textImage.tStartRefresh
            else:
                duration_val = thisExp.thisEntry['visualStimuliImage.stopped'] - textImage.tStartRefresh
            bids_event = BIDSTaskEvent(
                onset=textImage.tStartRefresh,
                duration=700.0,
                trial_type=WordStimuli,
            )
            if bids_handler:
                bids_handler.addEvent(bids_event)
            else:
                loop.addData('bidseventTextImage.event', bids_event)
        except BIDSError as e:
            print(f"An error occurred when creating BIDS event: {e}")
        try:
            if keyRespImage.tStopRefresh is not None:
                duration_val = keyRespImage.tStopRefresh - keyRespImage.tStartRefresh
            else:
                duration_val = thisExp.thisEntry['visualStimuliImage.stopped'] - keyRespImage.tStartRefresh
            bids_event = BIDSTaskEvent(
                onset=keyRespImage.tStartRefresh,
                duration=duration_val,
                trial_type=WordStimuli,
            )
            if bids_handler:
                bids_handler.addEvent(bids_event)
            else:
                loop.addData('bidsEventKeyRespImage.event', bids_event)
        except BIDSError as e:
            print(f"An error occurred when creating BIDS event: {e}")
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if visualStimuliImage.maxDurationReached:
            routineTimer.addTime(-visualStimuliImage.maxDuration)
        elif visualStimuliImage.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-3.000000)
        
        # --- Prepare to start Routine "movieStimuli" ---
        # create an object to store info about Routine movieStimuli
        movieStimuli = data.Routine(
            name='movieStimuli',
            components=[moviePresentation],
        )
        movieStimuli.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        moviePresentation.setMovie(MovieStimuli)
        # store start times for movieStimuli
        movieStimuli.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        movieStimuli.tStart = globalClock.getTime(format='float')
        movieStimuli.status = STARTED
        thisExp.addData('movieStimuli.started', movieStimuli.tStart)
        movieStimuli.maxDuration = None
        # keep track of which components have finished
        movieStimuliComponents = movieStimuli.components
        for thisComponent in movieStimuli.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "movieStimuli" ---
        # if trial has changed, end Routine now
        if isinstance(loop, data.TrialHandler2) and thisLoop.thisN != loop.thisTrial.thisN:
            continueRoutine = False
        movieStimuli.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 1.0:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *moviePresentation* updates
            
            # if moviePresentation is starting this frame...
            if moviePresentation.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                moviePresentation.frameNStart = frameN  # exact frame index
                moviePresentation.tStart = t  # local t and not account for scr refresh
                moviePresentation.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(moviePresentation, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'moviePresentation.started')
                # update status
                moviePresentation.status = STARTED
                moviePresentation.setAutoDraw(True)
                moviePresentation.play()
            
            # if moviePresentation is stopping this frame...
            if moviePresentation.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > moviePresentation.tStartRefresh + 1-frameTolerance or moviePresentation.isFinished:
                    # keep track of stop time/frame for later
                    moviePresentation.tStop = t  # not accounting for scr refresh
                    moviePresentation.tStopRefresh = tThisFlipGlobal  # on global time
                    moviePresentation.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'moviePresentation.stopped')
                    # update status
                    moviePresentation.status = FINISHED
                    moviePresentation.setAutoDraw(False)
                    moviePresentation.stop()
            if moviePresentation.isFinished:  # force-end the Routine
                continueRoutine = False
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[moviePresentation]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                movieStimuli.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in movieStimuli.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "movieStimuli" ---
        for thisComponent in movieStimuli.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for movieStimuli
        movieStimuli.tStop = globalClock.getTime(format='float')
        movieStimuli.tStopRefresh = tThisFlipGlobal
        thisExp.addData('movieStimuli.stopped', movieStimuli.tStop)
        moviePresentation.stop()  # ensure movie has stopped at end of Routine
        try:
            bids_event = BIDSTaskEvent(
                onset=moviePresentation.tStartRefresh,
                duration=1.0,
                event_type=type(moviePresentation).__name__,
                trial_type=WordStimuli,
                stim_file=MovieStimuli,
            )
            if bids_handler:
                bids_handler.addEvent(bids_event)
            else:
                loop.addData('bidseventMoviePresentation.event', bids_event)
        except BIDSError as e:
            print(f"An error occurred when creating BIDS event: {e}")
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if movieStimuli.maxDurationReached:
            routineTimer.addTime(-movieStimuli.maxDuration)
        elif movieStimuli.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-1.000000)
        thisExp.nextEntry()
        
    # completed 1.0 repeats of 'loop'
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "sliderResponse" ---
    # create an object to store info about Routine sliderResponse
    sliderResponse = data.Routine(
        name='sliderResponse',
        components=[textSlider, sliderResp],
    )
    sliderResponse.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    sliderResp.reset()
    # store start times for sliderResponse
    sliderResponse.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    sliderResponse.tStart = globalClock.getTime(format='float')
    sliderResponse.status = STARTED
    thisExp.addData('sliderResponse.started', sliderResponse.tStart)
    sliderResponse.maxDuration = None
    # keep track of which components have finished
    sliderResponseComponents = sliderResponse.components
    for thisComponent in sliderResponse.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "sliderResponse" ---
    sliderResponse.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 2.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *textSlider* updates
        
        # if textSlider is starting this frame...
        if textSlider.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            textSlider.frameNStart = frameN  # exact frame index
            textSlider.tStart = t  # local t and not account for scr refresh
            textSlider.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(textSlider, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'textSlider.started')
            # update status
            textSlider.status = STARTED
            textSlider.setAutoDraw(True)
        
        # if textSlider is active this frame...
        if textSlider.status == STARTED:
            # update params
            pass
        
        # if textSlider is stopping this frame...
        if textSlider.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > textSlider.tStartRefresh + 1-frameTolerance:
                # keep track of stop time/frame for later
                textSlider.tStop = t  # not accounting for scr refresh
                textSlider.tStopRefresh = tThisFlipGlobal  # on global time
                textSlider.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'textSlider.stopped')
                # update status
                textSlider.status = FINISHED
                textSlider.setAutoDraw(False)
        
        # *sliderResp* updates
        
        # if sliderResp is starting this frame...
        if sliderResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            sliderResp.frameNStart = frameN  # exact frame index
            sliderResp.tStart = t  # local t and not account for scr refresh
            sliderResp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(sliderResp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'sliderResp.started')
            # update status
            sliderResp.status = STARTED
            sliderResp.setAutoDraw(True)
        
        # if sliderResp is active this frame...
        if sliderResp.status == STARTED:
            # update params
            pass
        
        # if sliderResp is stopping this frame...
        if sliderResp.status == STARTED:
            # is it time to stop? (based on local clock)
            if tThisFlip > 2-frameTolerance:
                # keep track of stop time/frame for later
                sliderResp.tStop = t  # not accounting for scr refresh
                sliderResp.tStopRefresh = tThisFlipGlobal  # on global time
                sliderResp.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'sliderResp.stopped')
                # update status
                sliderResp.status = FINISHED
                sliderResp.setAutoDraw(False)
        
        # Check sliderResp for response to end Routine
        if sliderResp.getRating() is not None and sliderResp.status == STARTED:
            continueRoutine = False
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            sliderResponse.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in sliderResponse.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "sliderResponse" ---
    for thisComponent in sliderResponse.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for sliderResponse
    sliderResponse.tStop = globalClock.getTime(format='float')
    sliderResponse.tStopRefresh = tThisFlipGlobal
    thisExp.addData('sliderResponse.stopped', sliderResponse.tStop)
    thisExp.addData('sliderResp.response', sliderResp.getRating())
    thisExp.addData('sliderResp.rt', sliderResp.getRT())
    # Run 'End Routine' code from codeSliderResp
    try:
        responseOnset = sliderResp.tStartRefresh + sliderResp.rt
    except TypeError:
        responseOnset = None
    try:
        if textSlider.tStopRefresh is not None:
            duration_val = textSlider.tStopRefresh - textSlider.tStartRefresh
        else:
            duration_val = thisExp.thisEntry['sliderResponse.stopped'] - textSlider.tStartRefresh
        bids_event = BIDSTaskEvent(
            onset=textSlider.tStartRefresh,
            duration=duration_val,
            event_type=type(textSlider).__name__,
            trial_type=WordStimuli,
        )
        bids_event.update({"text_presented":"Did you like the example experiment?"})
        if bids_handler:
            bids_handler.addEvent(bids_event)
        else:
            thisExp.addData('bidseventTextSlider.event', bids_event)
    except BIDSError as e:
        print(f"An error occurred when creating BIDS event: {e}")
    logging.log(level=24, msg={k: v for k, v in bids_event.items() if v is not None})
    try:
        if sliderResp.tStopRefresh is not None:
            duration_val = sliderResp.tStopRefresh - sliderResp.tStartRefresh
        else:
            duration_val = thisExp.thisEntry['sliderResponse.stopped'] - sliderResp.tStartRefresh
        if hasattr(sliderResp, 'rt'):
            rt_val = sliderResp.rt
        else:
            rt_val = None
            logging.warning('The linked component "sliderResp" does not have a reaction time(.rt) attribute. Unable to link BIDS response_time to this component. Please verify the component settings.')
        bids_event = BIDSTaskEvent(
            onset=sliderResp.tStartRefresh,
            duration=duration_val,
            response_time=rt_val,
            event_type=type(sliderResp).__name__,
        )
        bids_event.update({"responded_discrete_value": sliderResp.markerPos})
        if bids_handler:
            bids_handler.addEvent(bids_event)
        else:
            thisExp.addData('bidseventSliderResp.event', bids_event)
    except BIDSError as e:
        print(f"An error occurred when creating BIDS event: {e}")
    logging.log(level=24, msg={k: v for k, v in bids_event.items() if v is not None})
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if sliderResponse.maxDurationReached:
        routineTimer.addTime(-sliderResponse.maxDuration)
    elif sliderResponse.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-2.000000)
    thisExp.nextEntry()
    
    # --- Prepare to start Routine "goodbyeScreen" ---
    # create an object to store info about Routine goodbyeScreen
    goodbyeScreen = data.Routine(
        name='goodbyeScreen',
        components=[textGoodbye],
    )
    goodbyeScreen.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # store start times for goodbyeScreen
    goodbyeScreen.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    goodbyeScreen.tStart = globalClock.getTime(format='float')
    goodbyeScreen.status = STARTED
    thisExp.addData('goodbyeScreen.started', goodbyeScreen.tStart)
    goodbyeScreen.maxDuration = None
    # keep track of which components have finished
    goodbyeScreenComponents = goodbyeScreen.components
    for thisComponent in goodbyeScreen.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "goodbyeScreen" ---
    goodbyeScreen.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 1.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *textGoodbye* updates
        
        # if textGoodbye is starting this frame...
        if textGoodbye.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            textGoodbye.frameNStart = frameN  # exact frame index
            textGoodbye.tStart = t  # local t and not account for scr refresh
            textGoodbye.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(textGoodbye, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'textGoodbye.started')
            # update status
            textGoodbye.status = STARTED
            textGoodbye.setAutoDraw(True)
        
        # if textGoodbye is active this frame...
        if textGoodbye.status == STARTED:
            # update params
            pass
        
        # if textGoodbye is stopping this frame...
        if textGoodbye.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > textGoodbye.tStartRefresh + 1-frameTolerance:
                # keep track of stop time/frame for later
                textGoodbye.tStop = t  # not accounting for scr refresh
                textGoodbye.tStopRefresh = tThisFlipGlobal  # on global time
                textGoodbye.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'textGoodbye.stopped')
                # update status
                textGoodbye.status = FINISHED
                textGoodbye.setAutoDraw(False)
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            goodbyeScreen.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in goodbyeScreen.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "goodbyeScreen" ---
    for thisComponent in goodbyeScreen.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for goodbyeScreen
    goodbyeScreen.tStop = globalClock.getTime(format='float')
    goodbyeScreen.tStopRefresh = tThisFlipGlobal
    thisExp.addData('goodbyeScreen.stopped', goodbyeScreen.tStop)
    try:
        if textGoodbye.tStopRefresh is not None:
            duration_val = textGoodbye.tStopRefresh - textGoodbye.tStartRefresh
        else:
            duration_val = thisExp.thisEntry['goodbyeScreen.stopped'] - textGoodbye.tStartRefresh
        bids_event = BIDSTaskEvent(
            onset=100.0,
            duration=101.0,
            response_time=102.0,
            event_type=type(textGoodbye).__name__,
            trial_type='overwrite test',
        )
        bids_event.update({"text_presented":"Goodybe"})
        if bids_handler:
            bids_handler.addEvent(bids_event)
        else:
            thisExp.addData('bidseventTextGoodbye.event', bids_event)
    except BIDSError as e:
        print(f"An error occurred when creating BIDS event: {e}")
    logging.log(level=24, msg={k: v for k, v in bids_event.items() if v is not None})
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if goodbyeScreen.maxDurationReached:
        routineTimer.addTime(-goodbyeScreen.maxDuration)
    elif goodbyeScreen.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-1.000000)
    thisExp.nextEntry()
    thisExp.nextEntry()
    # the Routine "bidsExport" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    ignore_list = [
        'participant',
        'session',
        'date',
        'expName',
        'psychopyVersion',
        'OS',
        'frameRate'
    ]
    participant_info = {
        key: thisExp.extraInfo[key]
        for key in thisExp.extraInfo
        if key not in ignore_list
    }
    # write tsv file and update
    try:
        if bids_handler.events:
            bids_handler.writeEvents(participant_info, add_stimuli=True, execute_sidecar=True, generate_hed_metadata=False)
    except Exception as e:
        print(f"An error occurred when writing BIDS events: {e}")
    
    # mark experiment as finished
    endExperiment(thisExp, win=win)


def saveData(thisExp):
    """
    Save data from this experiment
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    filename = thisExp.dataFileName
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename + '.csv', delim='auto')
    thisExp.saveAsPickle(filename)


def endExperiment(thisExp, win=None):
    """
    End this experiment, performing final shut down operations.
    
    This function does NOT close the window or end the Python process - use `quit` for this.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    """
    if win is not None:
        # remove autodraw from all current components
        win.clearAutoDraw()
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed
        win.flip()
    # return console logger level to WARNING
    logging.console.setLevel(logging.WARNING)
    # mark experiment handler as finished
    thisExp.status = FINISHED
    logging.flush()


def quit(thisExp, win=None, thisSession=None):
    """
    Fully quit, closing the window and ending the Python process.
    
    Parameters
    ==========
    win : psychopy.visual.Window
        Window to close.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    thisExp.abort()  # or data files will save again on exit
    # make sure everything is closed down
    if win is not None:
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()
        win.close()
    logging.flush()
    if thisSession is not None:
        thisSession.stop()
    # terminate Python process
    core.quit()


# if running this experiment as a script...
if __name__ == '__main__':
    # call all functions in order
    thisExp = setupData(expInfo=expInfo)
    logFile = setupLogging(filename=thisExp.dataFileName)
    win = setupWindow(expInfo=expInfo)
    setupDevices(expInfo=expInfo, thisExp=thisExp, win=win)
    run(
        expInfo=expInfo, 
        thisExp=thisExp, 
        win=win,
        globalClock='float'
    )
    saveData(thisExp=thisExp)
    quit(thisExp=thisExp, win=win)
