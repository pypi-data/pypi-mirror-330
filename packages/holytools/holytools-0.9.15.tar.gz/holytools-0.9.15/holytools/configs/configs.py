from __future__ import annotations
import os.path
from typing import Optional

import secretstorage
from cryptoalgos.encrypt import AES
from cryptoalgos.hash import SHA

from holytools.configs.base import BaseConfigs
from holytools.logging import LogLevel

# ---------------------------------------------------------

class FileConfigs(BaseConfigs):
    def __init__(self, fpath : str = '~/.pyconfig', encrypted : bool = False):
        self._config_fpath: str = self._as_abspath(path=fpath)
        self.is_encrypted : bool = encrypted
        if self.is_encrypted and not self.keyring_available():
            raise ValueError('Encrypted configs can only be used with D-Bus Secret Service e.g. GNOME Keyring')

        if self.is_encrypted:
            self.aes : AES = AES()
            self.sha : SHA = SHA()
            self.masterpw_hash : bytes = self.retrieve_masterpw_hash()
        config_dirpath = os.path.dirname(self._config_fpath)
        os.makedirs(config_dirpath, exist_ok=True)
        super().__init__()

    @classmethod
    def credentials(cls) -> FileConfigs:
        try:
            fpath = os.environ[f'CRED_FPATH']
        except:
            raise ValueError(f'Environment variable \"CRED_FPATH\" not found. '
                             f'Please define file path of config file through environment variable \"CRED_FPATH\"')
        # print(f'fpath = {fpath}')
        if not os.path.isfile(fpath):
            raise ValueError(f'File at path \"{fpath}\" does not exist')

        return FileConfigs(encrypted=True, fpath=fpath)


    def _populate_map(self):
        if not os.path.isfile(self._config_fpath):
            self.log(msg=f'File {self._config_fpath} could not be found, configs are empty', level=LogLevel.WARNING)
            return self._map

        content = self.read()
        lines = content.split(f'\n')

        current_section = None
        non_empty_lines = [line for line in lines if line.strip()]
        for num, line in enumerate(non_empty_lines):
            parts = line.split(f' = ')
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1]
                self._map[current_section] = {}
            elif len(parts) == 2:
                self._read_line(parts=parts, current_section=current_section, num=num)
            else:
                raise ValueError(f'Line {num + 1} in config file is invalid: \"{line}\"')

    def _read_line(self, parts : (str, str), current_section : Optional[str], num : int):
        key, value = parts
        if ' ' in key:
            raise ValueError(f'Key must not contain whitespaces, got key \"{key}\" in line {num + 1}')
        if ' ' in value:
            raise ValueError(f'Value must not contain whitespaces, got value \"{value}\" in line {num + 1}')
        self._map[current_section][key] = value

    def _update_resource(self):
        general_section = {k:v for k,v in self._map[None].items()}
        other_sections = {k:v for k,v in self._map.items() if not k is None}

        config_content = ''
        for k,v in general_section.items():
            config_content += f'{k} = {v}\n'

        for section_name, section_map  in other_sections.items():
            config_content += f'\n[{section_name}]\n'
            for subkey, subval in section_map.items():
                config_content += f'{subkey} = {subval}\n'

        self.write(content=config_content)

    def read(self) -> str:
        if not os.path.isfile(self._config_fpath):
            raise ValueError(f'No file exists at configured config fpath {self._config_fpath}')

        with open(self._config_fpath, 'r') as f:
            content = f.read()
        if self.is_encrypted:
            content = self.aes.decrypt(content=content, key=self.masterpw_hash)

        return content

    def write(self, content : str):
        if self.is_encrypted:
            content = self.aes.encrypt(content=content, key=self.masterpw_hash)
        with open(self._config_fpath, 'w') as f:
            f.write(content)

    def retrieve_masterpw_hash(self) -> bytes:
        label_name ="masterpw"
        connection = secretstorage.dbus_init()
        collections = secretstorage.get_all_collections(connection)

        if not collections:
            raise KeyError("No keyring collections found.")

        master_pw_hash = None
        for collection in collections:
            items = collection.get_all_items()
            master_pw_matches = [i for i in items if i.get_label() == label_name]
            if master_pw_matches:
                master_pw_item = master_pw_matches[0]
                master_pw = master_pw_item.get_secret().decode('utf-8', errors='replace')
                master_pw_hash = self.sha.get_hash(txt=master_pw)

        connection.close()
        if master_pw_hash is None:
            raise KeyError(f'No password labeled "{label_name}" found in any keyring')

        return master_pw_hash

    @staticmethod
    def keyring_available() -> bool:
        try:
            connection = secretstorage.dbus_init()
            connection.close()
            return True
        except:
            return False


if __name__ == "__main__":
    master_pwd = FileConfigs(encrypted=True).retrieve_masterpw_hash()
    print(f'Master pw hash = {master_pwd}')
    creds = FileConfigs.credentials()

