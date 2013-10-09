import os
import sys
import re
import argparse
from BeautifulSoup import BeautifulSoup as bs
import urllib2
from datetime import date as dt
import hockey_utils


BASE_URL = "http://www.hockey-reference.com"
 
def parse_args(args):
  parser = argparse.ArgumentParser(prog=args[0])
  parser.add_argument('date', help='"MM-DD-YY"')
  return parser.parse_args(args[1:])
 
def gen_soup(url):
  html = urllib2.urlopen(url)
  soup = bs(html)
  return soup
 
def parse_date(datestring):
  datevec = datestring.split('-')
  return datevec
 
def get_links_days_games(day):
  """http://www.hockey-reference.com/boxscores/index.cgi?month=10&day=1&year=2013"""
  datevec = parse_date(day)
  m = datevec[0]
  d = datevec[1]
  y = datevec[2]
  day_url = BASE_URL+"/boxscores/index.cgi?month=%s&day=%s&year=%s"%(m,d,y)
  print "scraping " + day_url
  day_soup = gen_soup(day_url)
  
  try:
    day_links = [BASE_URL+game.a["href"] for game in day_soup.find("tbody").findAll("tr")]
    print str(len(day_links)) + " games played this day"
  except AttributeError:
    print "no games on " + day
    day_links = False
  
  return day_links
 
class Game:
  def __init__(self, game_link):
    self.name = game_link
    self.game_link = game_link
    self.game_soup = gen_soup(game_link)
    self.teams = [hockey_utils.team_abbrevs[x.a.text] 
          for x in self.game_soup.findAll("span", "bold_text")
          if x.findAll('a', href=True)]
    self.score = ["".join(re.findall(r'\d', x.text)) 
        for x in self.game_soup.findAll("span", "bold_text") 
        if re.findall(r'\d', x.text)]
    self.scoredict = dict(zip(self.teams, self.score))
    self.date = ""
 
  def __str__(self):
    result = ""
    for k,v in self.scoredict.items():
      result += "%s: %s "%(k,v)
    return result

  def determine_winner(self):
    winner = max(self.scoredict, key=self.scoredict.get)
    return winner


if __name__ == "__main__":
  args = parse_args(sys.argv)
  links = get_links_days_games(args.date)
  if links:
    days_games = [Game(x) for x in get_links_days_games(args.date)]

    for x in days_games:
      hockey_utils.sqlite_insert("/Users/tylerw/learnpy/sqlite_dbs/hockey.db", 'games_basic',
          hockey_utils.games_basic_insert(x))
