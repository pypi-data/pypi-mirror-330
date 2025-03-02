import builtins


class InputSimulator:
    def __init__(self, inputs : list[str]):
        def generator():
            for inp in inputs:
                yield inp

        self.gen = generator()
        self.original_input = input

    def substitute(self):
        builtins.input = self.simulated_input

    def restore_input(self):
        builtins.input = self.original_input

    def simulated_input(self, *args, **kwargs):
        _ = kwargs
        try:
            response = next(self.gen)
        except:
            response = self.original_input()
        combined = f'{args[0]} {response}' if args else response
        print(combined)
        return response

if __name__ == "__main__":
    a = InputSimulator([f'An ice cream please','No, thank you'])
    a.substitute()

    item = input('What do you want?')
    r = input(f'Anything else?')

    print(f'done')