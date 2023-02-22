from copy import deepcopy as copy
data = input()

def split_tokens(data):
    res = []
    i = 0
    while i < len(data):
        
        if(data[i] == 'λ'):
            res.append(('λ', 0))
        elif(data[i] == '('):
            res.append(('(', 0))
        elif(data[i] == '.'):
            res.append(('.', 0))
        elif(data[i] == ')'):
            res.append((')', 0))
        else:
            str = ''
            j = i
            while j < len(data):
                if data[j] in ['λ', '(', ')', '.', ' ']:
                    break
                str += data[j]
                j+=1
            
            
            if len(str) > 0: 
                res.append((str, 1))
                i = j - 1
        i += 1
    return res
    
def get_identifier(list, pos):
    temp = pos
    result = {
        'type' : 'Name',
        'name' : None,
    }
    
    if temp >= len(list) or list[temp][1] != 1: return False, None, pos
    result['name'] = list[temp][0]
    temp += 1
    
    return True, result, temp
  
def application_expr(list, pos):
    temp = pos
    result = None
    res, result, temp = get_expr_low(list, temp)
    if not res: return False, None, pos
    
    while True:
        res, expr, temp = get_expr_low(list, temp)
        if not res: break
        result = {
            'type' : 'Application',
            'first' : result,
            'second' : expr,
        }
    return True, result, temp
    
def function_expr(list, pos):
    temp = pos
    result = {
        'type' : 'Function',
        'first' : None,
        'second' : None,
    }
    
    if temp >= len(list) or list[temp][0] != 'λ': return False, None, pos
    temp += 1
    
    
    res, result['first'], temp = get_expr(list, temp)
    if not res: return False, None, pos
    
    if temp >= len(list) or list[temp][0] != '.':  return False, None, pos
    temp += 1
    
    res, result['second'], temp = get_expr(list, temp)
    if not res: return False, None, pos
    return True, result, temp

def scope_expr(list, pos):
    temp = pos
    result = None
    if temp >= len(list) or list[temp][0] != '(': return False, None, pos
    temp += 1
    
    res, result, temp = get_expr(list, temp)
    if not res: return False, None, pos
    
    if temp >= len(list) or list[temp][0] != ')': return False, None, pos
    temp += 1
    
    return True, result, temp
    
    
def get_expr_low(list, pos):
    res_, res, temp = get_identifier(list, pos)
    if res_: return res_, res, temp 
    res_, res, temp = function_expr(list, pos)
    if res_: return res_, res, temp 
    res_, res, temp = scope_expr(list, pos)
    if res_: return res_, res, temp 
    return False, None, pos

def get_expr(list, pos):
    res_, res, temp = application_expr(list, pos)
    if res_: return res_, res, temp 
    res_, res, temp = get_expr_low(list, pos)
    if res_: return res_, res, temp 
    return False, None, pos

def set_free(graph, list):
    if(graph['type'] == 'Application'):
        set_free(graph['first'], list)
        set_free(graph['second'], list)
    elif (graph['type'] == 'Function'):
        temp_list = copy(list)
        temp_list.append(graph['first']['name'])
        set_free(graph['first'],temp_list)
        set_free(graph['second'], temp_list)
    elif (graph['type'] == 'Name'):
        graph['free'] = list.count(graph['name'])
    return graph

def re_set_free(graph, list, new_list):
    if(graph['type'] == 'Application'):
        re_set_free(graph['first'], list, new_list)
        re_set_free(graph['second'], list, new_list)
    elif (graph['type'] == 'Function'):
        temp_list = copy(new_list)
        temp_list.append(graph['first']['name'])
        re_set_free(graph['first'], list, temp_list)
        re_set_free(graph['second'], list, temp_list)
    elif (graph['type'] == 'Name'):
        if(graph['name'] in new_list):
            graph['free'] = list.count(graph['name']) + new_list.count(graph['name'])
    return graph

def un_set_free(graph, list):
    if(graph['type'] == 'Application'):
        un_set_free(graph['first'], list)
        un_set_free(graph['second'], list)
    elif (graph['type'] == 'Function'):
        temp_list = copy(list)
        temp_list.append(graph['first']['name'])
        un_set_free(graph['first'], temp_list)
        un_set_free(graph['second'], temp_list)
    elif (graph['type'] == 'Name'):
        if(graph['name'] in list):
            graph['free'] = 0
    return graph
    

def repalace_graph(graph, argFrom, argTo, list):
    if(graph['type'] == 'Application'):
        graph['first'] = repalace_graph(graph['first'], argFrom ,argTo, list)
        graph['second'] = repalace_graph(graph['second'], argFrom ,argTo, list)
    elif (graph['type'] == 'Function'):
        temp_list = copy(list)
        temp_list.append(graph['first']['name'])
        graph['second'] = repalace_graph(graph['second'], argFrom ,argTo, temp_list)
    elif (graph['type'] == 'Name'):
        if graph['name'] == argFrom['name'] and graph['free'] == argFrom['free']:
            graph = re_set_free(copy(argTo), list, [])
    return graph


def find_graph(graph, list):
    if(graph['type'] == 'Application'):
        graph['first'] = find_graph(graph['first'], list)
        if(graph['first']['type'] == 'Function'):
            graph['second'] = un_set_free(graph['second'], [])
            graph = repalace_graph(graph ['first']['second'], graph['first']['first'], graph['second'], list)
            return find_graph(graph, list)
        graph['second'] = find_graph(graph['second'], list)
    elif(graph['type'] == 'Function'):
        temp_list = copy(list)
        temp_list.append(graph['first']['name'])
        graph['second'] = find_graph(graph['second'], temp_list)
    return graph
    
def print_graph(graph):
    if(graph['type'] == 'Application'):
        s = ''
        if(graph['first']['type'] != 'Name'):
            s += '('
            s += print_graph(graph['first'])
            s += ')'
        else:
            s += print_graph(graph['first'])
        s += ' '
        if(graph['second']['type'] != 'Name'):
            s += '('
            s += print_graph(graph['second'])
            s += ')'
        else:
            s += print_graph(graph['second'])
        return s
    elif(graph['type'] == 'Function'):
        s = 'λ'
        s += print_graph(graph['first'])
        s += '.'
        s += print_graph(graph['second'])
        return s
    elif(graph['type'] == 'Name'):
        return graph['name']
    

list = split_tokens(data)
print(list)
graph = get_expr(list,0)[1]
print(graph)
graph = set_free(graph, [])
print(print_graph(graph))
graph = find_graph(graph, [])
print(print_graph(graph))