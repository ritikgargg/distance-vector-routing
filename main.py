N = 5 # Number of nodes(or routers)
inf = float('inf')

# Adjacency matrix for the routers
adj = [
    [0, 1, inf, inf, 1],
    [1, 0, 1, inf, inf],
    [inf, 1, 0, 1, inf],
    [inf, inf, 1, 0, 1],
    [1, inf, inf, 1, 0],
]

class Router:
    def __init__(self, x):
        '''
        '''
        self.x = x

        # Distance vector for the router
        self.dv = adj[x][:]

        # Next routers
        self.next = [None for _ in range(N)]
        for i in range(N):
            if adj[x][i] != inf:
                self.next[i] = i
    
    def receive(self, router):
        '''Function which receives the routing tables of other routers and updates the routing table of the receiving router.
        It also returns 'True' in case of an updation in the routing table of the receiver, or 
                        'False' when there is no updation in the routing table of the receiving router.'''
        if adj[router.x][self.x] != 1: # Only neighbors should be able to send distance vectors
            return False

        dv = router.get_refined_dv(self.x) # Using the split horizon method

        is_updated = False
        for destination in range(N):
            old_distance = self.dv[destination]
            new_distance = adj[self.x][router.x] + dv[destination]
            
            # Applying the cases of the routing algorithm
            if self.next[destination] == router.x:
                self.dv[destination] = new_distance
                self.next[destination] = router.x
                is_updated |= old_distance != new_distance
            elif new_distance < old_distance:
                self.dv[destination] = new_distance
                self.next[destination] = router.x
                is_updated = True
        return is_updated

    def get_refined_dv(self, to_router):
        '''Function to apply the split horizon strategy'''
        new_dv = self.dv[:]
        for i in range(N):
            if self.next[i] == to_router:
                new_dv[i] = inf
        return new_dv

def print_dvs():
    '''Function to print the routing information of all the routers'''
    for router in routers:
        print('ABCDE'[router.x], end='|  ')
        for i in range(N):
            dist = None
            next = ' '
            if router.dv[i] == inf:
                dist = '∞'
            else:
                dist = router.dv[i]

            if router.next[i] is not None:
                next = 'ABCDE'[router.next[i]]
            print(f'{dist}{next}', end=' ')
        print()
    print()

# Creating the required number of routers
routers = [Router(i) for i in range(N)]

print("\nIn the following outputs, each row depicts the routing table corresponding to the router(or node) printed at the head of the row.")
print("The entries in the routing table comprise of the distance and the next hop router values.\n")

t = 0
print("t = ", t)
print_dvs() # Initial state of the routing tables of all the routers

# Using a while loop to determine the time instant after which every node can reach every other node in the network.
while True:
    is_updated = False
    for sender in routers:
        for receiver in routers:
            is_updated |= receiver.receive(sender)
    # Break the loop when the network gets stabilized.
    if not is_updated:
        break
    t += 1
    print("t = ", t)
    print_dvs()

print("After t =", t , ", every node can reach every other node in the network.\n")

# Link breaking
t = t + 1
print("At t =", t, ", link BC breaks.\n")

# Updating the adjacency matrix and routing tables of the required routers to reflect the link breakage.
adj[1][2] = inf
adj[2][1] = inf

for i in range(N):
    if routers[1].next[i] == 2:
        routers[1].dv[i] = inf
        routers[1].next[i] = None
    if routers[2].next[i] == 1:
        routers[2].dv[i] = inf
        routers[2].next[i] = None

t = t + 1
print("t =", t)
print("Distance vectors after the link BC is broken:")
print_dvs()

# Using a while loop to determine the time instant after which the network stabilizes again.
while True:
    is_updated = False
    for sender in routers:
        for receiver in routers:
            is_updated |= receiver.receive(sender)
    if not is_updated:
        break
    t += 1
    print("t = ", t)
    print_dvs()

print("After t =", t , ", the network stabilizes again.\n")