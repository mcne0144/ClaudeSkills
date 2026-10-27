"""Faceless engine: deterministic parts of the faceless YouTube pipeline.

Standard library plus requests, Pillow and ffmpeg. Judgment steps (topic choice,
script point of view, review) are done by the scheduled Claude routines in
routines/, which call these verbs through faceless.py.
"""
