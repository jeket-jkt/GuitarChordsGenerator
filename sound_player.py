import pygame
from pathlib import Path
import threading
import time

class SoundPlayer:
    def __init__(self, samples_path: Path = None):
        if samples_path is None:
            samples_path = Path("data") / "samples"
        self.samples_path = Path(samples_path)
        try:
            pygame.mixer.init()
            self.available = True
        except Exception:
            self.available = False
        self._thread = None
        self._stop_flag = threading.Event()
        self._patterns = self._build_patterns()

    def _normalize_name(self, chord_name: str):
        return chord_name.strip().replace(" ", "")

    def _map_flat_to_sharp(self, name: str):
        if len(name) >= 2 and name[1] == 'b':
            mapping = {'Db': 'C#','Eb':'D#','Gb':'F#','Ab':'G#','Bb':'A#'}
            base = name[:2]
            rest = name[2:]
            if base in mapping:
                return mapping[base] + rest
        return name

    def _sample_file_for(self, chord_name: str):
        name = self._normalize_name(chord_name)
        name = self._map_flat_to_sharp(name)
        candidates = [
            self.samples_path / f"{name}.wav",
            self.samples_path / f"{name}.ogg",
            self.samples_path / f"{name.lower()}.wav",
            self.samples_path / f"{name.upper()}.wav"
        ]
        for p in candidates:
            if p.exists():
                return p
        return None

    def has_sample_for(self, chord_name: str) -> bool:
        return self._sample_file_for(chord_name) is not None

    def _build_patterns(self):
        # каждый паттерн — список шагов длиной 8 (восьмые)
        # 'D' — down (более громкий удар), 'U' — up (тише), 'x' — пауза
        return {
            'Down-Up': ['D','U','D','U','D','U','D','U'],
            'Rock':    ['D','x','D','U','D','x','D','U'],
            'Ballad':  ['D','x','x','U','D','x','x','U'],
            'Gallop':  ['D','D','U','D','D','U','D','U'],
            'Shuffle': ['D','x','U','D','x','U','D','x'],
            'Palm Mute': ['D','x','D','x','D','x','D','x']
        }

    def play_chord(self, chord_name: str, volume=1.0, mute=False):
        if not self.available:
            return False
        p = self._sample_file_for(chord_name)
        if not p:
            return False
        try:
            snd = pygame.mixer.Sound(str(p))
            vol = max(0.0, min(1.0, volume * (0.4 if mute else 1.0)))
            snd.set_volume(vol)
            snd.play()
            return True
        except Exception:
            return False

    def play_progression(self, chord_list, rhythm='Down-Up', bpm=100, delay_between_chords=0.0):
        if self._thread and self._thread.is_alive():
            return
        self._stop_flag.clear()
        pattern = self._patterns.get(rhythm, self._patterns['Down-Up'])
        steps = len(pattern)
        beat = 60.0 / bpm
        step_duration = beat / (steps / 4.0)  # шагов на такт: если steps=8 -> step_duration=beat/2 (восьмая)
        def runner():
            for chord in chord_list:
                if self._stop_flag.is_set():
                    break
                for step in pattern:
                    if self._stop_flag.is_set():
                        break
                    if step == 'D':
                        self.play_chord(chord, volume=1.0, mute=(rhythm=='Palm Mute'))
                    elif step == 'U':
                        self.play_chord(chord, volume=0.6, mute=(rhythm=='Palm Mute'))
                    elif step == 'x':
                        pass
                    time.sleep(step_duration)
                if delay_between_chords > 0:
                    time.sleep(delay_between_chords)
        self._thread = threading.Thread(target=runner, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_flag.set()
        try:
            pygame.mixer.stop()
        except Exception:
            pass