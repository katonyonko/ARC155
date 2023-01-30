import io
import sys

_INPUT = """\
6
2
6 2
abbaab
5 3
abcbb
3
12 400378271514996652
njvhhvjnnjvh
10 884633988115575508
rrhiyvrrur
36 71630165869626180
vsxmxajrrduhhudrrjaxmxsvvsxmxajrrduh
"""

sys.stdin = io.StringIO(_INPUT)
case_no=int(input())
for __ in range(case_no):
  T=int(input())
  for i in range(T):
    N,K=map(int,input().split())
    S=input()
    if K>2*N:
      m=K//N
      n=K%N
      if m%2==0: a=S[:n][::-1]+S+S[::-1][:N-n]
      else: a=S[N-n:]+S[::-1]+S[:N-n]
      if a==S[::-1]+S: print('Yes')
      else: print('No')
    else:
      Sd=(S[::-1]+S)[:K]
      if S+Sd==(S+Sd)[::-1] and (Sd+S)==(Sd+S)[::-1]: print('Yes')
      else: print('No')