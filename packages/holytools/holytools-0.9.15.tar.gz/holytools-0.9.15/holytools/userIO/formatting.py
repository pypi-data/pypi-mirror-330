class MessageFormatter:
    @staticmethod
    def get_boxed(text: str, headline: str = "") -> str:
        lines = text.split("\n")
        max_length = max([len(line) for line in lines] + [len(headline)+2])
        border = "+" + "-" * (max_length + 2) + "+"
        if headline:
            headline = f' {headline} '
            top_line = f"+{headline.center(max_length + 2, '-')}+"
        else:
            top_line =  border
        boxed_text = [top_line] + [f"| {line.ljust(max_length)} |" for line in lines] + [border]
        return "\n".join(boxed_text)


    @staticmethod
    def get_boxed_train(messages: list) -> str:
        if len(messages) == 0:
            raise ValueError("No messages to format")

        for msg in messages:
            if '\n' in msg:
                raise ValueError(f"Message contains newline character: {msg}")
        wagons = [MessageFormatter.get_boxed(headline="", text=msg) for msg in messages]

        total_str = ''
        no_lines = 3
        wagon_sep = 5

        pulled_cabins = [w.split('\n') for w in wagons[:-1]]
        conductor_lines = wagons[-1].split('\n')

        for j in range(no_lines):
            connect_symbol = '-' if j == 1 else ' '
            connector = f'{connect_symbol * wagon_sep}'
            for lines in pulled_cabins:
                total_str += f'{lines[j]}{connector}'
            total_str += f'{conductor_lines[j]}\n'

        total_str = total_str.strip()

        return total_str
