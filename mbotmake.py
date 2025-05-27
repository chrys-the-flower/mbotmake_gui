#!/usr/bin/env python3

import argparse
import zipfile
import json
import sys
import tempfile
import copy
import math
import re
import traceback
import base64
from os import getenv
from enum import Enum

from uuid import uuid4

DEBUG = False

METAJSON = '''
{
    "bot_type": null,
    "bounding_box": null,
    "chamber_temperature": null,
    "commanded_duration_s": null,
    "duration_s": null,
    "extruder_temperature": null,
    "extruder_temperatures": [null],
    "extrusion_distance_mm": null,
    "extrusion_distances_mm": [null],
    "extrusion_mass_g": null,
    "extrusion_masses_g": [null],
    "material": "pla",
    "materials": ["pla"],
    "num_z_layers": null,
    "num_z_transitions": null,
    "platform_temperature": null,
    "thing_id": null,
    "tool_type": null,
    "tool_types": [null],
    "total_commands": null,
    "miracle_config": {
        "_bot": null,
        "_extruders": [null],
        "_materials": [
            "pla"
        ],
        "doRaft": true,
        "gaggles": {
            "default": {
                "adjacentFillLeakyConnections": true,
                "adjacentFillLeakyDistanceRatio": 1.4,
                "backlashEpsilon": 0.05,
                "backlashFeedback": 0.9,
                "backlashX": 0.0,
                "backlashY": 0.09,
                "baseInsetDistanceMultiplier": 1.0,
                "baseLayerHeight": 0.2,
                "baseLayerWidth": 0.5,
                "baseNumberOfShells": 1,
                "bedZOffset": 0,
                "bridgeAnchorMinimumLength": 0.8,
                "bridgeAnchorWidth": 0.8,
                "bridgeMaximumLength": 80.0,
                "brimsBaseWidth": 2.5,
                "brimsModelOffset": 0.0,
                "brimsOverlapWidth": 1.5,
                "coarseness": 0.0001,
                "computeVolumeLike2_1_0": false,
                "defaultExtruder": 0,
                "defaultSupportMaterial": 0,
                "description": "",
                "doBacklashCompensation": false,
                "doBreakawaySupport": true,
                "doBridging": true,
                "doBrims": false,
                "doExponentialDeceleration": true,
                "doExternalSpurs": true,
                "doFanCommand": true,
                "doFanModulation": true,
                "doFixedLayerStart": false,
                "doFixedShellStart": true,
                "doInternalSpurs": false,
                "doMinfill": false,
                "doMixedRaft": false,
                "doMixedSupport": false,
                "doNewPathPlanning": true,
                "doPaddedBase": false,
                "doRaft": true,
                "doRateLimit": true,
                "doSplitLongMoves": false,
                "doSupport": true,
                "doSupportUnderBridges": false,
                "exponentialDecelerationMinSpeed": 0.0,
                "exponentialDecelerationRatio": 0.375,
                "exponentialDecelerationSegmentCount": 10,
                "extruderProfiles": [
                    {
                        "defaultTemperature": 215,
                        "extrusionProfiles": {
                            "bridges": {
                                "fanSpeed": 0.95,
                                "feedrate": 40.0
                            },
                            "brims": {
                                "fanSpeed": 0.5,
                                "feedrate": 10.0
                            },
                            "firstModelLayer": {
                                "fanSpeed": 1.0,
                                "feedrate": 30.0
                            },
                            "floorSurfaceFills": {
                                "fanSpeed": 0.5,
                                "feedrate": 90
                            },
                            "infill": {
                                "fanSpeed": 0.5,
                                "feedrate": 90
                            },
                            "insets": {
                                "fanSpeed": 0.95,
                                "feedrate": 90
                            },
                            "outlines": {
                                "fanSpeed": 0.95,
                                "feedrate": 40
                            },
                            "purge": {
                                "fanSpeed": 0.5,
                                "feedrate": 100
                            },
                            "raft": {
                                "fanSpeed": 0.95,
                                "feedrate": 90.0
                            },
                            "raftBase": {
                                "fanSpeed": 0.5,
                                "feedrate": 10.0
                            },
                            "roofSurfaceFills": {
                                "fanSpeed": 0.5,
                                "feedrate": 90
                            },
                            "sparseRoofSurfaceFills": {
                                "fanSpeed": 0.5,
                                "feedrate": 90
                            },
                            "spurs": {
                                "fanSpeed": 0.5,
                                "feedrate": 40
                            }
                        },
                        "extrusionVolumeMultiplier": 1.0,
                        "feedDiameter": 1.77,
                        "idleTemperature": 190,
                        "nozzleDiameter": 0.4,
                        "oozeFeedstockDistance": 0.1,
                        "preOozeFeedstockDistance": 0.1,
                        "restartExtraDistance": 0.1,
                        "restartRate": 30,
                        "retractDistance": 0.5,
                        "retractRate": 50,
                        "toolchangeRestartDistance": 18.5,
                        "toolchangeRestartRate": 6.0,
                        "toolchangeRetractDistance": 19.0,
                        "toolchangeRetractRate": 6.0
                    }
                ],
                "fanDefaultSpeed": 0.95,
                "fanLayer": 1,
                "fanModulationThreshold": 0.5,
                "fanModulationWindow": 0.1,
                "fixedLayerStartX": 0,
                "fixedLayerStartY": 0,
                "fixedShellStartDirection": 215,
                "floorSolidThickness": 0,
                "floorSurfaceThickness": 0.8,
                "floorThickness": 0.8,
                "horizontalInset": 0,
                "infillDensity": 0.4,
                "infillShellSpacingMultiplier": 0.55,
                "insetDistanceMultiplier": 1.0,
                "layerHeight": 0.2,
                "leakyConnectionsAdjacentDistance": 0.8,
                "maxConnectionLength": 10.0,
                "maxSparseFillThickness": 0.2,
                "maxSpurWidth": 0.5,
                "minLayerDuration": 5.0,
                "minLayerHeight": 0.01,
                "minRaftBaseGap": 10.0,
                "minSpeedMultiplier": 0.3,
                "minSpurLength": 0.34,
                "minSpurWidth": 0.12,
                "minThickInfillImprovement": 1.0,
                "minimumMoveDistance": 0.01,
                "modelFillProfiles": {
                    "bridge": {
                        "density": 1.0,
                        "orientationInterval": 0,
                        "orientationOffset": 0,
                        "orientationRange": 360,
                        "pattern": "bridge_fill"
                    },
                    "floor_surface": {
                        "density": 1.0,
                        "orientationInterval": 90,
                        "orientationRange": 90,
                        "pattern": "linear"
                    },
                    "roof_surface": {
                        "density": 1.0,
                        "orientationInterval": 90,
                        "orientationRange": 360,
                        "pattern": "linear"
                    },
                    "solid": {
                        "density": 1.0,
                        "orientationInterval": 90,
                        "orientationRange": 90,
                        "pattern": "linear"
                    },
                    "sparse": {
                        "density": 0.4,
                        "orientationInterval": 90,
                        "orientationOffset": 0,
                        "orientationRange": 90,
                        "pattern": "linear"
                    },
                    "sparse_roof_surface": {
                        "density": 0.4,
                        "orientationInterval": 90,
                        "orientationOffset": 0,
                        "orientationRange": 90,
                        "pattern": "linear"
                    }
                },
                "numberOfBrims": 5,
                "numberOfExtentShells": 2,
                "numberOfInternalBrims": 5,
                "numberOfShells": 2,
                "numberOfSparseShells": 0,
                "numberOfSupportShells": 0,
                "paddedBaseOutlineOffset": -0.5,
                "pauseHeights": [],
                "purgeBaseRotation": 45,
                "purgeBucketSide": 4.0,
                "purgeWallBaseFilamentWidth": 2.0,
                "purgeWallBasePatternLength": 10.0,
                "purgeWallBasePatternWidth": 8.0,
                "purgeWallModelOffset": 2.0,
                "purgeWallPatternWidth": 2.0,
                "purgeWallSpacing": 1.0,
                "purgeWallWidth": 0.5,
                "purgeWallXLength": 30,
                "raftBaseInfillShellSpacingMultiplier": 0.1,
                "raftBaseInsetDistanceMultiplier": 0.4,
                "raftBaseLayers": 1,
                "raftBaseOutset": 4,
                "raftBaseShells": 3,
                "raftBaseThickness": 0.3,
                "raftBaseWidth": 2.5,
                "raftBrimsSpacing": 1.0,
                "raftExtraOffset": 0.0,
                "raftFillProfiles": {
                    "base": {
                        "density": 0.2,
                        "linearFillGroupDensity": 2.2,
                        "linearFillGroupSize": 3,
                        "orientationInterval": 0,
                        "orientationOffset": 0,
                        "orientationRange": 180,
                        "pattern": "linear"
                    },
                    "interface": {
                        "density": 0.5,
                        "orientationInterval": 90,
                        "orientationOffset": 45,
                        "orientationRange": 360,
                        "pattern": "linear"
                    },
                    "surface": {
                        "density": 0.85,
                        "orientationInterval": 90,
                        "orientationOffset": 0,
                        "orientationRange": 90,
                        "pattern": "local_no_warp"
                    }
                },
                "raftInterfaceLayers": 2,
                "raftInterfaceShells": 0,
                "raftInterfaceThickness": 0.27,
                "raftInterfaceWidth": 0.4,
                "raftInterfaceZOffset": -0.14,
                "raftModelShellsSpacing": 0.26,
                "raftModelSpacing": 0.33,
                "raftSupportSpacing": 0.1,
                "raftSurfaceInsetDistanceMultiplier": 0.8,
                "raftSurfaceLayers": 2,
                "raftSurfaceOutset": 4,
                "raftSurfaceShellSpacingMultiplier": 0.7,
                "raftSurfaceShells": 2,
                "raftSurfaceThickness": 0.27,
                "raftSurfaceZOffset": -0.03,
                "rateLimitBufferSize": 100,
                "rateLimitMinSpeed": 10,
                "rateLimitSpeedRatio": 0.3,
                "rateLimitSplitBias": 0,
                "rateLimitSplitMoveDistance": 0.75,
                "rateLimitSplitRecursionDepth": 8,
                "rateLimitTransmissionRate": 150,
                "roofAnchorMargin": 0.4,
                "roofSolidThickness": 0,
                "roofSurfaceThickness": 0.8,
                "roofThickness": 0.8,
                "shellsLeakyConnections": true,
                "splitMinimumDistance": 0.4,
                "startPosition": {
                    "x": null,
                    "y": null,
                    "z": null
                },
                "supportAngle": 15,
                "supportBreakawayModelOffset": -0.15,
                "supportBreakawayModelRoofSpacing": 0.16,
                "supportCutout": 0.1,
                "supportCutoutExtraDistance": 0.6,
                "supportExtraDistance": 0.5,
                "supportFillProfiles": {
                    "solid": {
                        "density": 0.32,
                        "orientationInterval": 0,
                        "orientationOffset": 45,
                        "orientationRange": 360,
                        "pattern": "hilbert_fill"
                    },
                    "sparse": {
                        "consistentOrder": true,
                        "density": 0.16,
                        "orientationInterval": 0,
                        "orientationOffset": 45,
                        "orientationRange": 0,
                        "pattern": "linear"
                    }
                },
                "supportInsetDistanceMultiplier": 1.0,
                "supportInteriorExtruder": 0,
                "supportLayerHeight": 0.2,
                "supportLeakyConnections": true,
                "supportModelSpacing": 0.4,
                "supportRoofModelSpacing": 0.4,
                "supportRoofSolidThickness": 3.0,
                "supportShellSpacingMultiplier": 0.55,
                "thickLayerThreshold": 0,
                "thickLayerVolumeMultiplier": 1,
                "travelSpeedXY": 150,
                "travelSpeedZ": 23,
                "useRelativeExtruderPositions": false
            }
        },
        "version": "5.6.0"
    },
    "preferences": {
        "default": {
            "overrides": {
                "defaultSupportMaterial": 0,
                "doSupport": true,
                "doSupportUnderBridges": false,
                "modelFillProfiles.sparse.density": 0.4,
                "supportAngle": 15,
                "supportFillProfiles.sparse.density": 0.16,
                "supportModelSpacing": 0.4,
                "undefined": 0
            },
            "print_mode": "balanced"
        }
    },
    "uuid": "87fe421b-427a-4657-be72-28b7a6beee72",
    "version": "1.2.0"
}
'''


class MachineType(Enum):
    REPLICATOR5 = 1
    REPLICATORPlUS = 2
    REPLICATORMINI = 3
    REPLICATORMINIPLUS = 4


class ExtruderType(Enum):
    SMARTEXTRUDER = 1
    SMARTEXTRUDERPLUS = 2
    TOUGHEXTRUDER = 3
    EXPERIMENTALEXTRUDER = 4


def metaJson5th(meta):
    '''Update botType for Replicator 5th Gen'''
    meta['bot_type'] = "replicator_5"
    meta['miracle_config']['_bot'] = "replicator_5"
    meta['miracle_config']['gaggles']['default']['startPosition']['x'] = -125
    meta['miracle_config']['gaggles']['default']['startPosition']['y'] = -99
    meta['miracle_config']['gaggles']['default']['startPosition']['z'] = 0.2
    return meta


def metaJsonPlus(meta):
    '''Update botType for Replicator+'''
    meta['bot_type'] = "replicator_b"
    meta['miracle_config']['_bot'] = "replicator_b"
    meta['miracle_config']['gaggles']['default']['startPosition']['x'] = -150
    meta['miracle_config']['gaggles']['default']['startPosition']['y'] = -100
    meta['miracle_config']['gaggles']['default']['startPosition']['z'] = 0.2
    return meta


def metaJsonMini(meta):
    '''Update botType for Replicator Mini'''
    meta['bot_type'] = "mini_4"
    meta['miracle_config']['_bot'] = "mini_4"
    meta['miracle_config']['gaggles']['default']['startPosition']['x'] = -59
    meta['miracle_config']['gaggles']['default']['startPosition']['y'] = -48
    meta['miracle_config']['gaggles']['default']['startPosition']['z'] = 1
    return meta


def metaJsonMiniPlus(meta):
    '''Update botType for Replicator Mini+'''
    meta['bot_type'] = "mini_8"
    meta['miracle_config']['_bot'] = "mini_8"
    meta['miracle_config']['gaggles']['default']['startPosition']['x'] = -59
    meta['miracle_config']['gaggles']['default']['startPosition']['y'] = 37
    meta['miracle_config']['gaggles']['default']['startPosition']['z'] = 0.2
    return meta


def metaJsonSmartExtruder(meta):
    '''Updates Tool types for Smart Extruder'''
    meta['tool_type'] = "mk12"
    meta['tool_types'] = ["mk12"]
    meta['miracle_config']['_extruders'] = ["mk12"]

    return meta


def metaJsonSmartExtruderPlus(meta):
    '''Updates Tool types for Smart Extruder+'''
    meta['tool_type'] = "mk13"
    meta['tool_types'] = ["mk13"]
    meta['miracle_config']['_extruders'] = ["mk13"]

    return meta


def metaJsonToughSmartExtruderPlus(meta):
    '''Updates Tool types for Tough Smart Extruder+'''
    meta['tool_type'] = "mk13_impla"
    meta['tool_types'] = ["mk13_impla"]
    meta['miracle_config']['_extruders'] = ["mk13_impla"]

    return meta


def metaJsonExperimentalExtruderPlus(meta):
    '''Updates Tool types for Experimental Extruder'''
    meta['tool_type'] = "mk13_experimental"
    meta['tool_types'] = ["mk13_experimental"]
    meta['miracle_config']['_extruders'] = ["mk13_experimental"]

    return meta


def generateMetajson(temp, vardict, machinetype, extrudertype):
    meta = json.loads(METAJSON)

    match machinetype:
        case MachineType.REPLICATOR5:
            meta = metaJson5th(meta)
        case MachineType.REPLICATORPlUS:
            meta = metaJsonPlus(meta)
        case MachineType.REPLICATORMINI:
            meta = metaJsonMini(meta)
        case MachineType.REPLICATORMINIPLUS:
            meta = metaJsonMiniPlus(meta)

    match extrudertype:
        case ExtruderType.SMARTEXTRUDER:
            meta = metaJsonSmartExtruder(meta)
        case ExtruderType.SMARTEXTRUDERPLUS:
            meta = metaJsonSmartExtruderPlus(meta)
        case ExtruderType.TOUGHEXTRUDER:
            meta = metaJsonToughSmartExtruderPlus(meta)
        case ExtruderType.EXPERIMENTALEXTRUDER:
            meta = metaJsonExperimentalExtruderPlus(meta)

    meta['bounding_box'] = vardict['bounding_box']

    meta['total_commands'] = vardict['toolpathfilelength']

    meta['duration_s'] = vardict['time']

    # I have no idea what this is supposed to be
    meta['commanded_duration_s'] = vardict['time'] / 2

    meta['num_z_transitions'] = vardict['z_transitions']
    meta['num_z_layers'] = vardict['z_transitions'] + 1

    meta['platform_temperature'] = vardict['bedtemp']

    meta['extruder_temperature'] = vardict['extruder_temperature']
    meta['extruder_temperatures'] = [meta['extruder_temperature']]

    meta['extrusion_distance_mm'] = vardict['extrusion_distance']
    meta['extrusion_distances_mm'] = [meta['extrusion_distance_mm']]

    meta['extrusion_mass_g'] = vardict['extrusion_distance'] * 0.00305
    meta['extrusion_masses_g'] = [meta['extrusion_mass_g']]

    meta['uuid'] = str(uuid4())

    with open('{}/meta.json'.format(temp), 'w') as metafile:
        json.dump(meta, metafile, indent=4)


def generateThumbnails(filename, temp):
    '''copied from sabesnait's rfork'''
    tnNames = []
    file = open(filename, 'r')
    line = file.readline()
    if "PrusaSlicer" not in line and "HEADER_BLOCK_START" not in line:  # only tested on Prusa Slicer
        print(line)
        return tnNames
    while True:
        line = file.readline()
        if "thumbnail begin" in line:
            thumbnailMeta = line.split(' ')
            thumbnailSize = thumbnailMeta[3]

            line = file.readline()
            thumbnail_data = ""
            while "thumbnail end" not in line and line:
                thumbnail_data = thumbnail_data + line.strip("; \n")
                line = file.readline()
            decoded_data = base64.b64decode(thumbnail_data)
            thumbnailFileName = '{}/thumbnail_' + thumbnailSize + '.png'
            tnNames.append(thumbnailFileName)
            with open(thumbnailFileName.format(temp), 'wb') as thumbnailFile:
                thumbnailFile.write(decoded_data)
        if not line:
            break
    file.close()
    return tnNames


def generateCommand(function, metadata, parameters, tags):
    return [{'command': {'function': function,
                         'metadata': dict(metadata),
                         'parameters': dict(parameters),
                         'tags': list(tags)}}]


def computeTime(prev, current):
    if [current['x'], current['y'], current['z']] == [prev['x'], prev['y'], prev['z']] and current['a'] != prev['a']:
        # retraction takes time as well, add it in
        # time = sqrt((e2-e1)^2)/feedrate
        distance = math.dist([current['a']], [prev['a']])
    else:
        # get time traveled by the equasion
        # time = sqrt((x2-x1)^2 + (y2-y1)^2 + (z2-z1)^2)/feedrate
        distance = math.dist([current['x'], current['y'], current['z']],
                             [prev['x'], prev['y'], prev['z']])
    return distance / current['feedrate']


def createToolpath(filename, temp):
    corpus = open(filename).readlines()
    processed = []
    linenum_last = len(corpus)
    linenum = 0
    printline = '{0:>' + str(len(str(linenum_last))) + '}/{1} {2:>3.0f}%'
    axis = \
        {
            'a': 0.0,
            'feedrate': 23.0,
            'x': -10.3,
            'y': -0.25,
            'z': 0.3
        }
    tempmetadata = \
        {
            'index': -1,
            'temperature': 0
        }
    fanstatus = \
        {
            'index': 0,
            'value': False
        }
    fanduty = \
        {
            'index': 0,
            'value': 0.0
        }
    printersettings = \
        {
            'bedtemp': 0,
            'heatbed': False,
            'time': 0.0,
            'toolpathfilelength': 0,
            'z_transitions': 0,
            'extruder_temperature': 0
        }
    printeroffset = \
        {
            'a': 0.0,
            'x': 0.0,
            'y': 0.0,
            'z': -0.05
        }
    print('lines processed:')
    print(printline.format(0, linenum_last, 0.0), end='')
    """
    Quick reference:
    G0/G1 is move
    M104 is set_toolhead_temperature
    M140 sets bed temp
    M106 is fan_duty (sets fan)
    M107 is toggle_fan (off)
    M141 sets chamber temperature
    G90 toggles absolute positioning
    G91 toggles relative positioning
    """
    ignoring = False
    for linenum, line in enumerate(corpus, start=1):

        if (linenum % 100) == 0 or linenum == linenum_last:
            if ignoring:
                print('\n')
            ignoring = False
            print('\x1b[2K\r' + printline.format(linenum, linenum_last, linenum / linenum_last * 100.0), end='')

        if line.startswith(';LAYER:'):
            sec = int(line.split(':', 1)[1])
            # We add the first section manually
            if sec > 0:
                processed += generateCommand('comment', {}, {'comment': f'Layer Section {sec} ({sec})'}, [])
                processed += generateCommand('comment', {}, {'comment': 'Material 0'}, [])

        line = line.split(';', 1)[0]
        line = [part for part in line.strip().split(' ') if part != '']

        if not line:
            continue

        if line[0] in ['G0', 'G1']:

            if len(line) == 2 and line[1][0] == 'F':
                axis['feedrate'] = float(line[1][1:]) / 60.0

            else:  # Normal move
                prev = axis.copy()
                for ax in line[1:]:
                    if ax[0] == 'E':
                        axis['a'] = printeroffset['a'] + float(ax[1:])
                    elif ax[0] == 'X':
                        axis['x'] = printeroffset['x'] + float(ax[1:])
                    elif ax[0] == 'Y':
                        axis['y'] = printeroffset['y'] + float(ax[1:])
                    elif ax[0] == 'Z':
                        axis['z'] = printeroffset['z'] + float(ax[1:])
                    elif ax[0] == 'F':
                        axis['feedrate'] = float(ax[1:]) / 60.0

                if line[0] == 'G0':
                    tag = 'Travel Move'
                else:
                    if prev['a'] < axis['a']:
                        tag = 'Infill'
                    elif prev['a'] == axis['a']:
                        tag = 'Leaky Travel Move'
                    elif axis['a'] < prev['a']:
                        tag = 'Retract'

                processed += generateCommand('move',
                                             {'relative': {'a': False,
                                                           'x': False,
                                                           'y': False,
                                                           'z': False}},
                                             axis,
                                             [tag])

                printersettings['time'] += computeTime(prev, axis)

                if prev['z'] < axis['z']:
                    printersettings['z_transitions'] += 1

        elif line[0] == 'M82':
            # E absolute
            pass

        elif line[0] == 'G92':
            for ax in line[1:]:
                if ax[0] == 'E':
                    printeroffset['a'] = axis['a'] + float(ax[1:])
                elif ax[0] == 'X':
                    printeroffset['x'] = axis['x'] + float(ax[1:])
                elif ax[0] == 'Y':
                    printeroffset['y'] = axis['y'] + float(ax[1:])
                elif ax[0] == 'Z':
                    printeroffset['z'] = axis['z'] + float(ax[1:])

        elif line[0] == 'M104':
            for ax in line[1:]:
                if ax[0] == 'T':
                    tempmetadata['index'] = int(ax[1:])
                elif ax[0] == 'S':
                    tempmetadata['temperature'] = int(ax[1:])
                    if tempmetadata['temperature'] != 0:
                        if printersettings['extruder_temperature'] == 0:
                            printersettings['extruder_temperature'] = tempmetadata['temperature']
                        else:
                            print('\x1b[2K\rMultiple temperatures issued during print, using only first.')
            if tempmetadata['index'] != -1:
                processed += generateCommand('set_toolhead_temperature',
                                             {},
                                             tempmetadata,
                                             [])
                if printersettings['tool{}temp'.format(tempmetadata['index'])] == 0:
                    printersettings['tool{}temp'.format(tempmetadata['index'])] = tempmetadata['temperature']
            else:  # there is only one extruder
                processed += generateCommand('set_toolhead_temperature',
                                             {},
                                             {'temperature': tempmetadata['temperature']},
                                             [])
                printersettings['tool0temp'] = tempmetadata['temperature']

        elif line[0] == 'M105':
            # Report temp
            pass

        elif line[0] == 'M109':
            # Wait for hotend temp
            pass

        elif line[0] == 'M106':
            for ax in line[1:]:
                if ax[0] == 'P':
                    fanduty['index'] = int(ax[1:])
                    fanstatus['index'] = int(ax[1:])
                elif ax[0] == 'S':
                    fanduty['value'] = float(ax[1:]) / 255
            if not fanstatus['value']:
                fanstatus['value'] = True
                processed += generateCommand('toggle_fan',
                                             {},
                                             fanstatus,
                                             [])
            processed += generateCommand('fan_duty',
                                         {},
                                         fanduty,
                                         [])

        elif line[0] == 'M107':
            fanstatus['value'] = False
            processed += generateCommand('toggle_fan',
                                         {},
                                         fanstatus,
                                         [])

        elif line[0] == 'M140':
            printersettings['bedtemp'] = int(line[1][1:])
            printersettings['heatbed'] = True

        else:
            if ignoring:
                print('   ', repr(line[0]), end='')
            else:
                ignoring = True
                print('\n\nignoring', repr(line[0]), end='')
        if DEBUG:
            processed += generateCommand('comment', {}, {'comment': f'{line}'}, [])

    print()
    print('writing toolpath')
    lines = [
        '{"command" : {"function":"comment","metadata":{},"parameters":{"comment":"Layer Section 0 (0)"},"tags":[]}},',
        '{"command" : {"function":"comment","metadata":{},"parameters":{"comment":"Material 0"},"tags":[]}},',
        '{"command" : {"function":"comment","metadata":{},"parameters":{"comment":"Lower Position  0"},"tags":[]}},',
        '{"command" : {"function":"comment","metadata":{},"parameters":{"comment":"Upper Position  0.3"},"tags":[]}},',
        '{"command" : {"function":"comment","metadata":{},"parameters":{"comment":"Thickness       0.3"},"tags":[]}},',
        '{"command" : {"function":"comment","metadata":{},"parameters":{"comment":"Width           2.5"},"tags":[]}},',
        '{"command" : {"function":"move","metadata":{"relative":{"a":false,"x":false,"y":false,"z":false}},"parameters":{"a":0.0,"feedrate":23.0,"x":-50.0,"y":-50.0,"z":0.30},"tags":["Travel Move"]}},']
    lines += [f'{json.dumps(c, sort_keys=False)},' for c in processed]
    lines += ['{"command" : {"function":"comment","metadata":{},"parameters":{"comment":"End of print"},"tags":[]}}']
    # compiledtoolpath = json.dumps(processed, sort_keys=False, indent=4)
    with open('{}/print.jsontoolpath'.format(temp), 'w') as toolpathfile:
        toolpathfile.write("\n".join(["[", *lines, "]"]))

    print('checking toolpath')
    assert printersettings['extruder_temperature'] > 0
    with open('{}/print.jsontoolpath'.format(temp), 'r') as toolpathfile:
        json.load(toolpathfile)

    print('collecting printer settings')

    printersettings['toolpathfilelength'] = len(lines)

    printersettings['extrusion_distance'] = max(c['command']['parameters']['a']
                                                for c in processed
                                                if c['command']['function'] == 'move')

    printcoords = [cmd['command']['parameters'] for cmd in processed
                   if set(cmd['command']['tags']) & {'Infill', 'Leaky Travel Move'}]

    bbox = {'x_max': max(c['x'] for c in printcoords),
            'x_min': min(c['x'] for c in printcoords),
            'y_max': max(c['y'] for c in printcoords),
            'y_min': min(c['y'] for c in printcoords),
            'z_max': max(c['z'] for c in printcoords),
            'z_min': min(c['z'] for c in printcoords)}
    # for c in printcoords:
    #    print(c)
    # input('press')
    print(bbox)

    # Make sure bounding box is centered near the origin in X/Y and at the bottom of Z.
    xrel = (bbox['x_max'] + bbox['x_min']) / (bbox['x_max'] - bbox['x_min'])
    yrel = (bbox['y_max'] + bbox['y_min']) / (bbox['y_max'] - bbox['y_min'])
    zrel = (bbox['z_max'] + bbox['z_min']) / (bbox['z_max'] - bbox['z_min'])
    print('xrel:')
    print(xrel)
    print('yrel:')
    print(yrel)
    print('zrel:')
    print(zrel)
    assert -0.15 < xrel < 0.15, xrel
    assert -0.15 < yrel < 0.15, yrel
    # assert  0.95 < zrel < 1.05, zrel
    assert 0 < bbox['z_min'] < 0.5, bbox['z_min']

    printersettings['bounding_box'] = bbox

    return printersettings


def packageMBotFile(filename, temp, tnNames):
    with zipfile.ZipFile(filename, 'w', compression=zipfile.ZIP_DEFLATED) as mbotfile:
        for tn in tnNames:
            mbotfile.write(tn.format(temp), arcname=tn.strip("{}/"))
        mbotfile.write('{}/meta.json'.format(temp), arcname='meta.json')
        mbotfile.write('{}/print.jsontoolpath'.format(temp), arcname='print.jsontoolpath')
    return

def main(filename, printer, extruder, slicer):
    try:
        print(printer)
        # If you need to change it and you aren't using the post processing script change these 2 lines to match whichever machine and extruder your using,
        # otherwise use the corresponding -Machine, and -extruder in your post processing setup.
        machinetype = MachineType.REPLICATORPlUS
        extrudertype = ExtruderType.SMARTEXTRUDERPLUS
        slicerScript = False
        temp = tempfile.mkdtemp()

        if "prusa" in slicer:
            #slicerScript = True
            print("prusa")
        if "orca" in slicer:
            #slicerScript = True
            print("orca")

        if printer == "MiniPlus" or printer == "3":
            machinetype = MachineType.REPLICATORMINIPLUS
            print("MiniPlus")
        if printer == "RepPlus" or printer == "0":
            machinetype = MachineType.REPLICATORPlUS
            print("RepPlus")
        if printer == "Mini5" or printer == "2":
            machinetype = MachineType.REPLICATORMINI
            print("Mini5")
        if printer == "1" or printer == "Rep5" in printer:
            machinetype = MachineType.REPLICATOR5
            print("Rep5")

        if extruder == "-SmartExtPlus" or extruder == "0":
            extrudertype = ExtruderType.SMARTEXTRUDERPLUS
            print("SmartExtPlus")

        if extruder == "-SmartExt"  or extruder ==  "1":
            extrudertype = ExtruderType.SMARTEXTRUDER
            print("SmartExt")

        if extruder == "-ToughExt" or extruder == "2":
            extrudertype = ExtruderType.TOUGHEXTRUDER
            print("ToughExt")

        if extruder == "-ExperimentalExt" or extruder == "3" in extruder:
            extrudertype = ExtruderType.EXPERIMENTALEXTRUDER
            print("ExperimentalExt")

        if slicerScript:
            output = str(getenv('SLIC3R_PP_OUTPUT_NAME')).replace('.gcode', '.makerbot')
        else:
            output = filename.replace('.gcode', '.makerbot')


        print("Printer: ", machinetype)
        print("Extruder: ", extrudertype)
        print('Generating toolpath for', output)
        status="Generating Toolpath for " + output
        vardict = createToolpath(filename, temp)
        print('Generating metadata for', output)
        status = "Generating Metadata"
        generateMetajson(temp, vardict, machinetype, extrudertype)
        print('Generating thumbnails for', output)
        status = "Generating Thumbnails"
        tnNames = generateThumbnails(filename, temp)
        print(len(tnNames), 'Thumbnails(s) generated')
        print('Packaging', output)
        packageMBotFile(output, temp, tnNames)
        print(output, 'done!')
        status = "Done!"

        return True

    except Exception as e:
        print()
        print('An Error')
        print(e)
        return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='mbotmake',
        description='Convert GCode to .Makerbot')
    parser.add_argument('filename')  # positional argument
    parser.add_argument('-p' '--printer', default="RepPlus")  # option that takes a value
    parser.add_argument('-e', '--extruder', default="SmartExtPlus")
    parser.add_argument('-s', '--slicer', default="prusa")
    args = parser.parse_args()

    main(args.filename, args.printer, args.extruder, args.slicer)
