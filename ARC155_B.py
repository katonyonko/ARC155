import io
import sys

_INPUT = """\
6
4 0 5
1 3 11
2 7 8
1 8 2
2 8 9
2 1 2
1 2 3
2 2 6
20 795629912 123625148
2 860243184 892786970
2 645778367 668513124
1 531411849 174630323
1 635062977 195695960
2 382061637 411843651
1 585964296 589553566
1 310118888 68936560
1 525351160 858166280
2 395304415 429823333
2 583145399 703645715
2 97768492 218377432
1 707220749 459967102
1 210842017 363390878
2 489541834 553583525
2 731279777 811513313
1 549864943 493384741
1 815378318 826084592
2 369622093 374205455
1 78240781 821999998
2 241667193 243982581
"""

sys.stdin = io.StringIO(_INPUT)
case_no=int(input())
for __ in range(case_no):
  #multiset
  import math
  from bisect import bisect_left, bisect_right, insort
  from typing import Generic, Iterable, Iterator, TypeVar, Union, List
  T = TypeVar('T')
  class SortedMultiset(Generic[T]):
    BUCKET_RATIO = 50
    REBUILD_RATIO = 170
  
    def _build(self, a=None) -> None:
        "Evenly divide `a` into buckets."
        if a is None: a = list(self)
        size = self.size = len(a)
        bucket_size = int(math.ceil(math.sqrt(size / self.BUCKET_RATIO)))
        self.a = [a[size * i // bucket_size : size * (i + 1) // bucket_size] for i in range(bucket_size)]
  
    def __init__(self, a: Iterable[T] = []) -> None:
        "Make a new SortedMultiset from iterable. / O(N) if sorted / O(N log N)"
        a = list(a)
        if not all(a[i] <= a[i + 1] for i in range(len(a) - 1)):
            a = sorted(a)
        self._build(a)
  
    def __iter__(self) -> Iterator[T]:
        for i in self.a:
            for j in i: yield j
  
    def __reversed__(self) -> Iterator[T]:
        for i in reversed(self.a):
            for j in reversed(i): yield j
  
    def __len__(self) -> int:
        return self.size
  
    def __repr__(self) -> str:
        return "SortedMultiset" + str(self.a)
  
    def __str__(self) -> str:
        s = str(list(self))
        return "{" + s[1 : len(s) - 1] + "}"
  
    def _find_bucket(self, x: T) -> List[T]:
        "Find the bucket which should contain x. self must not be empty."
        for a in self.a:
            if x <= a[-1]: return a
        return a
  
    def __contains__(self, x: T) -> bool:
        if self.size == 0: return False
        a = self._find_bucket(x)
        i = bisect_left(a, x)
        return i != len(a) and a[i] == x
  
    def count(self, x: T) -> int:
        "Count the number of x."
        return self.index_right(x) - self.index(x)
  
    def add(self, x: T) -> None:
        "Add an element. / O(√N)"
        if self.size == 0:
            self.a = [[x]]
            self.size = 1
            return
        a = self._find_bucket(x)
        insort(a, x)
        self.size += 1
        if len(a) > len(self.a) * self.REBUILD_RATIO:
            self._build()
  
    def discard(self, x: T) -> bool:
        "Remove an element and return True if removed. / O(√N)"
        if self.size == 0: return False
        a = self._find_bucket(x)
        i = bisect_left(a, x)
        if i == len(a) or a[i] != x: return False
        a.pop(i)
        self.size -= 1
        if len(a) == 0: self._build()
        return True
  
    def lt(self, x: T) -> Union[T, None]:
        "Find the largest element < x, or None if it doesn't exist."
        for a in reversed(self.a):
            if a[0] < x:
                return a[bisect_left(a, x) - 1]
  
    def le(self, x: T) -> Union[T, None]:
        "Find the largest element <= x, or None if it doesn't exist."
        for a in reversed(self.a):
            if a[0] <= x:
                return a[bisect_right(a, x) - 1]
  
    def gt(self, x: T) -> Union[T, None]:
        "Find the smallest element > x, or None if it doesn't exist."
        for a in self.a:
            if a[-1] > x:
                return a[bisect_right(a, x)]
  
    def ge(self, x: T) -> Union[T, None]:
        "Find the smallest element >= x, or None if it doesn't exist."
        for a in self.a:
            if a[-1] >= x:
                return a[bisect_left(a, x)]
  
    def __getitem__(self, x: int) -> T:
        "Return the x-th element, or IndexError if it doesn't exist."
        if x < 0: x += self.size
        if x < 0: raise IndexError
        for a in self.a:
            if x < len(a): return a[x]
            x -= len(a)
        raise IndexError
  
    def index(self, x: T) -> int:
        "Count the number of elements < x."
        ans = 0
        for a in self.a:
            if a[-1] >= x:
                return ans + bisect_left(a, x)
            ans += len(a)
        return ans
  
    def index_right(self, x: T) -> int:
        "Count the number of elements <= x."
        ans = 0
        for a in self.a:
            if a[-1] > x:
                return ans + bisect_right(a, x)
            ans += len(a)
        return ans

  def adding(a,b,f):
    if f==-1:
      if ms.lt(b)==None:
        if b not in ms: ms.add(b)
      else:
        if ms.index_right(b)%2==0:
          y=ms.le(b)
          x=ms.le(y)
          if y in ms: ms.discard(y)
          if b not in ms: ms.add(b)
          if (x+b)//2>=a:
            if (x+b)//2 not in ms: ms.add((x+b)//2)
          else:
            if a not in ms: ms.add(a)
        else:
          x=ms.le(b)
          ms.add(b)
          if (x+b)//2>=a:
            if (x+b)//2 not in ms: ms.add((x+b)//2)
          else:
            if a not in ms: ms.add(a)
    else:
      if ms.gt(a)==None:
        if a not in ms: ms.add(a)
      else:
        if ms.index_right(a)%2==0:
          y=ms.ge(a)
          x=ms.ge(y)
          if y in ms: ms.discard(y)
          if a not in ms: ms.add(a)
          if b>=(a+x)//2:
            if (a+x)//2 not in ms: ms.add((a+x)//2)
          else:
            if b not in ms: ms.add(b)
        else:
          x=ms.ge(a)
          if b>=(a+x)//2:
            if (a+x)//2 not in ms: ms.add((a+x)//2)
          else:
            if b not in ms: ms.add(b)

  Q,A,B=map(int,input().split())
  ms=SortedMultiset()
  ms.add(2*(A-B))
  ms.add(2*A)
  ms.add(2*(A+B))
  for _ in range(Q):
    t,a,b=map(int,input().split())
    if t==1:
      if 2*(a-b) in ms and ms.index(2*(a-b))%2==1: pass
      else:
        adding(-10**10,2*(a-b),-1)
        adding(2*(a-b),2*a,1)
        adding(2*a,2*(a+b),-1)
        adding(2*(a+b),10**10,1)
      print(ms)
    else:
      p,q=ms.index(2*a),ms.index(2*b)
      if q-p>1: print(0)
      elif q-p==1:
        if p%2==0: print(0)
        else:
          x,y=ms.le(2*a),ms.le(2*b)
          print((y-x-max(y-2*a,2*b-y))//2)
      else:
        x,y=ms.le(2*a),ms.ge(2*b)
        if p%2==2: print((y-2*b)//2)
        else: print((2*a-x)//2)
      print(ms)