class Greet (gdb.Function):
    def __init__ (self):
        super (Greet, self).__init__ ("greet")

    def window(self, seq, n=2):
        from itertools import islice
        it = iter(seq)
        result = tuple(islice(it, n))
        if len(result) == n:
            yield result    
        for elem in it:
            result = result[1:] + (elem,)
            yield result

    def genlist(self):
        frame = gdb.newest_frame()
        decorator = gdb.FrameDecorator.FrameDecorator(frame)
        frame_locals = sorted(decorator.frame_locals(), key=lambda fl: fl.sym.value(frame).address)
        local_vars = ['&{}'.format(i.sym.name) for i in frame_locals]
        local_vars.append('$ebp')
        local_vars.insert(0, '$esp')
        return local_vars

    def remove(self):
        for i in self.genlist():
            gdb.execute('dashboard memory unwatch {}'.format(i))

    def add(self):
        for (start, end) in self.window(self.genlist()):
            print('{} to {}'.format(start, end))
            gdb.execute('dashboard memory watch {} ((void*) {} - (void*) {} )'.format(start, end, start))

    def invoke (self, action='add'):
        if action == 'remove': self.remove()
        else: self.add()
        return 'ok'

Greet ()
