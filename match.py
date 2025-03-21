from utils import parse_time
from team import Team
from event import Event
from scoreboard import Scoreboard

# Description: This file contains the Match class which is used to store the match data.
class Match:
    def __init__(self, match_id, obj):
        self.match_id = match_id
        self.name = obj['name']
        self.description = obj.get('description', '')
        self.teams = [Team(obj['name'], obj['color'], obj.get('code'), obj.get('score', 0)) for obj in obj['teams']]
        self.main_video = obj.get('main_video', f'{match_id}.mp4')
        self.logo_img = obj.get('logo_img', 'logo.png')
        self.logo_video = obj.get('logo_video', 'logo.mp4')
        self.bgm = obj.get('bgm', 'bgm.mp3')
        self.start = parse_time(obj.get('start', 0))
        self.end = parse_time(obj.get('end'))
        self.prev_time = parse_time(obj.get('prev_time', 0))
        self.bias = obj.get('bias', 0.2)
        self.quarter = obj.get('quarter')
        self.intro = obj.get('intro')
        self.narrator = obj.get('narrator', '云说')
        self.events = [Event('start', self.start, self.start)] + Event.load_from_csv(f'events.{match_id}.csv') + [Event('end', self.end, self.end)]
        self.comments = []
        self.score_updates = []
        self.scoreboard = Scoreboard.from_dict(
            {'title': self.name, 'team0': self.teams[0].code, 'team1': self.teams[1].code, 'quarter': 'Q' + str(self.quarter)}, 
            obj['scoreboard']) if 'scoreboard' in obj else None
        self.score_updates.append(ScoreUpdate(self.start, self.teams[0].score, self.teams[1].score))

    def update_score(self, time, team=None, score=None):
        if team is not None:
            self.teams[team].score = score
        self.score_updates.append(ScoreUpdate(time, self.teams[0].score, self.teams[1].score))

    def game_time(self, time):
        return time - self.start + self.prev_time

class ScoreUpdate:
    def __init__(self, time, score0, score1):
        self.time = time
        self.score0 = score0
        self.score1 = score1

    def __repr__(self):
        return f"time: {self.time}, score0: {self.score0}, score1: {self.score1}"
