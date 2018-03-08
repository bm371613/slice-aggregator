class IndexedUniqueMaxHeap:

    def __init__(self):
        self.data = []
        self.index = {}

    def _swap(self, ix1: int, ix2: int) -> None:
        ix1 = ix1 % len(self)
        ix2 = ix2 % len(self)
        if ix1 == ix2:
            return
        v1 = self.data[ix1]
        v2 = self.data[ix2]
        self.data[ix1] = v2
        self.data[ix2] = v1
        self.index[v2] = ix1
        self.index[v1] = ix2

    def add(self, value: int) -> None:
        if value in self:
            return
        child_ix = len(self)
        self.data.append(value)
        self.index[value] = child_ix
        parent_ix = (child_ix - 1) // 2
        while child_ix > 0 and self.data[child_ix] > self.data[parent_ix]:
            self._swap(child_ix, parent_ix)

            child_ix = parent_ix
            parent_ix = (child_ix - 1) // 2

    def remove(self, value: int) -> None:
        if value not in self:
            return
        ix = self.index[value]
        self._swap(ix, -1)
        del self.data[-1]
        del self.index[value]
        while True:
            snd = 2 * (ix + 1)
            fst = snd - 1
            if fst >= len(self):
                break
            selected = snd if snd < len(self) and self.data[snd] >= self.data[fst] else fst
            self._swap(ix, selected)
            ix = selected

    def max(self) -> int:
        return self.data[0] if self.data else None

    def __contains__(self, value: int) -> bool:
        return value in self.index

    def __len__(self) -> int:
        return len(self.data)
