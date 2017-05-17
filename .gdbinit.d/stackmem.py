class Watchstack (gdb.Function):
    def __init__ (self):
        super (Watchstack, self).__init__ ("watchstack")

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
        local_vars.append('$ebp+8')
        local_vars.insert(0, '$esp')
        return local_vars

    def remove(self):
        for i in self.genlist()[:-1]:
            gdb.execute('dashboard memory unwatch {}'.format(i))

    def add(self):
        for (start, end) in self.window(self.genlist()):
            gdb.execute('dashboard memory watch {} ((void*) {} - (void*) {} )'.format(start, end, start))

    def invoke (self, action):
        action = action.string()
        if action == "remove": self.remove()
        elif action == "add": self.add()
        return action

Watchstack ()
