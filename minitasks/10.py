from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        try:
            self.cache.move_to_end(key)
            return self.cache[key]
        except:
            return -1

    def put(self, key: int, value: int) -> None:
        try:
            self.cache.move_to_end(key)
        except:
            pass
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
