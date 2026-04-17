import os
import struct
import re

class GenericFile:
    def get_path(self):
        raise NotImplementedError("Metoda get_path trebuie implementata in clasa copil.")
        
    def get_freq(self):
        raise NotImplementedError("Metoda get_freq trebuie implementata in clasa copil.")


class TextASCII(GenericFile):
    def __init__(self, path_absolut, frecvente):
        self.path_absolut = path_absolut
        self.frecvente = frecvente

    def get_path(self):
        return self.path_absolut

    def get_freq(self):
        return self.frecvente


class TextUNICODE(GenericFile):
    def __init__(self, path_absolut, frecvente):
        self.path_absolut = path_absolut
        self.frecvente = frecvente

    def get_path(self):
        return self.path_absolut

    def get_freq(self):
        return self.frecvente


class Binary(GenericFile):
    def __init__(self, path_absolut, frecvente):
        self.path_absolut = path_absolut
        self.frecvente = frecvente

    def get_path(self):
        return self.path_absolut

    def get_freq(self):
        return self.frecvente


class XMLFile(TextASCII):
    def __init__(self, path_absolut, frecvente, first_tag):
        super().__init__(path_absolut, frecvente)
        self.first_tag = first_tag

    def get_first_tag(self):
        return self.first_tag


class BMP(Binary):
    def __init__(self, path_absolut, frecvente, width, height, bpp):
        super().__init__(path_absolut, frecvente)
        self.width = width
        self.height = height
        self.bpp = bpp

    def show_info(self):
        print(f"[-] BMP Gasit:\n    Cale: {self.get_path()}\n    Dimensiuni: {self.width}x{self.height}\n    Bits Per Pixel: {self.bpp}")


def get_frequencies(content):
    """Calculeaza frecventa fiecarui octet intre 0 si 255 ca procent."""
    freq = {i: 0 for i in range(256)}
    total_bytes = len(content)
    
    if total_bytes == 0:
        return freq

    for byte in content:
        freq[byte] += 1
        
    for i in range(256):
        freq[i] = freq[i] / total_bytes
        
    return freq


def determine_file_type(path_absolut, content):
    """Creeaza obiectul corespunzator clasei de fisier in functie de context."""
    if len(content) == 0:
        return None
        
    freq = get_frequencies(content)
    
    # Conditie pentru UNICODE/UTF16 - caracterul 0 (NULL byte) apare des
    if freq[0] >= 0.30:
        return TextUNICODE(path_absolut, freq)
    
    # Setul de caractere ASCII considerate "frecvente" conform cerintei
    # {9, 10, 13, 32...127}
    ascii_common = set([9, 10, 13] + list(range(32, 128)))
    
    # Calculam probabilitatea sa fie text ASCII
    ascii_freq_sum = sum(freq[i] for i in ascii_common)
    
    if ascii_freq_sum > 0.85: # Peste 85% din continut e ASCII valid
        text_str = content.decode('ascii', errors='ignore')
        # Cautam daca are tag-uri XML/HTML (ex. <tag>)
        xml_match = re.search(r'<([a-zA-Z0-9_\-]+)[^>]*>', text_str)
        
        if xml_match:
            first_tag = xml_match.group(0)
            return XMLFile(path_absolut, freq, first_tag)
        else:
            return TextASCII(path_absolut, freq)
            
    # Daca a picat toate testele de text, o clasificam ca fisier Binar
    # Testam identificatorii pentru BMP Header. Începe cu "BM"
    if content.startswith(b'BM') and len(content) >= 30:
        try:
            # struct.unpack parcurge octetii header-ului BMP
            # offset 18 -> Width (4 bytes int), offset 22 -> Height (4 bytes int)
            width, height = struct.unpack('<ii', content[18:26])
            
            # offset 28 -> bpp (2 bytes short)
            bpp = struct.unpack('<H', content[28:30])[0]
            
            return BMP(path_absolut, freq, width, height, bpp)
        except Exception:
            pass
            
    return Binary(path_absolut, freq)


def scan_directory(directory_path="."):
    """Parcurge recursiv si scaneaza cu os.walk()"""
    root_dir = os.path.abspath(directory_path)
    print(f"Scanam directorul {root_dir}...")
    
    for root, subdirs, files in os.walk(root_dir):
        # Ignoram folderele git etc. pentru simplitate in afisaje
        if '.git' in root:
            continue
            
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                # deschide fișierul spre acces binar
                try:
                    f = open(file_path, 'rb')
                    content = f.read()
                    f.close()
                    
                    # Filtram continutul si obtinem instanta corespunzatoare
                    file_obj = determine_file_type(file_path, content)
                    
                    if file_obj is None:
                        continue
                        
                    # Verificam clasele asa cum cere problema, utilizand 'isinstance'
                    if isinstance(file_obj, XMLFile):
                        print(f"[-] XML ASCII Gasit:\n    Cale: {file_obj.get_path()}\n    First Tag: {file_obj.get_first_tag()}")
                    elif type(file_obj) is TextUNICODE:
                        print(f"[-] UNICODE Gasit:\n    Cale: {file_obj.get_path()}")
                    elif isinstance(file_obj, BMP):
                        file_obj.show_info()
                        
                except Exception as e:
                    pass

if __name__ == "__main__":
    scan_directory(os.path.dirname(os.path.abspath(__file__)))
