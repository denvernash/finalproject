Sources:
1. Flickr - https://www.flickr.com/services/api/
2. Petfinder - https://www.petfinder.com/developers/api-docs
3. Wikipedia - https://www.mediawiki.org/wiki/API:Main_page


Requirements:

  API Key from Flickr, API Key from Petfinder
  These two keys should be included in a file called secrets.py

  For Flickr Key - https://www.flickr.com/services/apps/create/
  For Petfinder Key - https://www.petfinder.com/developers/api-key

  The flask app uses plotly scatter plots for mapping information
  https://plot.ly/python/scatter-plots-on-maps/


Structure:

 - Building the database:
    build_database.py pulls information from 3 other files (wikidog.py,
      flickrdog.py, nato.py) to conglomerate information into 4 main class structures.

      These are Dog, Breed, Image, and Shelter. These contain all the information
      necessary to insert information into the database

  - Flask App:
    the flask app pulls information from the database through mapping.py that
    contains 4 other main class structures:
    Display_Dog, Display_Breed, Display_Image, and Display_Shelter
    which contain the corresponding information from the database


User Guide:
  the file to run is app.py - this will generate a flask application that will
  show the webpage at your local host.

  From the homepage, navigate to the breeds page. This will show a table of dog
  breeds that you can sort through. Each table row contains general information
  about the breed and will contain 3 links.

  To see more specific details about the breed select the link on the breed name
  in column 2

  To see a table of specific dogs of a breed available for adoption select the
  count available number in column 5

  To map out where those dogs available for adoption are located, select map in
  column 6




Cautionary Notes for building the database:
  There are 3 cache files associated with this project, two of these files are
  very large, 30 MB and 20MB.

  Getting this data fresh would take a number of
  days to complete and the programs are not currently optimized to build the
  database with fresh data.

  With this in mind, take precautions to ensure that
  you have the cache files before running build_database.py, wikidog.py,
  flickrdog.py, or project_test.py.



































“Powered by Petfinder” and link to http://www.petfinder.com.

"This product uses the Flickr API but is not endorsed or certified by Flickr."


"This product includes data created by MaxMind, available from
http://www.maxmind.com/"

OPEN DATA LICENSE for MaxMind WorldCities and Postal Code Databases

Copyright (c) 2008 MaxMind Inc.  All Rights Reserved.

The database uses toponymic information, based on the Geographic Names Data Base, containing official standard names approved by
the United States
Board on Geographic Names and maintained by the National Geospatial-Intelligence Agency. More information is available at the Maps and
Geodata link at www.nga.mil. The National Geospatial-Intelligence Agency name, initials, and seal
are protected by 10 United States
Code Section 445.

It also uses free population data from Stefan Helders www.world-gazetteer.com.
Visit his website to download the free population data.  Our database
combines Stefan's population data with the list of all cities in the world.

All advertising materials and documentation mentioning features or use of
this database must display the following acknowledgment:
"This product includes data created by MaxMind, available from
http://www.maxmind.com/"

Redistribution and use with or without modification, are permitted provided
that the following conditions are met:
1. Redistributions must retain the above copyright notice, this list of
conditions and the following disclaimer in the documentation and/or other
materials provided with the distribution.
2. All advertising materials and documentation mentioning features or use of
this database must display the following acknowledgement:
"This product includes data created by MaxMind, available from
http://www.maxmind.com/"
3. "MaxMind" may not be used to endorse or promote products derived from this
database without specific prior written permission.

THIS DATABASE IS PROVIDED BY MAXMIND.COM ''AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL MAXMIND.COM BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
DATABASE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
