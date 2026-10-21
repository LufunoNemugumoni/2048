import heapq
def plan(grid,start,goal,astar=True):
 q=[(0,start)];came={};d={start:0}
 while q:
  _,u=heapq.heappop(q)
  if u==goal:
   p=[u]
   while u in came:u=came[u];p.append(u)
   return p[::-1]
  for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
   v=(u[0]+dr,u[1]+dc)
   if 0<=v[0]<len(grid) and 0<=v[1]<len(grid[0]) and grid[v[0]][v[1]]==0 and d[u]+1<d.get(v,10**9):
    d[v]=d[u]+1;came[v]=u;h=abs(v[0]-goal[0])+abs(v[1]-goal[1]) if astar else 0;heapq.heappush(q,(d[v]+h,v))
 return []
