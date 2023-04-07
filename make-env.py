import time, os, string, shutil, sys

from os.path import join
from random import randbytes, randint, choice, choices
from os.path import exists
from PIL import Image

if len(sys.argv) != 2:
    print("Usage: python3 make-env.py <root directory name>")
    print("Example: python3 make-env.py fakeroot")
    exit()

root = sys.argv[1]

def randomstr(
    length: int,
    chars: str = string.ascii_letters
    ) -> str:

    return "".join(choices(chars, k=length))

class EnvMaker:
    def __init__(self, root):
        if not exists(root):
            os.mkdir(root)
        
        else:
            shutil.rmtree(root)
            os.mkdir(root)

        self.root = root
        self.filenames = []

        self.functions = [
            self.make_Jpg,
            self.make_Binary,
            self.make_Dir,
            self.make_Txt,
            self.make_Creds,
            self.make_big_binary,
            self.make_LoremIpsum,
            self.make_ProgramFiles
        ]

        # prevents infinite recursive loop
        self.recursive_limit = 3
        self.recursive_counter = 0

        self.indir = False
        self.maxdirs = 40

        # counters
        self.dirs_made = 0
        self.files_made = 0
    
    def make_Jpg(self, root):

        width = height = choice([32, 64, 128, 256])

        rand_pixels = [randint(0, 255) for _ in range(width * height * 3)]
        rand_pixels_as_bytes = bytes(rand_pixels)

        random_image = Image.frombytes('RGB', (width, height), rand_pixels_as_bytes)
        random_image.save(
            join(root, f"img_{int(time.time())}.jpg")
        )

        self.files_made += 1
    
    def make_Binary(self, root):

        if exists(join(root, "binary.bin")):
            return choice(self.functions)(root)

        contents = randbytes(
            randint(1024, 4096)
        )

        with open(join(root, "binary.bin"), "wb") as fd:
            fd.write(contents)
        
        self.files_made += 1
    
    def make_Dir(self, root, dirname=None):

        if self.dirs_made >= self.maxdirs:
            return

        if self.indir:
            if self.recursive_counter >= self.recursive_limit:
                return

            self.recursive_counter += 1

        self.indir = True

        if not dirname:
            dirname = randomstr(randint(3, 9))

        dir = join(root, dirname)
        if not exists(dir):
            os.mkdir(dir)

        for _ in range(randint(1, 7)):
            choice(self.functions)(dir)
        
        self.indir = False

        self.dirs_made += 1
    
    def make_Txt(self, root):

        with open(join(root, randomstr(5)+".txt"), "w+") as fd:
            fd.write(randomstr(512))
        
        self.files_made += 1
    
    def make_Creds(self, root):

        fname = choice([
            "bank.txt",
            "passwords.txt",
            "credentials.txt",
            "secure.txt",
            "passwords.note"
        ])

        # check if it already exists
        if not exists(join(root, fname)):

            with open(join(root, fname), "w+") as fd:
                for _ in range(randint(1, 7)):
                    username = randomstr(randint(3, 10), string.ascii_lowercase+string.digits,)
                    password = randomstr(randint(4, 10), string.ascii_letters+string.digits+string.punctuation)

                    fd.write(f"{username}:{password}\n")
            
            self.files_made += 1
    
    def make_big_binary(self, root):

        if exists(join(root, "bigbinary.bin")):
            return choice(self.functions)(root)

        size = randint(2, 10) # 2-10 mb
        blob = randbytes(size * 1024 * 1024)

        with open(join(root, "bigbinary.bin"), "wb") as fd:
            fd.write(blob)
        
        self.files_made += 1
    
    def make_LoremIpsum(self, root):

        with open(join(root, randomstr(5)+".txt"), "w+") as fd:
            fd.write("""Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum""")
        
        self.files_made += 1
    
    def make_Html(self, root):

        with open(join(root, randomstr(3)+".html"), "w+") as fd:
            fd.write("""<html>
<head>
    <title>lol</title>
</head>
<body>
    <h1>html go brrrr</h1>
</body>
</html>""")

        self.files_made += 1
    
    def make_ProgramFiles(self, root):

        dirname = choice(["program files", "program files (x86)"])
        self.make_Dir(root, dirname)
    
    def make(self):
        for _ in range(20):
            print(f"Files: {self.files_made+1} :: Dirs: {self.dirs_made+1} :: Recursive counter: {self.recursive_counter}")
            choice(self.functions)(self.root)
        
        print("\n::: RESULTS :::")
        print(f"- Files created: {self.files_made+1}")
        print(f"- Directories created: {self.dirs_made+1}")

if __name__ == "__main__":
    env = EnvMaker(root)
    env.make()