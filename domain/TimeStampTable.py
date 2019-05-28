from collections import OrderedDict

class TimeStampTable(OrderedDict):
    def __init__(self, *args, **kwds):
        self.ts_number_limit = kwds.pop("size_limit", None)
        super().__init__(self, *args, **kwds)
    
    def __setitem__(self, key, value):
        OrderedDict.__setitem__(self, key, value)
        self._check_size_limit()

    def _check_size_limit(self):
        if self.ts_number_limit is not None:
            while len(self) > self.ts_number_limit:
                self.popitem(last=False)