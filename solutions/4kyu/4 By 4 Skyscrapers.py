'''In a grid of 4 by 4 squares you want to place a skyscraper in each square with only some clues:

The height of the skyscrapers is between 1 and 4
No two skyscrapers in a row or column may have the same number of floors
A clue is the number of skyscrapers that you can see in a row or column from the outside
Higher skyscrapers block the view of lower skyscrapers located behind them

Can you write a program that can solve this puzzle?

Example:

To understand how the puzzle works, this is an example of a row with 2 clues. Seen from the left side there are 4 buildings visible while seen from the right side only 1:

 4	    	    	    	    	 1

There is only one way in which the skyscrapers can be placed. From left-to-right all four buildings must be visible and no building may hide behind another building:

 4	 1	 2	 3	 4	 1

Example of a 4 by 4 puzzle with the solution:

  	    	    	 1	 2	  
  	  	  	  	  	  
  	  	  	  	  	 2
 1	  	  	  	  	  
  	  	  	  	  	  
  	  	  	 3	  	  

  	  	  	 1	 2	  
  	 2	 1	 4	 3	  
  	 3	 4	 1	 2	 2
 1	 4	 2	 3	 1	  
  	 1	 3	 2	 4	  
  	  	  	 3	  	  

Task:

Finish:
function solvePuzzle(clues)
Pass the clues in an array of 16 items. This array contains the clues around the clock, index:
  	 0	 1	   2	   3	  
 15	  	  	  	  	 4
 14	  	  	  	  	 5
 13	  	  	  	  	 6
 12	  	  	  	  	 7
  	11	10	 9	 8	  
If no clue is available, add value `0`
Each puzzle has only one possible solution
`SolvePuzzle()` returns matrix `int[][]`. The first indexer is for the row, the second indexer for the column. (Python: returns 4-tuple of 4-tuples, Ruby: 4-Array of 4-Arrays)
If you finished this kata you can use your solution as a base for the more challenging kata: 6 By 6 Skyscrapers'''

import numpy as np

#check if n appears more than once in array
def duped(l):
    for e in l:
        if l.count(e) > 1:
            return True
    return False

#find empty square to place number
def find_empty(city):
    for r in range(4):
        for c in range(4):
            if city[r][c]==0:
                return (r,c)
            
#check if clue works with n of skycrapers seen
def check_clue(clue,counter):
    if clue==0:
        return True
    return counter==clue

#check how many skyscrapers can be seen and if they are ok with clues          
def vis(arr,clues):
    l=len(arr)
    a1=0
    a2=0
    counter1=0
    counter2=0
    #count skycrapers visible from the two sides
    for k in range(l):
        if arr[k]>a1:
            a1=arr[k]
            counter1+=1
        if arr[l-k-1]>a2:
            a2=arr[l-k-1]
            counter2+=1
    #if the arr is not filled yet can't count the clues
    if l<4:
        return True
    #check the clues
    return check_clue( clues[0] , counter1 ) and check_clue( clues[1] , counter2 )
        
#check if a n placed is ok with all the clues           
def is_valid(r,c,city,clues):
    #row and column
    row=[ h for h in city[r] if h!=0]
    col=[r[c] for r in city if r[c]!=0]
    #if numbers are duplicate return
    if duped(row) or duped(col):
        return False
    #top right bottom left clues
    tc,rc,bc,lc = [clues[k][c] if k%2==0 else clues[k][r] for k in range(4)]
    #check if all clues work
    return vis(row,(lc,rc)) and vis(col,(tc,bc))
    
#recursive function
def solve(city,clues):
    #find position of empty square
    pos = find_empty(city)
    #if there is no empty square then it's solved
    if not pos:
        return True
    #row and column
    r,c=pos
    #all numbers that you can put in a 4x4
    for n in range(1,5):
        #put number in city
        city[r][c] = n
        #check if it's good
        if is_valid(r,c,city,clues):
            #recursion trigger
            if solve(city,clues):
                return True
        #delete number if it doesn't work cause of backtracking or just not valid
        city[r][c] = 0
    #if no possible solution :
    return False
    
#initial function
def solve_puzzle (clues):
    #list of clues with the last 2 reversed to make indexing easy
    clues = [list(clues[k:k+4]) if k < 5 else list(reversed(clues[k:k+4])) for k in range(0,13,4)] #top right bottom left
    #initialize city matrix
    city=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    #solve
    solve(city,clues)
    return tuple([tuple(a) for a in city])