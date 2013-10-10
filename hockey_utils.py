import re
import os
import sys
from datetime import date as dt
from BeautifulSoup import BeautifulSoup as bs
import argparse
import urllib2
import sqlite3

games_basic_schema = ['home_team', 'home_score', 'away_team', 'away_score', 'winner', 'date']

def sqlite_insert(db, table, values):
   """provide databse path, table, 
   and the values string for insertion to sqlite table"""

   connect_error = not os.path.exists(db)

   if connect_error:
     print "failed to connect to %s"%(db)
   elif table == 'games_basic':
     schema = ",".join(games_basic_schema)
     ins_cmd = "INSERT INTO %s (%s) VALUES (?,?,?,?,?,?)"%(table, schema)
     print "row = " + str(values)

     with sqlite3.connect(db) as conn:
       print 'inserting data'
       c = conn.cursor()
       c.execute(ins_cmd, values)    
       print 'row inserted'



def games_basic_insert(game):
  """Takes a Game class instance as an argument and generates
  the values for an insert command to the games_basic table
  in the hockey sqlite3 db"""
  winner = game.determine_winner()
  day = ''
  if len(game.date) > 1:
    day = game.date
    print day
  else:
    ints = re.findall(r'\d', game.name)
    ints = ints[:-1]
    day = "-".join([
      "".join(ints[4:6]), "".join(ints[6:]), "".join(ints[0:4])])
  values =(
      [game.scoredict.keys()[1],game.scoredict.values()[1],
        game.scoredict.keys()[0],game.scoredict.values()[0],
        winner,day])
 
  return values 


team_abbrevs = {
    "Anaheim Ducks"           :"ANA",
    "Boston Bruins"           :"BOS",
    "Buffalo Sabres"          :"BUF",
    "Calgary Flames"          :"CAL",
    "Carolina Hurricanes"     :"CAR",
    "Chicago Blackhawks"      :"CHI",
    "Colorado Avalanche"      :"COL",
    "Columbus Blue Jackets"   :"CBJ",
    "Dallas Stars"            :"DAL",
    "Detroit Red Wings"       :"DET",
    "Edmonton Oilers"         :"EDM",
    "Florida Panthers"        :"FLA",
    "Los Angeles Kings"       :"LAK",
    "Minnesota Wild"          :"MIN",
    "Montreal Canadiens"      :"MTL",
    "Nashville Predators"     :"NSH",
    "New Jersey Devils"       :"NJD",
    "New York Islanders"      :"NYI",
    "New York Rangers"        :"NYR",
    "Ottawa Senators"         :"OTT",
    "Philadelphia Flyers"     :"PHI",
    "Phoenix Coyotes"         :"PHX",
    "Pittsburgh Penguins"     :"PIT",
    "San Jose Sharks"         :"SJS",
    "St. Louis Blues"         :"STL",
    "Tampa Bay Lightning"     :"TBL",
    "Toronto Maple Leafs"     :"TOR",
    "Vancouver Canucks"       :"VAN",
    "Washington Capitals"     :"WSH",
    "Winnipeg Jets"           :"WPG",
    "Mighty Ducks of Anaheim" :"MDA",
    "Atlanta Flames"          :"ATF",
    "Hartford Whalers"        :"HAR",
    "Chicago Black Hawks"     :"CBH",
    "Quebec Nordiques"        :"QUE",
    "Minnesota North Stars"   :"MNS",
    "Atlanta Thrashers"       :"ATL",
    }
