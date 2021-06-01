import numpy as np


class ObjectCollection:
    def __init__(self,
                 objects: np.ndarray):

        self.objects = objects
        self.indices = self.get_indices(objects)
        self.idx_table = dict(zip(objects.ravel(), self.indices.ravel()))

    @ property
    def shape(self):
        return self.objects.shape

    @ property
    def size(self):
        return self.objects.size

    def get_idx(self, obj):
        return self.idx_table[obj]

    def __getitem__(self, indices):
        item = self.objects[indices]
        return (item if not isinstance(item, np.ndarray)
                else ObjectCollection(item))

    def __getattribute__(self, name: str):
        if (hasattr(ObjectCollection, name)
                or name in ['objects', 'indices', 'idx_table']):
            return object.__getattribute__(self, name)

        elif callable(getattr(self.objects[self.indices[0]], name)):
            def multicall(*args, **kwargs):
                output = np.empty(self.shape, object)
                output_args = np.empty(self.size, object)
                output_args[:] = [list() for i in range(self.size)]
                output_args = output_args.reshape(self.shape)

                output_kwargs = np.empty(self.size, object)
                output_kwargs[:] = [dict() for i in range(self.size)]
                output_kwargs = output_kwargs.reshape(self.shape)

                for arg in args:
                    args_broadcasted = np.broadcast_to(arg, self.shape)
                    for idx in self.indices:
                        output_args[idx].append(args_broadcasted[idx])
                for key, item in kwargs.items():
                    kwargs_broadcasted = np.broadcast_to(item, self.shape)
                    for idx in self.indices:
                        output_kwargs[idx][key] = kwargs_broadcasted[idx]
                for idx in self.indices.ravel():
                    output[idx] = getattr(self.objects[idx], name)(
                        *output_args[idx], **output_kwargs[idx])
                return output
            return multicall
        else:
            output = np.empty(self.shape, object)
            for idx in self.indices.ravel():
                output[idx] = getattr(self.objects[idx], name)
            return output

    @ staticmethod
    def get_indices(array: np.ndarray):
        indices = np.indices(array.shape).reshape(array.ndim, -1).T
        out = np.empty(array.size, dtype=object)
        out[:] = list(map(tuple, indices))
        return out
