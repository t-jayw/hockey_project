import datetime as dt
import today_in_hockey as tih
import hockey_utils as hu

today = dt.date.today()
end = dt.date(2013, 10, 01)

date_list = []
point = dt.date(2001, 9, 01)
plus = dt.timedelta(days=1)

while point < end:
  print point.strftime("%m-%d-%Y")
  date = point.strftime("%m-%d-%Y")
  days_links = tih.get_links_days_games(date)
  
  if days_links:
     days_games = [tih.Game(link) for link in days_links]
     for x in days_games:
       hu.sqlite_insert('/Users/tylerjaywood/sqlite_dbs/hockey.db',
                        'games_basic', hu.games_basic_insert(x))
  date_list += point.strftime("%m-%d-%Y")
  point += plus
