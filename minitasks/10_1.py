from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity=16):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return None

    def put(self, key, value):
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


cache = LRUCache(3)
cache.put("1", "a")
cache.put("2", "b")
cache.put("3", "c")
print(cache.get("1"))
cache.put("4", "d")
print(cache.get("2"))
