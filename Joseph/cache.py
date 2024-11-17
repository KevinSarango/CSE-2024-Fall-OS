from collections import deque
import random

DEBUG = False
def dbg(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

class Cache:
    def __init__(self, cache_size):
        self._cache_size = cache_size
        self._accesses = 0
        self._hits = 0
        self._misses = 0
        self.reset()
    
    def reset(self):
        self._accesses = 0
        self._hits = 0
        self._misses = 0
    
    def access(self, page_num):
        pass

    def hit_rate(self):
        return self._hits / self._accesses
    
    def miss_rate(self):
        return self._misses / self._accesses

class FIFOCache(Cache):
    def __init__(self, cache_size):
        super().__init__(cache_size)
        self._state = deque()
    
    def access(self, page_num):
        self._accesses += 1
        
        if page_num in self._state:
            dbg(f"[FIFOCache] Access {page_num} => hit!")
            self._hits += 1
        else:
            dbg(f"[FIFOCache] Access {page_num} => miss")
            self._misses += 1
            
            self._state.append(page_num)
            if len(self._state) > self._cache_size:
                out = self._state.popleft()
                dbg(f"[FIFOCache] Evicting {out} from cache")
            #dbg(f"[FIFOCache] State is now {self._state}")

class RandomCache(Cache):
    def __init__(self, cache_size):
        super().__init__(cache_size)
        self._state = []
    
    def access(self, page_num):
        self._accesses += 1
        
        if page_num in self._state:
            dbg(f"[RandomCache] Access {page_num} => hit!")
            self._hits += 1
        else:
            dbg(f"[RandomCache] Access {page_num} => miss")
            self._misses += 1
            
            self._state.append(page_num)
            if len(self._state) > self._cache_size:
                out = random.choice(self._state)
                self._state.remove(out)
                dbg(f"[RandomCache] Evicting {out} from cache")
            #dbg(f"[RandomCache] State is now {self._state}")

class LRUCache(Cache):
    def __init__(self, cache_size):
        super().__init__(cache_size)
        self._state = {}
    
    def access(self, page_num):
        self._accesses += 1
        
        for k,v in self._state.items():
            self._state[k] = v + 1
        
        if page_num in self._state:
            dbg(f"[LRUCache] Access {page_num} => hit!")
            self._hits += 1
            self._state[page_num] = 0
        else:
            dbg(f"[LRUCache] Access {page_num} => miss")
            self._misses += 1
            self._state[page_num] = 0
            
            if len(self._state) > self._cache_size:
                out = max(self._state, key=self._state.get)
                del self._state[out]
                dbg(f"[LRUCache] Evicting {out} from cache")
            #dbg(f"[LRUCache] State is now {self._state}")

class OptimalCache(Cache):
    pass

def do_test(cache, size, pattern):
    inst = cache(size)
    for a in pattern:
        inst.access(a)
    return (inst.hit_rate(), inst.miss_rate())

def test_cache(cache, size, pattern):
    name = cache.__name__
    print(f"Testing {name}({size=}) with pattern '{pattern}'")
    hr, mr = do_test(cache, size, pattern)
    print(f"{name}({size=}) had a hit rate of {hr:.2f} and a miss rate of {mr:.2f}")

def main():
    test_cache(FIFOCache, 3, "01201303121")
    test_cache(RandomCache, 3, "01201303121")
    test_cache(LRUCache, 3, "01201303121")

main()
