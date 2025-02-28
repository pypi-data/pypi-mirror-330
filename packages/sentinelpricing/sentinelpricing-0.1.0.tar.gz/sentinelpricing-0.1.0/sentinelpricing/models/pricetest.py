"""Price Test

Aims to make price testing easier to implement.

Needs to consider:
    - Buckets
    - Hashing (likely?)
    - LookupTable
"""

from itertools import combinations
from typing import List, Set

from .lookuptable import LookupTable


class Bucket:
    def __init__(self, a):
        self.bucket = a
        self.count = 0
        self.values = set()

    def put(self, val):
        self.values.add(val)
        self.count += 1


class PriceTest:

    def __init__(self, by: str, ratetable: LookupTable):

        self.by = by
        self.ratetable = ratetable

        self.num_buckets = len(ratetable)
        self.buckets = {i: Bucket(i) for i in range(self.num_buckets)}

    def __repr__(self): ...

    def apply(self, quote):
        by = self.by
        val = by(quote) if callable(by) else quote[by]
        bucket = hash(val) % self.buckets

        self.buckets[bucket]["values"].add(val)
        self.buckets[bucket]["count"] += 1

        return self.ratetable.lookup(bucket)

    def unique_bucket_values(self) -> bool:
        bucket_sets: List[Set] = [b.values for b in self.buckets.values()]

        for a, b in combinations(bucket_sets, 2):

            if len(a.intersection(b)) > 0:
                return False

        return True
