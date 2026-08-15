# sound_manager.py - Loads and plays chess sound effects.
#
# Every .mp3 is loaded ONCE, at construction, from an absolute path
# built off this file's own location (so it works no matter what
# directory the game is launched from). play() just triggers an
# already-loaded pygame.mixer.Sound - no file I/O happens during
# gameplay.
#
# All SFX play through one dedicated mixer channel. Before playing a
# new sound, that channel is stopped first, so a fast sequence of
# moves/clicks never stacks overlapping or lingering audio - the
# newest event's sound always wins immediately.
#
# If the mixer can't initialize (no audio device) or a sound file is
# missing/corrupt, that one sound (or all of them) is silently skipped
# instead of crashing the game.

import os
import pygame

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Reserve one mixer channel purely for gameplay SFX.
SFX_CHANNEL_ID = 0


class SoundManager:

    FILENAMES = {
        "move": "move.mp3",
        "capture": "capture.mp3",
        "castle": "castle.mp3",
        "promotion": "promotion.mp3",
        "check": "check.mp3",
        "game_over": "game_over.mp3",
        "illegal": "illegal.mp3",
    }

    def __init__(self, folder=None):

        self.enabled = True
        self.sounds = {}
        self.channel = None

        if folder is None:
            folder = os.path.join(BASE_DIR, "assets", "sounds")

        if pygame.mixer.get_init() is None:

            try:
                pygame.mixer.init()
            except pygame.error:
                self.enabled = False
                return

        for name, filename in self.FILENAMES.items():

            path = os.path.join(folder, filename)

            if not os.path.isfile(path):
                continue

            try:
                self.sounds[name] = pygame.mixer.Sound(path)
            except pygame.error:
                # Corrupt or unsupported file - skip just this one.
                continue

        try:
            self.channel = pygame.mixer.Channel(SFX_CHANNEL_ID)
        except pygame.error:
            # No dedicated channel available - fall back to sound.play()
            # in play(), which can't pre-empt itself but still works.
            self.channel = None

    def play(self, name):
        """
        Play a loaded sound by name, replacing whatever SFX is
        currently playing. No-op if the sound is missing or audio is
        disabled.
        """

        if not self.enabled:
            return

        sound = self.sounds.get(name)

        if sound is None:
            return

        if self.channel is not None:
            self.channel.stop()
            self.channel.play(sound)
        else:
            sound.play()