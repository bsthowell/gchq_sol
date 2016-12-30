#!/usr/bin/env python
import curses
from constants import *
import graphics 
import util

################################ GLOBAL VARIABLES

LEVEL_PROGRESS = [0 for _ in range(NUM_CELLS+1)]
SOLUTION = []
TOTAL_PROGRESS = 0

################################ GENERATE ROW PERMUTATIONS

def contains(perm, starting_col):
	for i in range(len(perm)):
		if starting_col[i] and not perm[i]:	return False
	return True

def distribute_zeroes(extra_zeroes, num_buckets):
	if num_buckets == 1: return [[extra_zeroes]]
	perms = []
	for i in range(extra_zeroes+1):
		for perm in distribute_zeroes(extra_zeroes - i, num_buckets - 1):
			perms.append([i] + perm) 
	return perms

def gen_row_perms(i):
	row = row_constraints[i]
	starting_row = starting_rows[i]
	perms = []
	zeroes_added = len(row)-1
	new_length = sum(row) + zeroes_added
	extra_zeroes = NUM_CELLS - new_length
	num_buckets = len(row) + 1
	distributions = distribute_zeroes(extra_zeroes, num_buckets)
	for dist in distributions:
		perm = [0]*dist[0] + [1]*row[0]
		for i in range(1,len(row)):
			perm += [0]*dist[i] + [0] + [1]*row[i]
		perm += [0]*dist[-1]
		if contains(perm, starting_row): perms.append(perm)
	return perms

################################ VERIFY ROW PERMUTATIONS

def aggregate(row):
	aggregated = []
	count = 0;
	for z in range(len(row)):
		if (row[z] == 0 and count != 0): 
			aggregated.append(count)
			#!
			aggregated.append(0)
			#!
			count = 0
		else: count += row[z]
	if count != 0: aggregated.append(count)
	return aggregated


def col_satisfies(limited, constraint):
	aggregated = aggregate(limited)
	length = len(aggregated)
	if (len(aggregated) > 2*len(constraint)): return False
	if(length > 0):
		last = aggregated[-1]
		if (last > 0) and (last > constraint[(length-1)/2]): return False
	for i in range(len(aggregated)/2):
		if aggregated[2*i] != constraint[i]: return False
	return True

def satisfies(i, arr):
	for j in range(NUM_CELLS-1):
		col = [row[j] for row in arr]
		limited = col
		constraint = col_constraints[j]
		if not col_satisfies(limited, constraint): return False
	return True

def check_correctness(arr):
	global SOLUTION
	result = satisfies(NUM_CELLS, arr)
	if result:
		SOLUTION = arr
	return result


################################ RECURSIVE BACKTRACKING ALGORITHM

def recurse(i, arr, stdscreen):
	LEVEL_PROGRESS[i] += 1
	graphics.update_screen(stdscreen, arr, TOTAL_PROGRESS, LEVEL_PROGRESS)
	if i==NUM_CELLS:
		if check_correctness(arr): return True
	if not satisfies(i, arr): return False
	perms = gen_row_perms(i)
	for perm in perms:
		if recurse(i+1, arr + [perm], stdscreen): return True
		global TOTAL_PROGRESS
		TOTAL_PROGRESS += util.product(num_each_row_perms[i+1:])


################################ MAIN

def main(stdscreen):
	stdscreen.refresh()
	recurse(0,[], stdscreen)

if __name__=='__main__':
	curses.wrapper(main)
	print SOLUTION
