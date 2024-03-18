#!/usr/bin/env python
# coding: utf-8

# In[7]:


import sympy
import random
from IPython.display import SVG, display


# In[19]:


########## setting variables as symbols for returned dictionaries ##############################
grav_a, v0_min, v0_max, m1_max, m2_max, L_max = sympy.symbols('grav_a, v0_min, v0_max, m1_max, m2_max, L_max')
rand_v0, rand_x0, rand_m1, rand_m2, string_L, inst_t = sympy.symbols('rand_v0, rand_x0, rand_m1, rand_m2, string_L, inst_t')
sol_a, sol_tmax, inst_v, inst_x, m1_min, m2_min = sympy.symbols('sol_a, sol_tmax, inst_v, inst_x, m1_min, m2_min')


def RAMachine():
    
    ########## setting variables as symbols ##############################
    v0, x0, m1, m2, a, tmax = sympy.symbols('v0, x0, m1, m2, a, tmax')

    ########## randomized dictionary #####################################
    randomizer = {
        v0: lambda: random.uniform(v0min, v0max),
        x0: lambda: random.uniform(0, L), 
        m1: lambda: random.uniform(m1min, m1max), 
        m2: lambda: random.uniform(m2min, m2max), 
    }
    

    
    ########## input planetary gravitation ###############################
    g = None
    while g is None or g <=0:
        try:
            g = float(input("What planet are we on? \nInput the planet's acceleration due to gravity as a positive number: "))
            if g <= 0:
                print("Incorrect input type. Try again.\n")
        except:
            print("Incorrect input type. Try again.\n")   
    print("\n")
    
    ########## input ranges ##############################################
    v0min = None
    while v0min is None:
        try:
            v0min = float(input("Input a minimum value for the initial velocity: "))
        except:
            print("Incorrect input type. Try again.\n")
  
    v0max = None
    while v0max is None or v0max <=v0min:
        try:
            v0max = float(input("Input a maximum value for the initial velocity: "))
            if v0max <=v0min:
                print("Incorrect input type. Try again.\n")
        except:
            print("Incorrect input type. Try again.\n")      
    
    m1min = None
    while m1min is None or m1min <=0:
        try:
            m1min = float(input("Input a minimum value for the left mass as a positive number: "))
            if m1min <= 0:
                print("Incorrect input type. Try again.\n")
        except:
            print("Incorrect input type. Try again.\n")   
    
    m1max = None
    while m1max is None or m1max <=m1min:
        try:
            m1max = float(input("Input a maximum value for the left mass as a positive number: "))
            if m1max <=0:
                print("Incorrect input type. Try again.\n")
        except:
            print("Incorrect input type. Try again.\n")   
    
    m2min = None
    while m2min is None or m2min <=0:
        try:
            m2min = float(input("Input a minimum value for the right mass as a positive number: "))
            if m2min <= 0:
                print("Incorrect input type. Try again.\n")
        except:
            print("Incorrect input type. Try again.\n")   
    
    m2max = None
    while m2max is None or m2max <=m2min:
        try:
            m2max = float(input("Input a maximum value for the right mass as a positive number: "))
            if m2max <=0:
                print("Incorrect input type. Try again.\n")
        except:
            print("Incorrect input type. Try again.\n")   
    
    Lmax = None
    while Lmax is None or Lmax <=0:
        try:
            Lmax = float(input("Input a maximum value for the string length as a positive number: "))
            if Lmax <=0:
                print("Incorrect input type. Try again.\n")
        except:
            print("Incorrect input type. Try again.\n")   
    print("\n")
    
    
    
    ######## randomized force equation ####################################
    force_eq = a - g*(m2 - m1)/(m1 + m2)
    

    ######## randomized force function ###################################
    def solve_force_for(solve_var):
        randomized = {}  # Collect randomized variables
        for var in (m1, m2, a):
            if var != solve_var:
                randomized[var] = randomizer[var]()
        result = sympy.solve(force_eq.xreplace(randomized), solve_var)
        force_result = result[0]
        return {solve_var: force_result}, randomized


    ####### solve force function for acceleration ########################
    solution, randomized = solve_force_for(a) 
    solution_a = solution[a]
    randomized_m1 = randomized[m1]
    randomized_m2 = randomized[m2]



    ####### finding random string length ##################################
    L = random.uniform(1, Lmax)


    ####### randomize t_max equation ######################################
    if solution_a < 0:
        tmax_eq_neg = tmax + (v0 + (v0**2 - 2*solution_a*(x0))**.5)/solution_a
        tmax_eq_pos = tmax + (v0 - (v0**2 - 2*solution_a*(x0))**.5)/solution_a
    else: 
        tmax_eq_neg = tmax + (v0 + (v0**2 - 2*solution_a*(x0 - L))**.5)/solution_a
        tmax_eq_pos = tmax + (v0 - (v0**2 - 2*solution_a*(x0 - L))**.5)/solution_a



    ########## randomized t_max function ##################################
    def solve_tmax_for(solve_var):
        randomizedf = {}
        for var in (tmax, v0, x0):
            if var != solve_var:
                randomizedf[var] = randomizer[var]()
        tmax_result_neg = sympy.solve(tmax_eq_neg.xreplace(randomizedf), solve_var)
        tmax_result_pos = sympy.solve(tmax_eq_pos.xreplace(randomizedf), solve_var)
        tmax_result = max(tmax_result_neg[0], tmax_result_pos[0])
        return {solve_var: tmax_result}, randomizedf    



    ######## solve t_max function for t_max ################################
    solutionf, randomizedf = solve_tmax_for(tmax)
    solution_tmax = solutionf[tmax]
    randomized_v0 = randomizedf[v0]
    randomized_x0 = randomizedf[x0]



    ########## finding instantaneous time ###############################
    t = random.uniform(0, solution_tmax)

    ######### finding v with randomized values ##########################
    v = randomized_v0 + solution_a*t

    ######### finding x with randomized values ##########################
    x = randomized_x0 + (randomized_v0)*t + .5*solution_a*t**2
    
    ######### which block hits the pulley for negative accel ############
    tturn = (-randomized_v0)/(solution_a)
    xturn = randomized_x0 + (randomized_v0)*tturn + .5*solution_a*tturn**2
    
    ######## finding the middle of the string for images ################
    Lmid = L/2
    
    
    
    ######## detecting a block hitting the pulley #######################
    if tturn > 0 and xturn >= L:
        x = L
        display(SVG('RAM Img Lhit.svg'))
        print("See svg file: RAM Img Lhit.svg")
        print("Error. Your initial velocity was too large and your negative acceleration not large enough.")
        print("The length of the string was exhausted, the left block collided with the pulley, and the entire")
        print("string-block device was launched from the pulley's track and hurled into your face. Final x = L.")
        print(f"x = {x}")
        print("\n")
        print(f'Solution for tturn: {tturn}')
        print(f'Solution for xturn: {xturn}')
    elif tturn > 0 and xturn < 0:
        display(SVG('RAM Img Rhit.svg'))
        print("See svg file: RAM Img Rhit.svg")
        print("Error. Your initial velocity was too large and your positive acceleration not large enough.")
        print("The length of the string was exhausted, the right block collided with the pulley, and the entire")
        print("string-block device was launched from the pulley's track and hurled into your face. Final x = 0.")
        print("\n")
        print(f'Solution for tturn: {tturn}')
        print(f'Solution for xturn: {xturn}')
    else:
        print("Congratulations! You successfully generated an Atwood's Machine problem.")
        print("Go forth and torture your students with the unwieldy knowledge of physics.")
 



    ######## displaying images ###########################################
    print("\n")
    print("###### INITIAL STATE ########")
    if randomized_x0 < Lmid:
        display(SVG('RAM Img Llower.svg'))
        print("See svg file: RAM Img Llower.svg")
    elif randomized_x0 > Lmid:
        display(SVG('RAM Img Rlower.svg'))
        print("See svg file: RAM Img Rlower.svg")
    else:
        display(SVG('RAMachine image.svg'))
        print("See svg file: RAMachine image.svg")
    
    print("\n")
    print("###### FINAL STATE ########")
    if x < Lmid:
        display(SVG('RAM Img Llower.svg'))
        print("See svg file: RAM Img Llower.svg")
    elif x > Lmid:
        display(SVG('RAM Img Rlower.svg'))
        print("See svg file: RAM Img Rlower.svg")
    else:
        display(SVG('RAMachine image.svg'))
        print("See svg file: RAMachine image.svg")
    
    

    
    ######## printing out all results ####################################
    print("\n")
    print('###### USER CHOSEN VALUES ########\n')
    print(f"Acceleration due to the planet's gravity: g = {g}")
    print(f"Range of masses for the left block: [m1min = {m1min}, m1max = {m1max})")
    print(f"Range of masses for the right block: [m2min = {m2min}, m2max = {m2max})")
    print(f"Range for initial velocity: [v0min = {v0min}, v0max = {v0max})")
    print(f"Range for the length of the string: [1, Lmax = {Lmax})")
    print('\n')
    
    print('###### RANDOMIZED VALUES ########\n')
    print(f'Mass of the left block: randomized_m1 = {randomized_m1}')
    print(f'Mass of the right block: randomized_m2 = {randomized_m2}')
    print(f'Initial velocity: randomized_v0 = {randomized_v0}')
    print(f"Range for initial position: [0, L)")
    print(f'Initial position: randomized_x0 = {randomized_x0}')
    print(f'Length of the string: L = {L}')
    print(f"Range for instantaneous time: [0, solution_tmax)")
    print(f'Instantaneous time: t = {t}')
    print('\n')
    
    print('###### SOLVED VALUES ########\n')
    print(f'Acceleration: solution_a = {solution_a}')
    print(f'Maximum time: solution_tmax = {solution_tmax}')
    print(f'Instantaneous velocity: v = {v}')
    print(f'Instantaneous position: x = {x}')
    print("\n")
        
    
    
    ######## dictionaries for returned variables ###########################
    chosen_vars = {
        grav_a : g,
        v0_min : v0min,
        v0_max : v0max,
        m1_min : m1min,
        m1_max : m1max,
        m2_min : m2min,
        m2_max : m2max,
        L_max : Lmax
    }
    
    randomized_vars = {
        rand_v0 : randomized_v0, 
        rand_x0 : randomized_x0, 
        rand_m1 : randomized_m1, 
        rand_m2 : randomized_m2, 
        string_L : L,
        inst_t : t
        
    }
    
    solved_for_vars = {
        sol_a : solution_a, 
        sol_tmax : solution_tmax,
        inst_v : v, 
        inst_x : x
    }
    
    
    return chosen_vars, randomized_vars, solved_for_vars




#####################################################################
################# CODE ENDS #########################################
#####################################################################


# In[ ]:




