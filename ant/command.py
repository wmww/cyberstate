import ant

class Command(ant.Ant):
    def __init__(self, *args):
        self.args = list(args)
        self.kwargs = {}
        self.deps = []
        self.sudo = False
        self.result = None

    def with_arg(self, arg):
        self.args.append(arg)
        return self

    def with_args(self, *args):
        self.args += list(args)
        return self

    def with_timout(self, timout):
        self.kwargs['timout'] = timout
        return self

    def with_input_str(self, input_str):
        self.kwargs['input_str'] = input_str
        return self

    def with_passthrough(self):
        self.kwargs['passthrough'] = True
        return self

    def with_cwd(self, cwd):
        self.kwargs['cwd'] = cwd
        return self

    def with_sudo(self):
        self.sudo = True
        return self

    def with_ignore_error(self):
        self.kwargs['ignore_error'] = True
        return self

    def into_check(self):
        return Check(self)

    def march(self, queen):
        args = self.args
        if not args:
            raise Error('No command arguments supplied')
        if self.sudo:
            args = ['sudo', '-S'] + args
        self.result = queen.run_command(args, **self.kwargs)

class Check(ant.Check):
    def __init__(self, command):
        assert isinstance(command, Command)
        self.command = command
        self.deps = [
            command.with_ignore_error()
        ]

    def check(self, queen):
        assert self.command.result
        return self.command.result.exit_code == 0