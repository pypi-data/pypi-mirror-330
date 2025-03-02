from .fileio import FileIO

class PlaintextFile(FileIO):
    def read(self) -> str:
        with open(self.fpath, 'r') as f:
            text = f.read()
        return text

    def write(self, content: str):
        with open(self.fpath, 'w', encoding='utf-8') as file:
            file.write(content)

    def view(self):
        content = self.read()
        print(content)

    def check_content_ok(self):
        try:
            with open(self.fpath, 'rb') as file:
                bytes_content = file.read()
                bytes_content.decode('utf-8')
            return True
        except UnicodeDecodeError:
            raise TypeError(f'File {self.fpath} is not a valid utf-8 encoded text file')

    @classmethod
    def get_text(cls, fpath : str) -> str:
        with open(fpath, 'r') as f:
            text = f.read()
        return text
