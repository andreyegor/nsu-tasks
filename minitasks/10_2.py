from collections import defaultdict, deque


class LRUCache:

    def __init__(self, capacity: int):
        self.cache = dict()
        self.capacity = capacity
        self.lru = deque()
        self.lru_cnt = defaultdict(int)

    def get(self, key: int) -> int:
        try: 
            out = self.cache[key]
            self.lru.append(key)
            self.lru_cnt[key]+=1
        except: 
            out = None
        return out

    def put(self, key: int, value: int) -> None:
        self.cache[key] = value
        self.lru.append(key)
        self.lru_cnt[key]+=1
        if len(self.cache)>self.capacity:
            while True:
                LRU_key = self.lru.popleft()
                self.lru_cnt[LRU_key]-=1
                if self.lru_cnt[LRU_key] <= 0:
                    break
            del self.cache[LRU_key]
        

cache = LRUCache(3)
cache.put("1", "a")
cache.put("2", "b")
cache.put("3", "c")
print(cache.get("1"))
cache.put("4", "d")
print(cache.get("2"))