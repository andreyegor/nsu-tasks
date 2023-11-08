from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity=16):
        self._cache = OrderedDict()
        self._capacity = capacity

    def get(self, key):
        try:
            self._cache.move_to_end(key)
            return self._cache[key]
        except:
            return None

    def put(self, key, value):
        try:
            self._cache.move_to_end(key)
        except:
            pass
        self._cache[key] = value
        if len(self._cache) > self._capacity:
            self._cache.popitem(last=False)


cache = LRUCache(3)
cache.put("1", "a")
cache.put("2", "b")
cache.put("3", "c")
print(cache.get("1"))
cache.put("4", "d")
print(cache.get("2"))