class LRUCache:

    def __init__(self, capacity: int):
        self.cache = dict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        if key in self.cache.keys(): 
            out = self.cache[key]
            del self.cache[key]
            self.cache[key] = out
        else: 
            out = None
        return out

    def put(self, key: int, value: int) -> None:
        try: del self.cache[key]
        except: pass
        self.cache[key] = value
        if len(self.cache)>self.capacity:
            del self.cache[next(iter(self.cache))]
            
cache = LRUCache(3)
cache.put("1", "a")
cache.put("2", "b")
cache.put("3", "c")
print(cache.get("1"))
cache.put("4", "d")
print(cache.get("2"))