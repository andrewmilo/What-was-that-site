#!/usr/bin/env python
__author__ = "Andrew Miloslavsky"
__copyright__ = "Copyright 2016"
__license__ = "MIT"
__maintainer__ = "Andrew Miloslavsky"
__email__ = "amiloslavsky@gmail.com"
__status__ = "Production"

from HistoryLib import *

SUPPORTED_BROWSERS = 'supported_browsers.txt'

def menu( options ):
    for counter, option in enumerate( options ):
            print ( "[" + str(counter) + "] %s" % option )

print ("\n**Please close all browsers until the history is retrieved.**\n")

with open( SUPPORTED_BROWSERS ) as f:
    browsers = f.readlines()

menu( browsers )

selection = int(input('Select Browser: '))
search_string = input('Search string: ')
search_startmonth = int(input('Start month: '))
search_endmonth = int(input('End month: '))
search_startday = int(input('Start day: '))
search_endday = int(input('End day: '))
search_startyear = int(input('Start year: '))
search_endyear = int(input('End year: '))

# Retrieve links from history
links = get_history_links( selection,
                           search_startmonth, 
                           search_endmonth, 
                           search_startday, 
                           search_endday,
                           search_startyear,
                           search_endyear )

# Search links for search string
found = search_links( links, search_string )

print ("\nFound {} matches.".format( len( found ) ) )

# Record results
f = open( 'output.txt', 'w' )
for link in found:
    f.write( link + "\n" )
f.close()