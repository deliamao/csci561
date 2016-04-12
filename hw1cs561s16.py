# csci561

# initiate the basic var
import copy
 hw2cs561s16.p
import os
#initiae
board_score = [[0 for col in range(5)] for row in range(5)]
board_state = [[0 for col in range(5)] for row in range(5)]
col_string =["A","B","C","D","E"]
part2_flag = False

# function
# evaluate function
def evaluate_score(board_score, board_cur_state, player):
    score = 0
    for i in range(5):
            for j in range(5):
                score = score + board_score[i][j] * board_cur_state[i][j]
    if player[0] == 'X':
        return score
    else:
        return -score

# Define the action function to update one the new state
def next_move(i, j, cur_board_state, team_label):
    #print (i,j, team_label)
    raid_flag = False
    raid_flag = raid_flag or ((i - 1 >= 0) and (cur_board_state[i - 1][j] == team_label))
    raid_flag = raid_flag or (i + 1 < 5 and cur_board_state[i + 1][j] == team_label)
    raid_flag = raid_flag or (j - 1 >= 0 and cur_board_state[i][j - 1] == team_label)
    raid_flag = raid_flag or (j + 1 < 5 and cur_board_state[i][j + 1] == team_label)
    if(raid_flag ):# update the status if it is raidFalse
        if i > 0 and i < 4 :
            if cur_board_state[i - 1][j] == -team_label:
                cur_board_state[i - 1][j] = team_label
            if cur_board_state[i + 1][j] == -team_label:
                cur_board_state[i + 1][j] = team_label
        elif i == 0:
            if cur_board_state[i + 1][j] == -team_label:
                cur_board_state[i + 1][j] = team_label
        else:
            if cur_board_state[i - 1][j] == -team_label:
                cur_board_state[i - 1][j] = team_label
        #update the state in col
        if(j > 0 and j < 4):
            if cur_board_state[i][j - 1] == -team_label:
                cur_board_state[i][j - 1]= team_label
            if cur_board_state[i][j + 1] == -team_label:
                cur_board_state[i][j + 1]= team_label
        elif j == 0 :
            if cur_board_state[i][j + 1] == -team_label:
                cur_board_state[i][j + 1] = team_label
        else:
            if cur_board_state[i][j - 1] == -team_label:
                cur_board_state[i][j - 1] = team_label
    # update the status of sneak and final step of raid
    cur_board_state[i][j] = team_label
    return cur_board_state


def is_full(cur_state):
    for i in range(5):
            for j in range(5):
                if(cur_state[i][j] == 0):
                    return False
    return True


def get_pos(i,j):
    return col_string[j] +str(i+1)


def get_traverse_log(pos, depth, value):
    "for traverse log output line"
    if part2_flag: return
    if value == float('inf'): value = 'Infinity'
    elif value ==float('-inf'): value = '-Infinity'
    else: value = str(value)
    line = '\n'+pos + ',' + str(depth) + ',' + value
    output_log.write(line)


def get_alphbet_log(pos,depth,value,alpha,beta):
    if part2_flag: return
    if value == float('inf'): value = 'Infinity'
    elif value ==float('-inf'): value = '-Infinity'
    else: value = str(value)

    if alpha == float('inf'): alpha = 'Infinity'
    elif alpha ==float('-inf'): alpha = '-Infinity'
    else: alpha = str(alpha)

    if beta == float('inf'): beta = 'Infinity'
    elif beta ==float('-inf'): beta = '-Infinity'
    else: beta = str(beta)
    line ='\n'+ pos + ',' + str(depth) + ',' + value + ',' + alpha + ',' + beta
    output_log.write(line)

# greedy_search function
def greedy_search(state, greedy_player):
    if greedy_player[0] == 'X':
        team_label = 1
    elif greedy_player[0] == 'O':
        team_label = -1
    else:
        print "can't recognize the player"
    max_evaluation = float('-inf')
    greedy_max_board_state = copy.deepcopy(state)
    for i in range(5):
        for j in range(5):
            if state[i][j] == 0:
                cur_board_state = copy.deepcopy(state)
                cur_board_state = next_move(i,j,cur_board_state,team_label)
                cur_score = evaluate_score(board_score,cur_board_state,greedy_player)
                if cur_score > max_evaluation:
                    max_evaluation = cur_score
                    greedy_max_board_state =copy.deepcopy(cur_board_state)
    state = greedy_max_board_state
    return state


# mini_max function pos is a string function
def mini_max(begin_depth, depth, state, mini_max_player, pos):
    result = MoveResult(float('-inf'),state)
    if begin_depth >= depth or is_full(state):
        result.node_score = evaluate_score(board_score,state,mini_max_player)
        result.node_state = state
        get_traverse_log(pos, begin_depth, result.node_score)
        return result

    if begin_depth % 2 == 0: # this is the player
        if mini_max_player[0] == 'X':
            team_label = 1
        elif mini_max_player[0] == 'O':
            team_label = -1
        result.node_score = float('-inf')
        get_traverse_log(pos, begin_depth, result.node_score)
        for i in range(5):
            for j in range(5):
                if state[i][j] == 0:
                    cur_board_state = copy.deepcopy(state)
                    cur_board_state = next_move(i,j,cur_board_state,team_label)
                    new_pos =get_pos(i,j)
                    cur_result = mini_max(begin_depth + 1, depth,cur_board_state,mini_max_player,new_pos)
                    if cur_result.node_score > result.node_score:
                        result.node_state = cur_board_state
                        result.node_score = cur_result.node_score
                    get_traverse_log(pos, begin_depth, result.node_score)

    if begin_depth %2 == 1: # this is opponent
        if mini_max_player[0] == 'X':  # oppone
            opp_team_label = -1
        elif mini_max_player[0] == 'O':
            opp_team_label = 1
        result.node_score = float('inf')
        get_traverse_log(pos, begin_depth, result.node_score)
        for i in range(5):
            for j in range(5):
                if state[i][j] == 0:
                    cur_board_state = copy.deepcopy(state)
                    cur_board_state = next_move(i,j,cur_board_state,opp_team_label)
                    new_pos =get_pos(i,j)
                    cur_result = mini_max(begin_depth + 1, depth,cur_board_state,mini_max_player,new_pos)
                    if cur_result.node_score < result.node_score:
                        result.node_state = cur_board_state
                        result.node_score = cur_result.node_score
                    get_traverse_log(pos, begin_depth, result.node_score)
    return result


def alpha_beta(begin_depth,depth,state,alpbet_player, alpha,beta,pos):
    result = MoveResult(float('-inf'),state)
    if begin_depth >= depth or is_full(state):
        result.node_score = evaluate_score(board_score,state,alpbet_player)
        result.node_state = state
        get_alphbet_log(pos, begin_depth, result.node_score,alpha,beta)
        return result

    if begin_depth % 2 == 0:#player x
        result.node_score = float('-inf')
        if alpbet_player[0] == 'X':
            team_label = 1
        elif alpbet_player[0] == 'O':
            team_label = -1
        get_alphbet_log(pos,begin_depth,result.node_score,alpha,beta)
        for i in range(5):
            for j in range(5):
                if state[i][j] == 0:
                    cur_board_state = copy.deepcopy(state)
                    cur_board_state = next_move(i,j,cur_board_state,team_label)
                    new_pos =get_pos(i,j)
                    cur_result = alpha_beta(begin_depth + 1, depth,cur_board_state,alpbet_player,alpha,beta,new_pos)
                    if cur_result.node_score > result.node_score:
                        result.node_state = cur_board_state
                        result.node_score = cur_result.node_score
                    if result.node_score >= beta :
                        get_alphbet_log(pos,begin_depth,result.node_score,alpha,beta)
                        return result
                    if result.node_score > alpha:
                        alpha = result.node_score
                    get_alphbet_log(pos,begin_depth,result.node_score,alpha,beta)

    if begin_depth %2 == 1: # player 0
        if alpbet_player[0] == 'X':  # oppone
            opp_team_label = -1
        elif alpbet_player[0] == 'O':
            opp_team_label = 1
        result.node_score = float('inf')
        get_alphbet_log(pos,begin_depth,result.node_score,alpha,beta)
        for i in range(5):
            for j in range(5):
                if state[i][j] == 0:
                    cur_board_state = copy.deepcopy(state)
                    cur_board_state = next_move(i,j,cur_board_state,opp_team_label)
                    new_pos =get_pos(i,j)
                    cur_result = alpha_beta(begin_depth + 1, depth,cur_board_state,alpbet_player,alpha,beta,new_pos)
                    if cur_result.node_score < result.node_score:
                        result.node_state = cur_board_state
                        result.node_score = cur_result.node_score
                    if result.node_score <= alpha:
                       get_alphbet_log(pos,begin_depth,result.node_score,alpha,beta)
                       return result
                    if result.node_score < beta:
                        beta = result.node_score

                    get_alphbet_log(pos,begin_depth,result.node_score,alpha,beta)


    return result


class MoveResult:
    def __init__ (self,node_score,node_state):
        self.node_score = node_score
        self.node_state = node_state

# mainFunction
filename = sys.argv[2]
input_file = open(filename,'r')
task = int(input_file.readline())
if task != 4:
    player = input_file.readline().strip('\n')
    depth = int(input_file.readline().strip('\n'))
    for i in range(5):
        score_row_string = input_file.readline().strip('\n').split(' ')
        for j in range(5):
            board_score[i][j] = int(score_row_string[j])
    for i in range(5):
        state_row_string = input_file.readline().strip('\n')
        for j in range(5):
            if state_row_string[j] == '*':
                board_state[i][j] = int(0)
            elif state_row_string[j] == 'X':
                board_state[i][j] = 1
            elif state_row_string[j] == 'O':
                board_state[i][j] = -1
    input_file.close()

else:
    first_player = input_file.readline().strip('\n')
    first_player_algorithm =int(input_file.readline().strip('\n'))
    first_player_depth = int(input_file.readline().strip('\n'))
    second_player = input_file.readline().strip('\n')
    second_player_algorithm = int(input_file.readline().strip('\n'))
    second_player_depth = int(input_file.readline().strip('\n'))
    for i in range(5):
        score_row_string = input_file.readline().strip('\n').split(' ')
        for j in range(5):
            board_score[i][j] = int(score_row_string[j])
    for i in range(5):
        state_row_string = input_file.readline().strip('\n')
        for j in range(5):
            # change the board to 0,1,-1 ,occuppied by X mark 1, occuppied by O mark -1, unoccupied mark 0
            if state_row_string[j] == '*':
                board_state[i][j] = int(0)
            elif state_row_string[j] == 'X':
                board_state[i][j] = 1
            elif state_row_string[j] == 'O':
                board_state[i][j] = -1
    input_file.close()

if task == 1:
    board_state = greedy_search(board_state, player)

if task == 2:
    output_log = open('traverse_log.txt', 'w')
    output_log.write('Node,Depth,Value')
    board_state = mini_max(0,depth,board_state,player,'root').node_state
    output_log.close()

if task == 3:
    output_log = open('traverse_log.txt', 'w')
    output_log.write('Node,Depth,Value,Alpha,Beta')
    board_state = alpha_beta(0,depth,board_state,player,float('-inf'), float('inf'),'root').node_state
    output_log.close()
# print output to the next_state.txt
if task != 4:
    next_state = open('next_state.txt', 'w')
    first_line = True
    for i in range(5):
        line = ''
        if first_line == True:
            first_line = False
        else:
            line += '\n'
        for j in range(5):
            if board_state[i][j] == 0:
                line += '*'
            elif board_state[i][j] == 1:
                line += 'X'
            elif board_state[i][j] == -1:
                 line += 'O'
        next_state.write(line)
    next_state.close()

if task == 4:
    part2_flag = True
    next_state = open('trace_state.txt', 'w')
    player1_turn = True
    first_line = True
    war_board_state = copy.deepcopy(board_state)
    while is_full(war_board_state) == False:
        if player1_turn==True:
            player = first_player
            algo = first_player_algorithm
            depth = first_player_depth
        else:
            player = second_player
            algo = second_player_algorithm
            depth = second_player_depth
        if algo == 1:
            war_board_state = greedy_search(war_board_state, player)
        elif algo == 2:
            war_board_state = mini_max(0,depth,war_board_state,player,'root').node_state
        elif algo == 3:
            war_board_state = alpha_beta(0,depth,war_board_state,player,float('-inf'), float('inf'),'root').node_state
        for x in range(5):
            line = ''
            if first_line == False:
                 line += '\n'
            first_line = False
            for y in range(5):
                if war_board_state[x][y] == 0:
                    line += '*'
                elif war_board_state[x][y] == 1:
                    line += 'X'
                elif war_board_state[x][y] == -1:
                    line += 'O'
            next_state.write(line)

        player1_turn = not player1_turn

    next_state.close()














