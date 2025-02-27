class GWSCache:
    def __init__(self):
        """Initialize the cache dictionary."""
        self.cache = {}

    def set(self, key, value):
        """Store a value in the cache with the given key."""
        self.cache[key] = value

    def get(self, key):
        """Retrieve a value from the cache by key. Returns None if the key is not found."""
        return self.cache.get(key, None)

    def delete(self, key):
        """Remove a specific key from the cache."""
        if key in self.cache:
            del self.cache[key]

    def clear(self):
        """Clear all items from the cache."""
        self.cache.clear()

    def has_key(self, key):
        """Check if a key exists in the cache."""
        return key in self.cache
