import os
from pathlib import Path
from shutil import move, unpack_archive
from re import sub

def normalise(string):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    TRANS = {}

    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

    string = string.translate(TRANS)
    string = sub(r"\W+", "_", string)

    return string

def sort():
    folder = Path("")
    if not os.path.isdir(folder):
        os.mkdir(folder)
    os.makedirs(folder / "images", exist_ok=True)
    os.makedirs(folder / "video", exist_ok=True)
    os.makedirs(folder / "documents", exist_ok=True)
    os.makedirs(folder / "audio", exist_ok=True)
    os.makedirs(folder / "archives", exist_ok=True)
    
    images = []
    video = []
    documents = []
    audio = []
    archives = []
    known_extensions = set()
    unknown_extensions = set()

    for f in folder.rglob("*.*"):
        if os.path.commonpath([folder / "archives"]) == os.path.commonpath([folder / "archives", f]):
            continue
        elif os.path.commonpath([folder / "audio"]) == os.path.commonpath([folder / "audio", f]):
            continue
        elif os.path.commonpath([folder / "documents"]) == os.path.commonpath([folder / "documents", f]):
            continue
        elif os.path.commonpath([folder / "images"]) == os.path.commonpath([folder / "images", f]):
            continue
        elif os.path.commonpath([folder / "video"]) == os.path.commonpath([folder / "video", f]):
            continue
        
        if f.suffix in ['.jpeg', '.png', '.jpg', '.svg']:
            images.append(f.name)
            known_extensions.add(f.suffix)
            move(f, folder / "images")
        elif f.suffix in ['.avi', '.mp4', '.mov', '.mkv']:
            video.append(f.name)
            known_extensions.add(f.suffix)
            move(f, folder / "video")
        elif f.suffix in ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx']:
            documents.append(f.name)
            known_extensions.add(f.suffix)
            move(f, folder / "documents")
        elif f.suffix in ['.mp3', '.ogg', '.wav', '.amr']:
            audio.append(f.name)
            known_extensions.add(f.suffix)
            move(f, folder / "audio")
        elif f.suffix in ['.zip', '.gz', '.tar']:
            archives.append(f.name)
            known_extensions.add(f.suffix)
            unpack_archive(f, folder / "archives" / f.name.rsplit(".")[0])
            f.unlink()
        else:
            unknown_extensions.add(f.suffix)

    for root, dirs, files in os.walk(folder, topdown=False):
        for file in files:
            split_file = file.rsplit(".")
            trans_file = normalise(split_file[0])
            file_name = os.path.join(root, file)
            file_rename = os.path.join(root, (f"{trans_file}.{split_file[1]}"))
            os.rename(file_name, file_rename)
        for dir in dirs:
            if not os.listdir(os.path.join(root, dir)):
                os.rmdir(os.path.join(root, dir))
                continue
            trans_dir = normalise(dir)
            dir_name = os.path.join(root, dir)
            dir_rename = os.path.join(root, trans_dir)
            os.rename(dir_name, dir_rename)
            
    print(f"Images: {images}")
    print(f"Video: {video}")
    print(f"Documents: {documents}")
    print(f"Audio: {audio}")
    print(f"Archives: {archives}")
    print(f"All known extensions in the target folder: {known_extensions}")
    print(f"All unknown extensions in the target folder: {unknown_extensions}")

if __name__ == "__main__":
    sort()
