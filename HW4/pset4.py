# Cody Houff
# sources: https://github.com/pucrs-automated-planning/pddl-parser

import re
import itertools
import sys, time
import random, math, copy
import sys, pprint

class PSet4():

    def solve_pddl(self, domain_file: str, problem_file: str):

        class Action:

            def __init__(self, name, parameters, positive_preconditions, negative_preconditions, add_effects, del_effects, extensions = None):
                def frozenset_of_tuples(data):
                    return frozenset([tuple(t) for t in data])
                self.name = name
                self.parameters = parameters
                self.positive_preconditions = frozenset_of_tuples(positive_preconditions)
                self.negative_preconditions = frozenset_of_tuples(negative_preconditions)
                self.add_effects = frozenset_of_tuples(add_effects)
                self.del_effects = frozenset_of_tuples(del_effects)


            def __str__(self):
                return 'action: ' + self.name + \
                '\n  parameters: ' + str(self.parameters) + \
                '\n  positive_preconditions: ' + str([list(i) for i in self.positive_preconditions]) + \
                '\n  negative_preconditions: ' + str([list(i) for i in self.negative_preconditions]) + \
                '\n  add_effects: ' + str([list(i) for i in self.add_effects]) + \
                '\n  del_effects: ' + str([list(i) for i in self.del_effects]) + '\n'

            def __eq__(self, other): 
                return self.__dict__ == other.__dict__

            def groundify(self, objects, types):
                if not self.parameters:
                    yield self
                    return
                type_map = []
                variables = []
                for var, type in self.parameters:
                    type_stack = [type]
                    items = []
                    while type_stack:
                        t = type_stack.pop()
                        if t in objects:
                            items += objects[t]
                        elif t in types:
                            type_stack += types[t]
                        else:
                            raise Exception('Unrecognized type ' + t)
                    type_map.append(items)
                    variables.append(var)
                for assignment in itertools.product(*type_map):
                    positive_preconditions = self.replace(self.positive_preconditions, variables, assignment)
                    negative_preconditions = self.replace(self.negative_preconditions, variables, assignment)
                    add_effects = self.replace(self.add_effects, variables, assignment)
                    del_effects = self.replace(self.del_effects, variables, assignment)
                    yield Action(self.name, assignment, positive_preconditions, negative_preconditions, add_effects, del_effects)


            def replace(self, group, variables, assignment):
                g = []
                for pred in group:
                    pred = list(pred)
                    iv = 0
                    for v in variables:
                        while v in pred:
                            pred[pred.index(v)] = assignment[iv]
                        iv += 1
                    g.append(pred)
                return g

        #if __name__ == '__main__':
        a = Action('move', [['?ag', 'agent'], ['?from', 'pos'], ['?to', 'pos']],
            [['at', '?ag', '?from'], ['adjacent', '?from', '?to']],
            [['at', '?ag', '?to']],
            [['at', '?ag', '?to']],
            [['at', '?ag', '?from']]
        )
        #print(a)

        objects = {
            'agent': ['ana','bob'],
            'pos': ['p1','p2']
        }
        types = {'object': ['agent', 'pos']}
        #for act in a.groundify(objects, types):
            #print(act)



        class PDDL_Parser:

            SUPPORTED_REQUIREMENTS = [':strips', ':negative-preconditions', ':typing']

            #filename = "blocksworld.pddl"

            def scan_tokens(self, filename):
                with open(filename,'r') as f:
                    # Remove single line comments
                    str = re.sub(r';.*$', '', f.read(), flags=re.MULTILINE).lower()
                # Tokenize
                stack = []
                list = []
                for t in re.findall(r'[()]|[^\s()]+', str):
                    if t == '(':
                        stack.append(list)
                        list = []
                    elif t == ')':
                        if stack:
                            l = list
                            list = stack.pop()
                            list.append(l)
                        else:
                            raise Exception('Missing open parentheses')
                    else:
                        list.append(t)
                if stack:
                    raise Exception('Missing close parentheses')
                if len(list) != 1:
                    raise Exception('Malformed expression')
                return list[0]


            def parse_domain(self, domain_filename):
                tokens = self.scan_tokens(domain_filename)
                if type(tokens) is list and tokens.pop(0) == 'define':
                    self.domain_name = 'unknown'
                    self.requirements = []
                    self.types = {}
                    self.objects = {}
                    self.actions = []
                    self.predicates = {}
                    while tokens:
                        group = tokens.pop(0)
                        t = group.pop(0)
                        if t == 'domain':
                            self.domain_name = group[0]
                        elif t == ':requirements':
                            for req in group:
                                if not req in self.SUPPORTED_REQUIREMENTS:
                                    raise Exception('Requirement ' + req + ' not supported')
                            self.requirements = group
                        elif t == ':constants':
                            self.parse_objects(group, t)
                        elif t == ':predicates':
                            self.parse_predicates(group)
                        elif t == ':types':
                            self.parse_types(group)
                        elif t == ':action':
                            self.parse_action(group)
                        else: self.parse_domain_extended(t, group)
                else:
                    raise Exception('File ' + domain_filename + ' does not match domain pattern')

            def parse_domain_extended(self, t, group):
                print(str(t) + ' is not recognized in domain')

            def parse_hierarchy(self, group, structure, name, redefine):
                list = []
                while group:
                    if redefine and group[0] in structure:
                        raise Exception('Redefined supertype of ' + group[0])
                    elif group[0] == '-':
                        if not list:
                            raise Exception('Unexpected hyphen in ' + name)
                        group.pop(0)
                        type = group.pop(0)
                        if not type in structure:
                            structure[type] = []
                        structure[type] += list
                        list = []
                    else:
                        list.append(group.pop(0))
                if list:
                    if not 'object' in structure:
                        structure['object'] = []
                    structure['object'] += list

            def parse_objects(self, group, name):
                self.parse_hierarchy(group, self.objects, name, False)

            def parse_types(self, group):
                self.parse_hierarchy(group, self.types, 'types', True)

            def parse_predicates(self, group):
                for pred in group:
                    predicate_name = pred.pop(0)
                    if predicate_name in self.predicates:
                        raise Exception('Predicate ' + predicate_name + ' redefined')
                    arguments = {}
                    untyped_variables = []
                    while pred:
                        t = pred.pop(0)
                        if t == '-':
                            if not untyped_variables:
                                raise Exception('Unexpected hyphen in predicates')
                            type = pred.pop(0)
                            while untyped_variables:
                                arguments[untyped_variables.pop(0)] = type
                        else:
                            untyped_variables.append(t)
                    while untyped_variables:
                        arguments[untyped_variables.pop(0)] = 'object'
                    self.predicates[predicate_name] = arguments


            def parse_action(self, group):
                name = group.pop(0)
                if not type(name) is str:
                    raise Exception('Action without name definition')
                for act in self.actions:
                    if act.name == name:
                        raise Exception('Action ' + name + ' redefined')
                parameters = []
                positive_preconditions = []
                negative_preconditions = []
                add_effects = []
                del_effects = []
                extensions = None
                while group:
                    t = group.pop(0)
                    if t == ':parameters':
                        if not type(group) is list:
                            raise Exception('Error with ' + name + ' parameters')
                        parameters = []
                        untyped_parameters = []
                        p = group.pop(0)
                        while p:
                            t = p.pop(0)
                            if t == '-':
                                if not untyped_parameters:
                                    raise Exception('Unexpected hyphen in ' + name + ' parameters')
                                ptype = p.pop(0)
                                while untyped_parameters:
                                    parameters.append([untyped_parameters.pop(0), ptype])
                            else:
                                untyped_parameters.append(t)
                        while untyped_parameters:
                            parameters.append([untyped_parameters.pop(0), 'object'])
                    elif t == ':precondition':
                        self.split_predicates(group.pop(0), positive_preconditions, negative_preconditions, name, ' preconditions')
                    elif t == ':effect':
                        self.split_predicates(group.pop(0), add_effects, del_effects, name, ' effects')
                    else: extensions = self.parse_action_extended(t, group)
                self.actions.append(Action(name, parameters, positive_preconditions, negative_preconditions, add_effects, del_effects, extensions))

            def parse_action_extended(self, t, group):
                print(str(t) + ' is not recognized in action')


            def parse_problem(self, problem_filename):
                def frozenset_of_tuples(data):
                    return frozenset([tuple(t) for t in data])
                tokens = self.scan_tokens(problem_filename)
                if type(tokens) is list and tokens.pop(0) == 'define':
                    self.problem_name = 'unknown'
                    self.state = frozenset()
                    self.positive_goals = frozenset()
                    self.negative_goals = frozenset()
                    while tokens:
                        group = tokens.pop(0)
                        t = group.pop(0)
                        if t == 'problem':
                            self.problem_name = group[0]
                        elif t == ':domain':
                            if self.domain_name != group[0]:
                                raise Exception('Different domain specified in problem file')
                        elif t == ':requirements':
                            pass # Ignore requirements in problem, parse them in the domain
                        elif t == ':objects':
                            self.parse_objects(group, t)
                        elif t == ':init':
                            self.state = frozenset_of_tuples(group)
                        elif t == ':goal':
                            positive_goals = []
                            negative_goals = []
                            self.split_predicates(group[0], positive_goals, negative_goals, '', 'goals')
                            self.positive_goals = frozenset_of_tuples(positive_goals)
                            self.negative_goals = frozenset_of_tuples(negative_goals)
                        else: self.parse_problem_extended(t, group)
                else:
                    raise Exception('File ' + problem_filename + ' does not match problem pattern')

            def parse_problem_extended(self, t, group):
                print(str(t) + ' is not recognized in problem')


            def split_predicates(self, group, positive, negative, name, part):
                if not type(group) is list:
                    raise Exception('Error with ' + name + part)
                if group[0] == 'and':
                    group.pop(0)
                else:
                    group = [group]
                for predicate in group:
                    if predicate[0] == 'not':
                        if len(predicate) != 2:
                            raise Exception('Unexpected not in ' + name + part)
                        negative.append(predicate[-1])
                    else:
                        positive.append(predicate)

        #if __name__ == '__main__':
        #import sys, pprint

        #domain = "domain.pddl"
        #problem = "problem.pddl"
        parser = PDDL_Parser()

        parser.parse_domain(domain_file)
        parser.parse_problem(problem_file)



        class Planner:


            def solve(self, domain, problem):
                # Parser
                parser = PDDL_Parser()
                parser.parse_domain(domain)
                parser.parse_problem(problem)
                # Parsed data
                state = parser.state
                goal_pos = parser.positive_goals
                goal_not = parser.negative_goals
                # Do nothing
                if self.applicable(state, goal_pos, goal_not):
                    return []
                # Grounding process
                ground_actions = []
                for action in parser.actions:
                    for act in action.groundify(parser.objects, parser.types):
                        ground_actions.append(act)
                # Search
                visited = set([state])
                fringe = [state, None]
                while fringe:
                    state = fringe.pop(0)
                    plan = fringe.pop(0)
                    for act in ground_actions:
                        if self.applicable(state, act.positive_preconditions, act.negative_preconditions):
                            new_state = self.apply(state, act.add_effects, act.del_effects)
                            if new_state not in visited:
                                if self.applicable(new_state, goal_pos, goal_not):
                                    full_plan = [act]
                                    while plan:
                                        act, plan = plan
                                        full_plan.insert(0, act)
                                    return full_plan
                                visited.add(new_state)
                                fringe.append(new_state)
                                fringe.append((act, plan))
                return None


            def applicable(self, state, positive, negative):
                return positive.issubset(state) and negative.isdisjoint(state)


            def apply(self, state, positive, negative):
                return state.difference(negative).union(positive)

        #if __name__ == '__main__':
            
        start_time = time.time()
        action_array = []
        
        verbose = len(sys.argv) > 3 and sys.argv[3] == '-v'
        planner = Planner()
        plan = planner.solve(domain_file, problem_file)
        print('Time: ' + str(time.time() - start_time) + 's')
        if type(plan) is list:
            #print('plan:')
            for act in plan:
                #print(act if verbose else act.name + ' ' + ' '.join(act.parameters))
                action = act if verbose else act.name + ' ' + ' '.join(act.parameters)
                action_array = action_array + [action]
            #print(action_array)
        else:
            print('No plan was found')
            exit(1)
            

        #plan = ['Action 1','Action 2'] 
        return action_array

    def solve_rrt(self, corners: [(float, float)]):
        """
        corners: [(float, float)] - a list of 4 (x, y) corners in a rectangle, in the
           order upper-left, upper-right, lower-right, lower-left

        returns: a list of (float_float) tuples containing the (x, y) positions of
           vertices along the path from the start to the goal node. The 0th index
           should be the start node, the last item should be the goal node. If no
           path could be found, return None
        """
        iterations = 1000
        x_dim = 10
        y_dim = 10
        start_node = [1,1]
        end_node = [9,9]
        nodes = [start_node]
        #nodes[0] = [1,1]
        paths = [[start_node]]
        solution_paths = []
        sq_pts = corners #[(3,7),(7,7),(3,3),(7,3)]
        #array1 = array1 + [elapsed_time]
        i = 0
        sq_pt1 = sq_pts[0]
        sq_pt2 = sq_pts[1]
        sq_pt3 = sq_pts[2]
        sq_pt4 = sq_pts[3]

        #node_paths = [ [[1,1],[2,2]], [[1,1],[3,3]] ]

        # A Python3 program to find if 2 given line segments intersect or not
        def dist(p1,p2):
            return math.sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))

        def onSegment(p, q, r):
            if ((q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and
                   (q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1]))):
                return True
            return False
         
        def orientation(p, q, r):    
            val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1]))
            if (val > 0): 
                return 1  # Clockwise orientation
            elif (val < 0):  
                return 2 # Counterclockwise orientation
            else:
                return 0 # Collinear orientation
         
        def test_intersect(p1,q1,p2,q2): # true if the line segment 'p1q1' and 'p2q2' intersect.
             
            # Find the 4 orientations required for
            # the general and special cases
            o1 = orientation(p1, q1, p2)
            o2 = orientation(p1, q1, q2)
            o3 = orientation(p2, q2, p1)
            o4 = orientation(p2, q2, q1)

            if ((o1 != o2) and (o3 != o4)): # General case
                return True
         
            if ((o1 == 0) and onSegment(p1, p2, q1)): # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
                return True

            if ((o2 == 0) and onSegment(p1, q2, q1)): # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
                return True
         
            if ((o3 == 0) and onSegment(p2, p1, q2)): # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
                return True

            if ((o4 == 0) and onSegment(p2, q1, q2)): # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
                return True

            return False # If none of the cases

        def add_node_paths(paths,closest_node,rand):
            for path in paths:
                if (path[-1] == closest_node):
                    new_path = copy.deepcopy(path)
                    new_path = new_path + [rand]
                    paths = paths + [new_path]
                    break
            #print("add_node_paths: done")
            return paths

        def check_path_to_end(sq_pt, paths, end_node, solution_paths):
            existing_path = paths[-1]
            i = 0
            intersect = False
            for sq_pt in sq_pts:
                if(i==0):
                    prev_pt = sq_pts[3]
                    
                if (test_intersect(prev_pt, sq_pt, existing_path[-1], end_node)):
                    intersect = True
                    #print("intersect: True")
                    break
              
                prev_pt = sq_pt
                i=i+1
                    
                
            if (intersect == False):
                #print("end path works")

                new_path = copy.deepcopy(existing_path)
                new_path = new_path + [end_node]
                paths = paths + [new_path]
                solution_paths = solution_paths + [new_path]
                
                    
            return paths, solution_paths
                    

        for j in range(iterations):

            #print("j: ",j)
            rand = [random.random()*x_dim, random.random()*y_dim]

            #print("rand:",rand)
            if(rand[0]>sq_pt1[0] and rand[0]<sq_pt4[0] and rand[1]<sq_pt1[1] and rand[1]>sq_pt4[1]):
                rand = end_node
                

            #print("rand:",rand)

            closest_node = [1,1]
            if (rand not in nodes):
                for node in nodes:
                     #print("node: ", node)
                    if (dist([node[0],node[1]],[rand[0],rand[1]]) < dist([closest_node[0],closest_node[1]],[rand[0],rand[1]])):
                        closest_node = [node[0],node[1]]

                #print("closest_node: ",closest_node)
                i = 0
                intersect = False
                for sq_pt in sq_pts:
                    if(i==0):
                        prev_pt = sq_pts[3]
                        
                    if (test_intersect(prev_pt, sq_pt, closest_node, rand)):
                        intersect = True
                        #print("intersect: True")
                        break
                  
                    prev_pt = sq_pt
                    i=i+1
                    
                if (intersect == False):
                    #print("intersect: False")
                    if(closest_node != end_node):
                        nodes = nodes + [rand]
                        paths = add_node_paths(paths,closest_node,rand)
                 
                        #print("try for end path")
                        paths, solution_paths = check_path_to_end(sq_pt, paths, end_node, solution_paths)
                        #print("paths: ",paths)

                #print("j: ",j)
                #print("nodes: ",nodes)
                #print("solution_paths: ",solution_paths)
           
               
        #print(len(solution_paths))
        #print(solution_paths)

        best_solution = []
        existing_dist_total = 1000
        dist_total = 0

        #solution_paths = [[[1.0, 1.0], [0.5178568060313504, 8.033679863661146], [9.321233931106182, 9.003334474359534], [5.378995378707076, 8.273015817220085], [6.881788049088911, 8.447529416734865], [9, 9]]]


        for solution in solution_paths:
            i = 0
            #print("solution: ",solution)
            for pt in solution:
                if(i>0):
                    #print("pt: ",pt)
                    #print("prev_pt: ",prev_pt)
                    distance = dist(prev_pt,pt)
                    dist_total = dist_total + distance
                    
                prev_pt = pt
                i = i+1
            #print("dist_total: ",dist_total)
            if (dist_total<existing_dist_total):
                best_solution = solution
                existing_dist_total = dist_total
                #print(existing_dist_total)
            dist_total = 0
            distance = 0
        print(best_solution)

        if best_solution == []:
            return None

        def totuple(a):
            try:
                return tuple(totuple(i) for i in a)
            except TypeError:
                return a
            
        
        return totuple(best_solution)


if __name__ == "__main__":
    p = PSet4()
    plan = p.solve_pddl('domain.pddl', 'problem.pddl')
    print("Plan : ", plan)
    print("Plan Length : ", len(plan))
    rrt_path = p.solve_rrt([(3,7),(7,7),(3,3),(7,3)])
    print("Path length: " + str(len(rrt_path)))


    #[(3,7),(7,7),(3,3),(7,3)]
#print(solve_pddl(1,"domain.pddl","problem.pddl"))
#solve_rrt(self, corners: [(float, float)])
