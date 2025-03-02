from .fileio import FileIO


class BinaryFile(FileIO):
    def read(self) -> bytes:
        return self.as_bytes()

    def write(self,content: bytes):
        with open(self.fpath, 'wb') as file:
            file.write(content)

    def view(self):
        content = self.read()
        hex_content = content.hex()
        for i in range(0, len(hex_content), 20):
            line = ' '.join(hex_content[j:j + 2] for j in range(i, min(i + 20, len(hex_content)), 2))
            print(line)

    def check_content_ok(self):
        pass



