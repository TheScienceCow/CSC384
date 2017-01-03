#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the hitori models.  

'''
Construct and return hitori CSP models.
'''

from cspbase import *
import itertools

def hitori_csp_model_1(initial_hitori_board):
    '''Return a CSP object representing a hitori CSP problem along 
       with an array of variables for the problem. That is return

       hitori_csp, variable_array

       where hitori_csp is a csp representing hitori using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the hitori board (indexed from (0,0) to (8,8))

       
       
       The input board is specified as a list of n lists. Each of the
       n lists represents a row of the board. Each item in the list 
       represents a cell, and will contain a number between 1--n.
       E.g., the board
    
       -------------------  
       |1|3|4|1|
       |3|1|2|4|
       |2|4|2|3|
       |1|2|3|2|
       -------------------
       would be represented by the list of lists
       
       [[1,3,4,1],
       [3,1,2,4],
       [2,4,2,3],
       [1,2,3,2]]
       
       This routine returns Model_1 which consists of a variable for
       each cell of the board, with domain equal to {0,i}, with i being
       the initial value of the cell in the board. 
       
       Model_1 also contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.)
       
       All of the constraints of Model_1 MUST BE binary constraints 
       (i.e., constraints whose scope includes exactly two variables).
    '''
    #Initialize variables
    hitori_csp = CSP("Model_1")
    length = len(initial_hitori_board)
    variable_array = [[None for i in range(length)] for j in range(length)]

    for i in range(length):
      for j in range(length):
        #For each tile, add the variable into variable_array and to the csp object
        var = Variable("Var "+str(i)+","+str(j), [0, initial_hitori_board[i][j]])
        variable_array[i][j] = (var)
        hitori_csp.add_var(var)

    for var in hitori_csp.get_all_vars():
        row = int(var.name[4:].split(",")[0])
        col = int(var.name[4:].split(",")[1])
        for var2 in hitori_csp.get_all_vars():
              row2 = int(var2.name[4:].split(",")[0])
              col2 = int(var2.name[4:].split(",")[1])
              #For each pair of variables on the grid, if they are in the same row or column but not the same variable
              if (var is not var2) and ((row == row2) or (col ==col2)):
                c = Constraint(var.name + "," + var2.name, [var,var2])
                #Generate all sat_tuples
                sat_tuples = []
                for val in var.domain():
                  for val2 in var2.domain():
                    #Both black and not adjacent
                    if val == 0 and val2 == 0 and (abs(row - row2) != 1 and abs(col - col2) != 1):
                      sat_tuples.append([val,val2])
                    elif val != val2:
                      sat_tuples.append([val,val2])
                c.add_satisfying_tuples(sat_tuples)
                hitori_csp.add_constraint(c)
    
    return hitori_csp, variable_array

##############################

def hitori_csp_model_2(initial_hitori_board):
    '''Return a CSP object representing a hitori CSP problem along 
       with an array of variables for the problem. That is return

       hitori_csp, variable_array

       where hitori_csp is a csp representing hitori using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the hitori board (indexed from (0,0) to (8,8))

       
       
       The input board is specified as a list of n lists. Each of the
       n lists represents a row of the board. Each item in the list 
       represents a cell, and will contain a number between 1--n.
       E.g., the board
    
       -------------------  
       |1|3|4|1|
       |3|1|2|4|
       |2|4|2|3|
       |1|2|3|2|
       -------------------
       would be represented by the list of lists
       
       [[1,3,4,1],
       [3,1,2,4],
       [2,4,2,3],
       [1,2,3,2]]

       The input board takes the same input format (a list of n lists 
       specifying the board as hitori_csp_model_1).
   
       The variables of model_2 are the same as for model_1: a variable
       for each cell of the board, with domain equal to {0,i}, where i is
       the initial value of the cell.

       However, model_2 has different constraints.  In particular, instead
       of binary not-equals constraints, model_2 has 2n n-ary constraints
       that resemble a modified all-different constraint.  Each constraint
       is over n variables.  For any given row (resp. column), that 
       constraint will incorporate both the adjacent black squares and 
       no repeated numbers rules.
       
    '''
    #Same as above
    hitori_csp = CSP("Model_2")
    length = len(initial_hitori_board)
    variable_array = [[None for i in range(length)] for j in range(length)]

    for i in range(length):
      for j in range(length):
        var = Variable("Var "+str(i)+","+str(j), [0, initial_hitori_board[i][j]])
        variable_array[i][j] = (var)
        hitori_csp.add_var(var)

    #Constraints for columns
    for row in range(length):
        c = Constraint("Row " + str(row), variable_array[row])
        sat_tuples = n_ary_constraints_tuples(variable_array[row])
        c.add_satisfying_tuples(sat_tuples)
        hitori_csp.add_constraint(c)

    #Constraints for rows
    for col in range(len(initial_hitori_board)):
        col_vars = [row[col] for row in variable_array]
        c = Constraint("Column " + str(col), col_vars)
        sat_tuples = n_ary_constraints_tuples(col_vars)
        c.add_satisfying_tuples(sat_tuples)
        hitori_csp.add_constraint(c)

    return hitori_csp, variable_array

def no_neighbouring_blacks(l):
  for i in range(len(l) - 1):
    if (l[i] == 0 and l[i + 1] == 0):
      return False
  return True

def no_duplicate_numbers(l):
  for i in range(len(l) - 1):
    if l[i] != 0 and l[i] in l[i + 1:]:
      return False
  return True
    
def n_ary_constraints_tuples(vars):
    domain_list = []
    for var in vars:
      domain_list.append(var.domain())
    #Find all combinations possible
    tups_list = list(itertools.product(*domain_list))
    #Turn tuples into lists
    tups_list = [list(ele) for ele in tups_list]
    #Delete duplicate lists
    tups_list.sort()
    tups_list = list(tups_list for tups_list,_ in itertools.groupby(tups_list))
    #Delete lists with neighbouring black tiles and duplicate numbers
    tups_list = [x for x in tups_list if (no_neighbouring_blacks(x))]
    tups_list = [x for x in tups_list if (no_duplicate_numbers(x))]
    
    return tups_list
