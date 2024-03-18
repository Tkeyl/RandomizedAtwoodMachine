#!/usr/bin/env python
# coding: utf-8


from RAMachine_FinalVersion import *


chosen_vars, randomized_vars, solved_for_vars = RAMachine ()


####### printing out returned dictionary #########################
print(f'chosen_vars = {chosen_vars}')
print(f'randomized_vars = {randomized_vars}')
print(f'solved_for_vars = {solved_for_vars}')
print('\n')

####### grabbing a dictionary entry and assigning it to a variable ####
randomized_v0 = randomized_vars[rand_v0]
print(f'randomized_v0 = {randomized_v0}')
