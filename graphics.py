#!/usr/bin/env python
##### GRAPHICS
from constants import *

def update_screen(stdscreen, arr, TOTAL_PROGRESS, LEVEL_PROGRESS):
	stdscreen.erase()
	stdscreen.border(0)
	draw_progress(stdscreen, TOTAL_PROGRESS, LEVEL_PROGRESS)
	draw_arr(arr, stdscreen, LEVEL_PROGRESS)
	stdscreen.refresh()

def draw_progress(stdscreen, TOTAL_PROGRESS, LEVEL_PROGRESS):
	total_percent = float(TOTAL_PROGRESS)/num_row_perms[-1]
	stdscreen.addstr(2,2, "Approximate Total progress: " + format(total_percent, "%"))
	for level in range(len(LEVEL_PROGRESS)):
		progress = LEVEL_PROGRESS[level]
		percent = float(progress)/num_row_perms[level]
		stdscreen.addstr(level + 4, 2, 
							"# examined at level " + str(level) + ": \t" + str(progress) +
																	"\t\tPercent of total: " + format(percent, "%"))

def draw_arr(arr, stdscreen, LEVEL_PROGRESS):
	first_line = len(LEVEL_PROGRESS) + 4 + 1
	for i in range(len(arr)):
		row = arr[i]
		row_string = " ".join([str(elem) for elem in row])
		stdscreen.addstr(first_line + i, 2, row_string)