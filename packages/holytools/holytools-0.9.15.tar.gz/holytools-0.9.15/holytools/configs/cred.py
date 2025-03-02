import sys

from holytools.configs import FileConfigs


def main():
    configs = FileConfigs.credentials()
    num_args = len(sys.argv) - 1

    if num_args == 0:
        print(f'Credential store content')
        content = configs.read().strip()
        if len(content) == 0:
            return

        lines = content.split(f'\n')
        for l in lines:
            if len(l) > 0 and not l.startswith(f'['):
                l = f'├── {l}'
            print(l)

    elif num_args == 2:
        action, key = sys.argv[1], sys.argv[2]
        if action == 'insert':
            value = input(f'Enter value for key \"{key}\": ')
            configs.set(key=key, value=value)
        elif action == 'remove':
            configs.remove(key=key)
        else:
            raise ValueError(f'Unknown command \"{action}\"')
    else:
        raise ValueError(f'Invalid command syntax: {sys.argv}')

if __name__ == "__main__":
    main()