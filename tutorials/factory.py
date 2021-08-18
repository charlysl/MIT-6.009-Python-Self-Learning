## Factory Simulator

class Factory:
    """ Keeps track of the state of a factory """
    def __init__(self):
        self.machines = []
        self.output_queue = Queue("finished goods")
        self.queues = [self.output_queue]
        self.time = 0
        self.setup()

    def setup(self):
        pass

    def simulate(self, num_steps, report=False):
        if report: print("starting simulation at time", self.time)
        while num_steps > 0:
            if report: print("time:", self.time)
            for m in self.machines:
                m.timestep()
            self.time += 1
            num_steps -= 1
            if report: self.report()
        if report:
            print("ending simulation at time", self.time)
            print("  Output parts:")
            for p in self.output_queue.parts:
                print("   ", p)

    def report(self):
        """ report state of factory """
        for m in self.machines:
            m.report()
        for q in self.queues:
            q.report()

class ToyFactory(Factory):
    def setup(self):
        nuts  = InfiniteQueue("nuts supply", Nut)
        bolts = InfiniteQueue("bolts supply", Bolt)
        cutter_q = Queue("cutter", Assembly)
        paint_q = Queue("paint", Toy)
        self.queues = [nuts, bolts, cutter_q, paint_q] + self.queues

        slow_m = Assembler('slow', [nuts, bolts], cutter_q, 3)
        fast_m = Assembler('fast', [nuts, bolts], cutter_q, 1)
        cut3 = Cutter('spicy', [cutter_q], paint_q, 1)
        paint = Painter('red', [paint_q], self.output_queue, 1)
        self.machines += [slow_m, fast_m, cut3, paint]


class Part:
    next_id = 0
    def __init__(self):
        self.__class__.next_id += 1
        self.id = self.next_id

    def __repr__(self):
        return "<"+self.__class__.__name__+" "+str(self.id)+">"

class Nut(Part):
    next_id = 0

class Bolt(Part): 
    next_id = 0

class Assembly(Part):
    next_id = 0
    def __init__(self, sub_parts=None):
        Part.__init__(self)
        self.sub = sub_parts

    def __repr__(self):
        result = str(self.id)
        if self.sub:
            result += ", sub: "+str(self.sub)
        return "<"+self.__class__.__name__+" "+result+">"

class Toy(Assembly):
    next_id = 0


class Queue:
    def __init__(self, name, cls=Part):
        self.name = name
        self.parts = []
        self.make_part = cls

    def push(self, parts):
        self.parts.append(parts)

    def pop(self):
        return self.parts.pop(0)

    def report(self):
        print(" ", self)
        
    def __len__(self):
        return len(self.parts)

    def __repr__(self):
        contents = str(len(self.parts))+" "+self.make_part.__name__+"s"
        return "<"+self.__class__.__name__+" ("+repr(self.name)+"): "+contents+">"
    
class InfiniteQueue(Queue):
    def __init__(self, name, cls=Part):
        Queue.__init__(self, name, cls=cls)
        self.push(self.make_part())
        
    def pop(self):
        p = Queue.pop(self)
        self.push(self.make_part())
        return p


class Machine:
    def __init__(self, name, in_queues, out_queue, time_required):
        self.name = name
        self.tat = time_required
        self.in_queues = in_queues
        self.out_queue = out_queue

        self.state = 'waiting'  # 'waiting' | 'busy' | 'offline'
        self.time_remaining = 0
        self.parts = []

    def timestep(self):
        if self.state == 'waiting':
            return self.start_operation()
        elif self.state == 'busy':
            self.time_remaining -= 1
            if self.time_remaining <= 0:
                return self.finish_operation()
        else:
            return self.state

    def start_operation(self):
        """ Attempt to start operation. Return state of machine """
        if self.state != 'waiting':
            return self.state

        # Get needed parts, if available
        if not all((len(q)>0 for q in self.in_queues)):
            self.state = 'waiting'  # still waiting for some inputs
            return self.state 

        # Can get all needed parts
        self.state = 'busy'
        self.parts = [q.pop() for q in self.in_queues]
        self.time_remaining = self.tat
        return self.state
        
    def finish_operation(self):
        """ Generic operation: pass-through parts """
        for p in self.parts:
            self.out_queue.push(p)
        self.state = 'waiting'
        self.parts = []

    def report(self):
        print(" ", self)

    def __repr__(self):
        status = self.state
        if self.state == 'busy':
            status += ", time_remaining: " + str(self.time_remaining)
        return "<"+self.__class__.__name__+" ("+repr(self.name)+"): "+status+">"

class Assembler(Machine):
    def finish_operation(self):
        new_part = Assembly(self.parts)
        self.out_queue.push(new_part)
        self.state = 'waiting'
        self.parts = []

class Cutter(Machine):
    def finish_operation(self):
        for p in self.parts:
            for i in range(3):
                self.out_queue.push(Toy(p))
        self.state = 'waiting'
        self.parts = []

class Painter(Machine):
    def finish_operation(self):
        for p in self.parts:
            p.color = 'red'
            self.out_queue.push(p)
        self.state = 'waiting'
        self.parts = []

if __name__ == '__main__':
    f = ToyFactory()
    results = []
    for i in range(20):
        f.simulate(10, False)
        results.append(len(f.output_queue))
    f.report()
    print("results per 10 time units:", results)
