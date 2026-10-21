import heapq, math

def build_demo_grid(w, h):
    g=[[0]*h for _ in range(w)]
    # Obstacles mapped approximately from the Webots world, inflated for the robot footprint.
    def block(x0,x1,z0,z1):
        for x in range(max(0,x0), min(w,x1+1)):
            for z in range(max(0,z0), min(h,z1+1)): g[x][z]=1
    block(10,20,14,17)  # horizontal obstacle
    block(26,29,17,26)  # vertical obstacle
    block(15,25,6,9)    # lower obstacle
    return g

def astar_grid(grid, start, goal):
    w,h=len(grid),len(grid[0])
    if grid[start[0]][start[1]] or grid[goal[0]][goal[1]]: return []
    q=[(0,start)]; came={}; cost={start:0}
    while q:
        _,cur=heapq.heappop(q)
        if cur==goal:
            path=[cur]
            while cur in came: cur=came[cur]; path.append(cur)
            return path[::-1]
        for dx,dz in ((1,0),(-1,0),(0,1),(0,-1)):
            n=(cur[0]+dx,cur[1]+dz)
            if not(0<=n[0]<w and 0<=n[1]<h) or grid[n[0]][n[1]]: continue
            nc=cost[cur]+1
            if nc<cost.get(n,1e9):
                cost[n]=nc; came[n]=cur
                hcost=abs(goal[0]-n[0])+abs(goal[1]-n[1])
                heapq.heappush(q,(nc+hcost,n))
    return []

def dijkstra_grid(grid,start,goal):
    w,h=len(grid),len(grid[0]); q=[(0,start)]; came={}; cost={start:0}
    while q:
        d,cur=heapq.heappop(q)
        if cur==goal: break
        for dx,dz in ((1,0),(-1,0),(0,1),(0,-1)):
            n=(cur[0]+dx,cur[1]+dz)
            if not(0<=n[0]<w and 0<=n[1]<h) or grid[n[0]][n[1]]: continue
            nd=d+1
            if nd<cost.get(n,1e9): cost[n]=nd; came[n]=cur; heapq.heappush(q,(nd,n))
    if goal not in cost: return []
    p=[goal]; c=goal
    while c in came: c=came[c]; p.append(c)
    return p[::-1]
