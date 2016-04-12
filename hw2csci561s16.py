import sys
import copy
#initial variable

standardize_variable_counter = 0
# divide all the predicate into callAtomic include name and args args is a list
'''
the first section is build up the data structure to store the information
'''
class Atomic:
    def __init__ (self,name,args):
        self.name = name
        self.args = args
#funtion
def create_atomic(query_clause):
    name= query_clause.split('(')[0]
    args_part = query_clause.split('(')[1]
    args_part = args_part.split(')')[0]
    args = args_part.split(', ')
    atomic_class = Atomic(name,args)
    return atomic_class

def build_map(kb_sentence):
    global kb_search_map
    sentence_array= kb_sentence.split(' => ')
    if len(sentence_array) == 1:
        rhs = create_atomic(sentence_array[0])
        lhs = []
    else:
        conjunction_list = sentence_array[0].split(' && ')
        rhs = create_atomic(sentence_array[1])
        lhs = []
        for i in range(len(conjunction_list)):
            lhs.append(create_atomic(conjunction_list[i]))

    sentence_list = []
    sentence_list.append(rhs)
    sentence_list.append(lhs)
    kb_search_map.setdefault(rhs.name,[]).append(sentence_list)

##################################################################################################
# the first step of program need to translate the query in to goals
# return the goal in atomic format

def initital_goals(query_sentence):
    query_arr = query_sentence.split(' && ')
    initital_goals = []
    for i in range(len(query_arr)):
        initital_goals.append(create_atomic(query_arr[i]))
    return initital_goals


def fetch_rules_for_goal(kb_map, goal):
    if not kb_map.has_key(goal.name):
        return None
    else:
        return kb_map[goal.name]


def is_var(args):
    """Judge if s is a variable"""
    return args[0].islower()


def is_const(s = ''):
    """Judge if s is a constant"""
    return not is_var(s)

// replace the var with new var name to prevent dumplicate name
def standardize_variables(temp_rule):
    rule = copy.deepcopy(temp_rule)
    global standardize_variable_counter
    record_map = {}
    for i in range(len(rule[0].args)):
        if is_var(rule[0].args[i]):
             if rule[0].args[i] not in record_map:
                 v = "v" + str(standardize_variable_counter)
                 record_map[rule[0].args[i]] = v
                 rule[0].args[i] = v
                 standardize_variable_counter += 1
             else:
                  rule[0].args[i] = record_map[rule[0].args[i]]

    for a in range(len(rule[1])):
        for b in range(len(rule[1][a].args)):
            #print rule[1][a].args
            if is_var(rule[1][a].args[b]):
                if rule[1][a].args[b] not in record_map:
                    v = "v" + str(standardize_variable_counter)
                    record_map[rule[1][a].args[b]] = v
                    rule[1][a].args[b] = v
                    standardize_variable_counter += 1
                else:
                    rule[1][a].args[b] = record_map[rule[1][a].args[b]]
    return rule

    '''
    print rule[0].args
    print rule[1][0].args
    print rule[1][1].args
    print rule[1][2].args
    print rule[1][3].args
    '''


## define the unify function to unify rhs and goal

def unify_var(var,val,theta):
    if theta.has_key(var):
        return unify(theta[var],val, theta)
    elif theta.has_key(val):
        return unify(var,theta[val],theta)
    else:
        new_theta = copy.deepcopy(theta)
        new_theta[var] = val
        return new_theta

#x,y, should be args, find the mapping
def unify(rhs, goal, theta):
    if theta is None:
        return None
    new_theta = theta
    for i in range(len(rhs.args)):
        x = rhs.args[i]
        y = goal.args[i]
        if x == y:
             continue
        elif is_var(x):
            new_theta = unify_var(x,y,new_theta)
        elif is_var(y):
            new_theta = unify_var(y,x,new_theta)
        else:
            new_theta = None
            break
    return new_theta

# define subst funciton : use the current theta to replace the args in goal_atomoic

def subst(theta,tmp_first_goal):
    first_goal = copy.deepcopy(tmp_first_goal) #########
    for i in range(len(first_goal.args)):
        while(theta.has_key(first_goal.args[i])):
                #print first_goal.args[i] + theta[first_goal.args[i]]
           first_goal.args[i] = theta[first_goal.args[i]]

    return first_goal

##print out document

def print_result(type, tmp_atmoic,theta):
    atmoic = subst(theta, tmp_atmoic)
    line = type + ': ' + atmoic.name + '('
    for i in range(len(atmoic.args)):
        if i != 0:
            line = line + ', '
        if is_var(atmoic.args[i]):
            line = line + '_'
        else:
            line = line + atmoic.args[i]
    line = line + ')'+'\n'
    #print line
    output.write(line)

###############################################################################################
#below is the main fol_bc ask
def fol_bc_ask(kb_map, query):
    if(len(query) == 0):
        return "there are no query to do backwarad chaining"
    if(len(query)==1):
        return fol_bc_or(kb_map, query[0],{})
        #print_result('Ask', query[0],theta)
    if(len(query) > 1):
        return fol_bc_and(kb_map, query,{})


def fol_bc_or(kb_map, goal, theta):
    flag = False
    first = True
    print_result('Ask', goal,theta)
    if not kb_map.has_key(goal.name):
        print_result('False', goal,theta)
    rules = fetch_rules_for_goal(kb_map, goal)
    if rules != None:
        for rule in rules:
            standard_rule = standardize_variables(rule)
            lhs = standard_rule[1]
            rhs = standard_rule[0]
            u = unify(rhs,goal,theta)
            if u == None : continue
            if not first:
                print_result('Ask',goal,theta)
            for theta1 in fol_bc_and(kb_map,lhs,u):
                flag = True
                print_result('True', goal,theta1)
                yield theta1
            first = False
        if flag == False:
            print_result('False', goal,theta)

def is_share_common_varialbe(first, rest):
    for atmoic in rest:
        for arg in atmoic.args:
            if is_var(arg) and arg in first.args:
                return True

def fol_bc_and(kb_map,goals,theta):
    if theta is None:
        pass
    elif len(goals) == 0:
        yield theta
    else:
        first,rest = goals[0], goals[1:]
        common_flag = is_share_common_varialbe(first,rest)
        sub_first = subst(theta, first)
        for theta1 in fol_bc_or(kb_map, sub_first, theta):
            is_theta_true= False
            for theta2 in fol_bc_and(kb_map,rest, theta1):
                is_theta_true = True
                yield theta2
            if not common_flag and not is_theta_true:
                break



#get the input file
filename = sys.argv[2]
#filename = "sample05.txt"

output_file_name = 'output.txt'
input_file = open(filename,'r')
output = open(output_file_name, 'w')

query = input_file.readline().strip('\n')
kb_sentence_count= input_file.readline().strip('\n')
knowledge_base = []
for i in range(int(kb_sentence_count)):
    knowledge_base.append(input_file.readline().strip('\n'))
# covert the query to goal

kb_search_map = {}
for i in range(len(knowledge_base)):
    build_map(knowledge_base[i])

bc_goals = initital_goals(query)
t =fol_bc_ask(kb_search_map, bc_goals)

try:
  t.next()
except StopIteration:
    output.write('False')
else:
    output.write('True')

output.close()
input_file.close()

























