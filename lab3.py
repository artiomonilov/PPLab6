import os

class AudioFile:
    ext = ""
    def __init__(self, filepath):
        if not filepath.endswith(self.ext):
            raise Exception("Format invalid")
        self.filepath = filepath
    
    def validate(self):
        print(f"Fisierul {self.filepath} a fost validat ca {self.ext}")

class MP3File(AudioFile):
    ext = ".mp3"

class WAVFile(AudioFile):
    ext = ".wav"

class OGGFile(AudioFile):
    ext = ".ogg"

class FLACFile(AudioFile):
    ext = ".flac"

def validate_audio_file(filepath):
    if not os.path.exists(filepath):
        print(f"Eroare: Fisierul '{filepath}' nu exista pe disk.")
        return

    ext = os.path.splitext(filepath)[1].lower()
    
    try:
        if ext == ".mp3":
            f = MP3File(filepath)
        elif ext == ".wav":
            f = WAVFile(filepath)
        elif ext == ".ogg":
            f = OGGFile(filepath)
        elif ext == ".flac":
            f = FLACFile(filepath)
        else:
            print(f"Eroare: Formatul {ext} nu este suportat pentru '{filepath}'.")
            return
        
        f.validate()
    except Exception as e:
        print(f"Eroare la procesarea fisierului {filepath}: {e}")

if __name__ == "__main__":
    print("Validare Fisiere Audio")
    while True:
        path = input("Introduceti calea catre fisierul audio (sau 'q' pentru ieșire): ")
        if path.lower() == 'q':
            break
        validate_audio_file(path)