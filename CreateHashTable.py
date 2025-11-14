class CreateHashTable:
    def __init__(self, capacity):
        self.capacity = capacity
        self.table = []
        for i in range(capacity):
            self.table.append([])

    def insert(self, key, value):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for keyValue in bucket_list:
            if keyValue[0] == key:
                keyValue[1] = value
                return True
        key_value = [key, value]
        bucket_list.append(key_value)
        return True

    # searches keyvalue for the correct key (keyValue[0])
    # and returns correct value keyValue[1]
    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for keyValue in bucket_list:
            if keyValue[0] == key:
                return keyValue[1]
        return None

    # searches keyvalue for the correct key and deletes it
    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        if key in bucket_list:
            bucket_list.remove(key)