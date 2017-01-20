#!/usr/bin/env python
__author__ = "Andrew Miloslavsky"
__copyright__ = "Copyright 2016"
__license__ = "MIT"
__maintainer__ = "Andrew Miloslavsky"
__email__ = "amiloslavsky@gmail.com"
__status__ = "Production"

import sqlite3
import os
import urllib2
import re
import threading
import Queue
from threading import Thread
from datetime import datetime, timedelta

# Gets links from browser histories
def get_history_links( selection, startmonth, endmonth, startday, endday, startyear, endyear ):

    links = []

    if selection == 0 or str(selection).lower() == "google chrome" or str(selection).lower() == "chrome": # chrome
        conn = sqlite3.connect( os.getenv("APPDATA") + '\..\Local\Google\Chrome\User Data\Default\history' )

        c = conn.cursor()

        for row in (c.execute('select url, title, visit_count, last_visit_time from urls')):
            row = list(row)
            url_time = datetime(1601, 1, 1) + timedelta(microseconds=row[3])
            row[3] = url_time

            if ( row[3].date().month >= startmonth
            and row[3].date().month <= endmonth
            and row[3].date().day >= startday
            and row[3].date().day <= endday
            and row[3].date().year >= startyear
            and row[3].date().year <= endyear ):
                links.append( row )

        conn.commit()
        conn.close()
    else:
        print "Browser not supported."

    print "\n{} links found.".format( len( links ) )

    return links         

# Performs a search on 1 link
def search_link( output_list, link, search_string ):

    try:
        r = urllib2.urlopen( link[ 0 ] ).read()
        
        words = re.search(search_string, r, re.IGNORECASE)
        if words:
            matchtext = "[Match: " + words.group(0) + "] on " + link[0] + " visited on " + str(link[3].date()) + " at " + str(link[3].time());
            print matchtext + "\n"
            output_list.append( matchtext + "\n" )
    except urllib2.HTTPError, e:
        pass#print( "[Warning: HTTP Error] " + link[0] + "\n"  )
    except urllib2.URLError, e:
        pass#print( "[Warning: HTTP Error] " + link[0] + "\n"  

# Distributes all links to threads
def search_links( link_list, search_string ):
    output = []
    threads = []
    
    print "\n[Queuing links...]\n"

    # Main thread distributes all the links
    for link in link_list:
        t = threading.Thread(target=search_link, args=(output,link,search_string))
        threads.append( t )
    
    for thread in threads: # Starts all threads as daemons
        thread.setDaemon( True )
        thread.start()
    for thread in threads: # Waits for all threads to finish
        thread.join()

    return output