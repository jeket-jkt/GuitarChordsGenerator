import json
import random
from pathlib import Path

NOTE_NAMES_SHARP = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
NOTE_TO_INT = {n:i for i,n in enumerate(NOTE_NAMES_SHARP)}
INT_TO_NOTE = {i:n for n,i in NOTE_TO_INT.items()}

MAJOR_SCALE_STEPS = [0, 2, 4, 5, 7, 9, 11]
MINOR_SCALE_STEPS = [0, 2, 3, 5, 7, 8, 10]

def triad_quality(root_int, third_int, fifth_int):
    third = (third_int - root_int) % 12
    fifth = (fifth_int - root_int) % 12
    if third == 4 and fifth == 7:
        return ''
    if third == 3 and fifth == 7:
        return 'm'
    if third == 3 and fifth == 6:
        return 'dim'
    return ''

def int_to_note_name(i):
    return INT_TO_NOTE[i % 12]

class ChordGenerator:
    def __init__(self, chords_file: Path = None):
        if chords_file is None:
            chords_file = Path("data/chords.json")
        self.chords_file = Path(chords_file)
        self._load_list()
        self.circle_of_fifths = self._build_circle_of_fifths()
        self.common_patterns = {
            "I-IV-V": ["I", "IV", "V"],
            "I-vi-IV-V": ["I","vi","IV","V"],
            "ii-V-I": ["ii","V","I"],
            "I–IV–I–V–IV–I": ["I","IV","I","V","IV","I"]
        }

    def _load_list(self):
        try:
            with self.chords_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                self.chords_list = [s.strip() for s in data if isinstance(s, str)]
            else:
                self.chords_list = []
        except:
            self.chords_list = []

    def _build_circle_of_fifths(self):
        circle = []
        cur = NOTE_TO_INT['C']
        seen = set()
        for _ in range(12):
            circle.append(int_to_note_name(cur))
            seen.add(cur)
            cur = (cur + 7) % 12
            if cur in seen:
                break
        return circle

    def diatonic_triads(self, key: str, scale: str = 'major'):
        key = key.strip().replace('b','').replace('♭','')
        root = NOTE_TO_INT.get(key.upper())
        if root is None:
            if len(key) > 1 and key[1] == 'b':
                base = key[0].upper()
                alt = base + '#'
                root = NOTE_TO_INT.get(alt)
            else:
                raise ValueError("Bad key")
        steps = MAJOR_SCALE_STEPS if scale == 'major' else MINOR_SCALE_STEPS
        degrees = [(root + s) % 12 for s in steps]
        triads = []
        for i in range(7):
            r = degrees[i]
            third = degrees[(i+1) % 7]
            fifth = degrees[(i+2) % 7]
            q = triad_quality(r, third, fifth)
            triads.append(int_to_note_name(r) + q)
        return triads

    def roman_to_chord(self, roman: str, key: str, scale='major'):
        triads = self.diatonic_triads(key, scale=scale)
        roman_map = {
            'I':0,'II':1,'III':2,'IV':3,'V':4,'VI':5,'VII':6,
            'i':0,'ii':1,'iii':2,'iv':3,'v':4,'vi':5,'vii':6
        }
        base = roman
        for idx,ch in enumerate(roman):
            if not ch.isalpha():
                base = roman[:idx]
                break
        base = base.upper()
        idx = roman_map[base]
        return triads[idx]

    def progression_from_pattern(self, pattern_key: str, key: str, scale='major'):
        pattern = self.common_patterns.get(pattern_key)
        return [self.roman_to_chord(r, key, scale) for r in pattern]

    def random_walk_on_circle(self, length=4, start=None, direction='fifths', jump_prob=0.2):
        circle = self.circle_of_fifths[:]
        if direction == 'fourths':
            circle = circle[::-1]
        if start is None:
            cur_idx = random.randrange(len(circle))
        else:
            try:
                cur_idx = circle.index(start)
            except:
                cur_idx = random.randrange(len(circle))
        result = []
        for _ in range(length):
            if random.random() < jump_prob:
                cur_idx = random.randrange(len(circle))
            result.append(circle[cur_idx])
            step = random.choice([1,1,-1])
            cur_idx = (cur_idx + step) % len(circle)
        return result

    def generate_by_rules(self, key='C', scale='major', length=4):
        triads = self.diatonic_triads(key, scale=scale)
        transition = {
            0:[0,1,3,4,5],
            1:[4,0,2],
            2:[5,0],
            3:[0,4,1],
            4:[0,5,3],
            5:[0,3,4],
            6:[0,1]
        }
        current = 0
        progression = []
        for _ in range(length):
            progression.append(triads[current])
            choices = transition.get(current,[0])
            current = random.choice(choices)
        return progression

    def get_random_chord(self):
        if self.chords_list:
            return random.choice(self.chords_list)
        return random.choice(self.circle_of_fifths)

    def get_progression(self, mode='rules', **kwargs):
        key = kwargs.get('key','C')
        scale = kwargs.get('scale','major')
        length = kwargs.get('length',4)
        if mode == 'pattern':
            return self.progression_from_pattern(kwargs.get('pattern_key','I-vi-IV-V'), key, scale)
        if mode == 'circle_walk':
            return self.random_walk_on_circle(length=length, start=kwargs.get('start'), direction=kwargs.get('direction','fifths'))
        if mode == 'diatonic':
            return self.diatonic_triads(key, scale=scale)
        return self.generate_by_rules(key=key, scale=scale, length=length)

    def get_chord_list(self):
        return list(self.chords_list)