import re
import sys
from datetime import date as dt
from BeautifulSoup import BeautifulSoup as bs
import argparse
import urllib2

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
  day_soup = gen_soup(day_url)
 
  day_links = [BASE_URL+game.a["href"] for game in day_soup.find("tbody").findAll("tr")]
  
  return day_links

def game_summary(game_link):
  """generate a brief summary of a game"""
  game_soup = gen_soup(game_link)

class Game:
  def __init__(self, game_link):
    self.name = game_link
    self.game_link = game_link
    self.game_soup = gen_soup(game_link)
    self.teams = [x.a.text for x in self.game_soup.findAll("span", "bold_text") 
          if x.findAll('a', href=True)]
    self.score = ["".join(re.findall(r'\d', x.text)) for x in self.game_soup.findAll("span", "bold_text")
          if re.findall(r'\d', x.text)] 
  
  def announce(self):
    print 'game: '+'\n'+self.teams[0]+': '+self.score[0]+'\n''@ '+self.teams[1]+': '+self.score[1]

if __name__ == "__main__":
  args = parse_args(sys.argv)
  days_games = [Game(x) for x in get_links_days_games(args.date)]
  
  scores = [x.announce() for x in days_games]
