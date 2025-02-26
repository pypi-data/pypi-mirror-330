#!/usr/bin/env python3
#-----------------------------------------------------------------------
#
# Find all devices which have subcircuit definitions in the path
# sky130A/libs.ref/sky130_fd_pr/.  List all of these devices.  Then
# find all paths from the directory models/ that will read the
# subcircuit definition through a hierarchical series of includes.
#-----------------------------------------------------------------------

import re
import os 
import sys

#-----------------------------------------------------------------------
# Find all devices used inside a subcircuit definition and return them
# as a list.  "netlist" is the full path to a layout-extracted netlist
# (.spice file) to parse.
#-----------------------------------------------------------------------

def find_devices_in_subckt(netlist):

    stddevrex = re.compile('[xmqdcrl]([^ \t]+)[ \t]+(.+)', re.IGNORECASE)
    subcktrex = re.compile('.subckt[ \t]+([^ \t]+)[ \t]+(.*)', re.IGNORECASE)
    endsrex = re.compile('.ends', re.IGNORECASE)

    devlist = []

    with open(netlist, 'r') as ifile:
        spicelines = ifile.read().splitlines()
        insub = False
        for line in spicelines:
            if not insub:
                smatch = subcktrex.match(line)
                if smatch:
                    insub = True
            else:
                ematch = endsrex.match(line)
                if ematch:
                    insub = False
                else:
                    dmatch = stddevrex.match(line)
                    if dmatch:
                        tokens = dmatch.group(2).split()
                        for token in tokens[::-1]:
                            if '=' not in token:
                                devlist.append(token)
                                break

    return devlist

#-----------------------------------------------------------
# Find all models in the model directory path, recursively
#-----------------------------------------------------------

def addmodels(modelpath):
    modelfmts = os.listdir(modelpath)
    files_to_parse = []
    for modelfmt in modelfmts:
        if os.path.isdir(modelpath + '/' + modelfmt):
            files_to_parse.extend(addmodels(modelpath + '/' + modelfmt))
        else:
            fmtext = os.path.splitext(modelfmt)[1]
            if fmtext == '.spice':
                files_to_parse.append(modelpath + '/' + modelfmt)

    return files_to_parse

#-----------------------------------------------------------
# Find the device name in a SPICE "X" line
#-----------------------------------------------------------

def get_device_name(line):
    # The instance name has already been parsed out of the line, and
    # all continuation lines have been added, so this routine finds
    # the last keyword that is not a parameter (i.e., does not contain
    # '=').

    tokens = line.split()
    for token in tokens:
        if '=' in token:
            break
        else:
            devname = token

    return devname

#-----------------------------------------------------------
# Pick the file from the list that is appropriate for the
# choice of either FEOL or BEOL corner.  Mostly ad-hoc rules
# based on the known file names.
#-----------------------------------------------------------

def choose_preferred(inclist, feol, beol, notop, debug):

    try:
        # The top-level file 'sky130.lib.spice' is always preferred
        validinc = next(item for item in inclist if os.path.split(item)[1] == 'sky130.lib.spice')
    except:
        # (1) Sort list by the length of the root name of the file
        inclist = sorted(inclist, key=lambda x: len(os.path.splitext(os.path.split(x)[1])[0]))

        # (2) Sort list by depth of directory hierarchy
        inclist = sorted(inclist, key=lambda x: len(x.split('/')))

        validinc = None
        for incfile in inclist:
            incname = os.path.split(incfile)[1]
            if debug:
                print('       choose preferred, checking: "' + incname + '"')

            if incname == 'custom.spice':
                # Ignore "custom.spice" (example file, unused)
                continue
            elif notop and incname.startswith('correl'):
                # Ignore "correl1.spice", etc., if "-notop" option chosen
                continue
            elif 'leak' in incname:
                # Ignore anything with "leak" in the name (don't know under
                # what condition this would be used).
                continue
            elif 'monte' in incname and 'mc' not in feol:
                # Ignore anything with "montecarlo" in the name unless feol == 'mc'
                continue
            elif feol in incname:
                validinc = incfile
                break
            elif 't' in beol and 'typical' in incname:
                validinc = incfile
                break
            elif 'h' in beol and 'high' in incname:
                validinc = incfile
                break
            elif 'l' in beol and 'low' in incname:
                validinc = incfile
                break
            else:
                # Record this as a valid entry but keep going.
                validinc = incfile

    if debug:
        if validinc:
            incname = os.path.split(validinc)[1]
            print('      choose_preferred:  chose ' + validinc + ' (' + incname + ')')
        else:
            print('      choose_preferred:  no suitable include files found.')

    return validinc

#---------------------------------------------------------------------
# Sort files with the subcircuit by relevance.  Files are considered
# in the order ".model.spice", ".pm3.spice", and ".spice".
#---------------------------------------------------------------------

def preferred_order(subfiles, feol):
    ordfiles = []
    feolstr = '__' + feol

    # Sort by length first, so shorter ones, e.g., without "leak",
    # end up at the front of the list.
    ordlist = sorted(subfiles, key=len)

    for file in ordlist[:]:
        if file.endswith('.corner.spice') and feolstr in file:
            ordfiles.append(file)
            ordlist.remove(file)

    for file in ordlist[:]:
        if file.endswith('.model.spice'):
            ordfiles.append(file)
            ordlist.remove(file)

    for file in ordlist[:]:
        if file.endswith('.pm3.spice') and feolstr in file:
            ordfiles.append(file)
            ordlist.remove(file)

    for file in ordlist[:]:
        if file.endswith('.pm3.spice'):
            ordfiles.append(file)
            ordlist.remove(file)

    ordfiles.extend(ordlist)
    return ordfiles

#-----------------------------------------------------------
# Find the appropriate file to include to handle this device
#-----------------------------------------------------------

def check_device(subfiles, includedict, modfilesdict, feol, beol, notop, debug):
    # subfiles = list of files that define this subcircuit.
    # includedict  = files that include the dictionary keyword file
    # modfilesdict = files that are included by the dictionary keyword file
    # feol = FEOL corner (fs, tt, ss, etc.) for transistors, diodes
    # beol = BEOL corner (hl, tt, ll, etc.) for capacitors, resistors, inductors

    ordfiles = preferred_order(subfiles, feol)
    if debug:
        print('')
        print('Check_device:  Search order:')
        for ordfile in ordfiles:
            print('   ' + os.path.split(ordfile)[1])

    # Find the proper include file to include this device.  Attempt on all
    # entries in ordfiles, and stop at the first one that returns a result.
    # Assume that all files have unique names and point to the proper
    # location, so that is is only necessary to look at the last path
    # component.

    if debug:
        print('\nClimb hierarchy of includes to the top:')

    for ordfile in ordfiles:
        ordname = os.path.split(ordfile)[1]
        if debug:
            print('   (1) Search for "' + ordname  + '"')
        try:
            inclist = includedict[ordname][1:]
        except:
            if debug:
                print('   No include file found for "' + ordfile + '"')
                print('   Sample entry:')
                for key in includedict:
                    print('      ' + key + ': "' + str(includedict[key][1:]) + '"')
                    break
            continue
        else:
            if debug:
                print('   Starting list = ')
                for item in inclist:
                    print('      ' + item)

        i = 0
        while True:
            i += 1
            if i > 1000:
                raise SystemError('Suck!?')

            incfile = choose_preferred(inclist, feol, beol, notop, debug)
            if not incfile:
                break
            incname = os.path.split(incfile)[1]
            if debug:
                print('   (2) Search for "' + incname  + '"')
            try:
                inclist = includedict[incname][1:]
            except:
                break
            else:
                if debug:
                    print('   Continuing list = ')
                    for item in inclist:
                        print('      ' + item)

        if debug:
            print('Final top level include file is: "' + incfile + '"')
        return incfile

    # Should only happen if subfiles is empty list
    return None

#-----------------------------------------------------------
# Find all cells and all models
#-----------------------------------------------------------

def find_everything(cellspath, modelspath):

    allcells = os.listdir(cellspath)

    subcktrex = re.compile('\.subckt[ \t]+([^ \t]+)[ \t]+', re.IGNORECASE)
    includerex = re.compile('\.include[ \t]+([^ \t]+)', re.IGNORECASE)

    filesdict  = {}
    subcktdict  = {}
    includedict  = {}
    modfilesdict  = {}

    for cellfile in allcells:
        cellpath = cellspath + '/' + cellfile
        cellfmts = os.listdir(cellpath)
        files_to_parse = []
        for cellfmt in cellfmts:
            fmtext = os.path.splitext(cellfmt)[1]
            if fmtext == '.spice':
                files_to_parse.append(cellpath + '/' + cellfmt)

        for file in files_to_parse:
            with open(file, 'r') as ifile:
                spicelines = ifile.read().splitlines()
                for line in spicelines:
                    smatch = subcktrex.match(line)
                    if smatch:
                        subname = smatch.group(1)
                        try:
                            subcktdict[subname].append(file)
                        except:
                            subcktdict[subname] = [file]
                        filetail = os.path.split(file)[1]
                        try:
                            filesdict[filetail].append(subname)
                        except:
                            filesdict[filetail] = [subname]

    files_to_parse = addmodels(modelspath)
    files_to_parse.extend(addmodels(cellspath))

    for file in files_to_parse:
        # NOTE:  Avoid problems with sonos directories using
        # "tt.spice", which causes the include chain recursive
        # loop to fail to exit.  This is a one-off exception
        # (hack alert)
        if '_of_life' in file:
            continue
        if '/tests/' in file:
            continue

        with open(file, 'r') as ifile:
            spicelines = ifile.read().splitlines()
            for line in spicelines:
                imatch = includerex.match(line)
                if imatch:
                    incname = imatch.group(1).strip('"')
                    inckey = os.path.split(incname)[1]

                    try:
                        inclist = includedict[inckey]
                    except:
                        includedict[inckey] = [incname, file]
                    else:
                        if file not in inclist[1:]:
                            includedict[inckey].append(file)
                    filetail = os.path.split(file)[1]
                    try:
                        modlist = modfilesdict[filetail]
                    except:
                        modfilesdict[filetail] = [incname]
                    else:
                        if incname not in modlist:
                            modfilesdict[filetail].append(incname)

    return filesdict, subcktdict, includedict, modfilesdict

#-----------------------------------------------------------
# Main application
#-----------------------------------------------------------

def do_find_all_devices(libtop, techtop, sourcefile, cellname=None, feol='tt', beol='tt', doall=False, notop=False, debug=True):

    (filesdict, subcktdict, includedict, modfilesdict) = find_everything(libtop, techtop)

    if sourcefile:
        # Parse the source file and find all 'X' records, and collect a list
        # of all primitive devices used in the file by cross-checking against
        # the dictionary of subcircuits.

        devrex = re.compile('x([^ \t]+)[ \t]+(.*)', re.IGNORECASE)
        incfiles = []

        with open(sourcefile, 'r') as ifile:
            spicelines = ifile.read().splitlines()

        if debug:
            print('Netlist file first line is "' + spicelines[0] + '"')

        isdev = False
        for line in spicelines:
            if line.startswith('*'):
                continue
            if line.strip() == '':
                continue
            elif line.startswith('+'):
                if isdev:
                    rest += line[1:]
            elif isdev:
                devname = get_device_name(rest)
                try:
                    subfiles = subcktdict[devname]
                except:
                    pass
                else:
                    incfile = check_device(subfiles, includedict, modfilesdict, feol, beol, notop, debug)
                    if not incfile:
                        incfile = preferred_order(subfiles, feol)[0]

                    if incfile:
                        if debug:
                            print('Device ' + devname + ':  Include ' + incfile)
                        if incfile not in incfiles:
                            incfiles.append(incfile)
                    else:
                        print('Something went dreadfully wrong with device "' + devname + '"')

                isdev = False
        
            smatch = devrex.match(line)
            if smatch:
                instname = smatch.group(1)
                rest = smatch.group(2)
                isdev = True
            elif isdev:
                devname = get_device_name(rest)
                try:
                    subfiles = subcktdict[devname]
                except:
                    pass
                else:
                    incfile = check_device(subfiles, includedict, modfilesdict, feol, beol, notop, debug)
                    if not incfile:
                        incfile = preferred_order(subfiles, feol)[0]

                    if incfile:
                        if debug:
                            print('Device "' + devname + '":  Include "' + incfile + '"')
                        if incfile not in incfiles:
                            incfiles.append(incfile)
                    else:
                        print('Something went dreadfully wrong with device "' + devname + '"')
                isdev = False

        # Return the .include lines needed
        return incfiles

    elif cellname:
        # Diagnostic:  Given a cell name on the command line (with -cell=<name>),
        # Run check_device() on the cell and report.
        try:
            subfiles = subcktdict[cellname]
        except:
            print('No cell "' + cellname + '" was found in the PDK files.')
            return []

        incfile = check_device(subfiles, includedict, modfilesdict, feol, beol, notop, debug)
        if debug:
            print('')
            print('Report:')
            print('')
            print('Cell = "' + cellname + '"')
            print('')

        # If incfile is just <cellname>.spice, then it is a layout-extracted
        # netlist and there isn't any model definition for it.  Check the
        # netlist subckt contents for other subcircuits being used, and check
        # them recursively.  If the netlist subckt definition has no contents,
        # then flag this as a major error.

        if not incfile and len(subfiles) == 1:
            if debug:
                print('Cell is only defined by layout-extracted netlist')
            subfile = subfiles[0]
            devsused = find_devices_in_subckt(subfile)
            if len(devsused) == 0:
                print('ERROR:  Layout-extracted netlist of ' + cellname + ' is empty!')
                # Return empty list
                return []

            incfiles = [subfile]
            for device in devsused:
                try:
                    newincfile = do_find_all_devices(libtop, techtop, sourcefile, device,
					feol, beol, doall, notop, debug)[0]
                except:
                    newincfile = None
                if newincfile and newincfile not in incfiles:
                    incfiles.append(newincfile)

            return incfiles

        bestfilepath = preferred_order(subfiles, feol)[0]
        if bestfilepath.startswith(libtop):
            bestfile = bestfilepath[len(libtop) + 1:]
        print('Subcircuit defined in (from ' + libtop + '/): "' + bestfile + '"')

        if debug:
            print('')
            print('Top level include: ')

        if incfile:
            return [incfile]
        else:
            return [bestfilepath]

    elif doall:
        allincludes = []
        for cellname in subcktdict:

            # Diagnostic:  Given a cell name on the command line (with -cell=<name>),
            # Run check_device() on the cell and report.
            try:
                subfiles = subcktdict[cellname]
            except:
                print('No cell "' + cellname + '" was found in the PDK files.')
                continue

            incfile = check_device(subfiles, includedict, modfilesdict, feol, beol, notop, debug)
            print('Cell = "' + cellname + '"')
            bestfilepath = preferred_order(subfiles, feol)[0]
            if bestfilepath.startswith(libtop):
                bestfile = bestfilepath[len(libtop) + 1:]
            print('   Subcircuit: "' + os.path.split(bestfile)[1] + '"')
            print('   Include: ', end='')
            if incfile:
                if incfile not in allincludes:
                    allincludes.append(incfile)
                print('"' + incfile + '"')
            else:
                if bestfilepath not in allincludes:
                    allincludes.append(bestfilepath)
                print('"' + bestfilepath + '"')

        print('')
        print('Summary:  All files to include:\n')
        return allincludes

    else:
        # No source file given, so just dump the lists of subcircuits, models,
        # and files into four different output files.

        nsubs = 0
        with open('sublist.txt', 'w') as ofile:
            for key in subcktdict:
                nsubs += 1
                value = subcktdict[key]
                print(key + ': ' + ', '.join(value), file=ofile)

        nfiles = 0
        with open('filelist.txt', 'w') as ofile:
            for key in filesdict:
                nfiles += 1
                value = filesdict[key]
                print(key + ': ' + ', '.join(value), file=ofile)

        with open('inclist.txt', 'w') as ofile:
            for key in includedict:
                value = includedict[key]
                print(key + '(' + value[0] + '): ' + ', '.join(value[1:]), file=ofile)

        with open('modfilelist.txt', 'w') as ofile:
            for key in modfilesdict:
                value = modfilesdict[key]
                print(key + ': ' + ', '.join(value), file=ofile)

        print('Found ' + str(nsubs) + ' subcircuit definitions in ' + str(nfiles) + ' files.')
        return []

#-----------------------------------------------------------
# Command-line entry point
#-----------------------------------------------------------

if __name__ == "__main__":

    optionlist = []
    arguments = []

    for option in sys.argv[1:]:
        if option.find('-', 0) == 0:
            optionlist.append(option)
        else:
            arguments.append(option)

    variant = 'sky130A'
    libtop = '/usr/share/pdk/' + variant + '/libs.ref/sky130_fd_pr/'
    # techtop = '/usr/share/pdk/' + variant + '/libs.tech/ngspice/'
    techtop = '../../ngspice/'
   
    # Default FEOL corner is "tt", and default BEOL corner is "tt"
    feol = 'tt'
    beol = 'tt'
    cellname = None
    debug = False
    doall = False
    notop = False

    # Override defaults from options

    for option in optionlist:
        if option.startswith('-variant'):
            try:
                variant = option.split('=')[1]
            except:
                print('Option usage:  -variant=<variantstring>')
                sys.exit(1)
        elif option.startswith('-corner') or option.startswith('-feol'):
            try:
                feol = option.split('=')[1]
            except:
                print('Option usage:  -feol=<corner_name>')
                sys.exit(1)
        elif option.startswith('-beol'):
            try:
                beol = option.split('=')[1]
            except:
                print('Option usage:  -beol=<corner_name>')
                sys.exit(1)
        elif option.startswith('-cell'):
            try:
                cellname = option.split('=')[1]
            except:
                print('Option usage:  -cell=<cell_name>')
                sys.exit(1)
        elif option == '-notop':
            notop = True
        elif option == '-all':
            doall = True
        elif option == '-debug':
            debug = True

    # Parse "-pdkpath" after the others because it is dependent on any option
    # "-variant" passed on the command line.

    for option in optionlist:
        if option.startswith('-pdkpath'):
            try:
                pathroot = option.split('=')[1]
            except:
                print('Option usage:  -pdkpath=<pathname>')
                sys.exit(1)
            if not os.path.isdir(pathroot):
                print('Cannot find PDK directory ' + pathroot)
                sys.exit(1)
            libtop = pathroot + '/' + variant + '/libs.ref/sky130_fd_pr/'
            # techtop = pathroot + '/' + variant + '/libs.tech/ngspice/'
            techtop = '../../ngspice/'
            if not os.path.isdir(libtop):
                print('Cannot find primitive device directory ' + libtop)
                sys.exit(1)
            if not os.path.isdir(techtop):
                print('Cannot find ngspice model directory ' + techtop)
                sys.exit(1)

    # To be done:  Make this a useful routine that can insert one or more
    # .include statements into a SPICE netlist.  Should take any number of
    # files on the arguments line and modify the files in place.

    if len(arguments) > 0:
        sourcefile = arguments[0]
        if not os.path.isfile(sourcefile):
            print('Cannot read SPICE source file ' + sourcefile)
            sys.exit(1)
    else:
        sourcefile = None

    if not os.path.isdir(libtop):
        print('Cannot find primitive device library ' + libtop)
        sys.exit(1)
    elif debug:
        print('\nFinding everything in ' + libtop + '.')

    incfiles = do_find_all_devices(libtop, sourcefile, cellname, feol, beol, doall, notop, debug)
    for incfile in incfiles:
        if incfile.endswith('.lib.spice'):
            print('.lib ' + incfile + ' ' + feol)
        else:
            print('.include "' + incfile + '"')

    sys.exit(0)
