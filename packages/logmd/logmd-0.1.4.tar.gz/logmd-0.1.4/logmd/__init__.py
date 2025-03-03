import httpx
import multiprocessing
from multiprocessing import Queue
import time 
import hashlib 
import atexit
from io import StringIO
import ase.io
from openmm import unit
import ase.io
from io import StringIO
import json 
import os 
import random 

# Linux/Mac/Windows compatible path. 
token_path = os.path.expanduser("~/.logmd_token")
dev = False 
base_url = 'https://rcsb.ai' if not dev else 'http://localhost:5173'

class LogMD:
    def __init__(self, num_workers=3, project='', template='', interval=100):
        t0 = time.time()
        self.frame_num = 0
        self.interval = interval
        self.project = project
        self.token = None

        self.adjectives = open('logmd/names.txt', 'r').read().split('\n')[0].split(' ')
        self.nouns = open('logmd/names.txt', 'r').read().split('\n')[1].split(' ')

        if template != '': self.template = ase.io.read(template) # for openmm

        # if no token => not logged in, log publically. 
        # if no project => don't need to be logged in, log publically. 
        self.logged_in = os.path.exists(token_path) and self.project != ''
        if self.logged_in:
            if os.path.exists(token_path):
                try:
                    self.load_token() 
                except:
                    print(f'\033[90m[\033[32mlogmd\033[90m] token file is corrupted, please login again')
                    LogMD.setup_token()
                    self.load_token()
            else: 
                LogMD.setup_token()
                self.load_token()

        # Upload using multiple processes
        self.upload_queue = Queue()
        self.status_queue = Queue()
        self.num_workers = num_workers
        self.upload_processes = []
        
        for _ in range(self.num_workers):
            process = multiprocessing.Process(
                target=self.upload_worker_process,
                args=(self.upload_queue, self.status_queue, self.token, self.project)
            )
            process.start()
            self.upload_processes.append(process)
        
        self.num = self.num_files() + 1

        # Generate sha hash.
        if self.logged_in: 
            i, j = random.randint(0, len(self.adjectives) - 1), random.randint(0, len(self.nouns) - 1)
            self.run_id = f'{self.adjectives[i]}-{self.nouns[j]}-{self.num}'
            self.url = f'{base_url}/logmd/{self.project}/' + self.run_id
        else: 
            self.run_id = hashlib.sha256(str(time.time()).encode()).hexdigest()[:8]
            self.url = f'{base_url}/logmd/' + self.run_id
        
        # Print init message with run id. 
        print(f'\033[90m[\033[32mlogmd\033[90m] \033[90mload_time=\033[34m{time.time()-t0:.2f}s\033[90m\033[0m ')
        print(f'\033[90m[\033[32mlogmd\033[90m] \033[90mid=\033[34m{self.run_id}\033[90m\033[0m 🚀')
        print(f'\033[90m[\033[32mlogmd\033[90m] \033[90murl=\033[34m{self.url}\033[90m\033[0m 🚀')
        
        # Cleanup asynch processes when python exists. 
        atexit.register(self.cleanup)

    def load_token(self):
        with open(token_path, 'r') as token_file: 
            self.token = json.load(token_file)

    @staticmethod
    def setup_token():
        print(f'\033[90m[\033[32mlogmd\033[90m] login here: \033[34mhttps://{base_url}/auth')
        token = input()
        with open(token_path, 'w') as token_file: 
            token_file.write(token)


    def cleanup(self):
        print(f'\033[90m[\033[32mlogmd\033[90m] finishing uploads (if >5s open issue https://github.com/log-md/logmd)')

        # Send termination signal to all worker processes
        for _ in range(self.num_workers):
            self.upload_queue.put(None)
        for process in self.upload_processes:
            process.join()
        print(f'\033[90m[\033[32mlogmd\033[90m] id=\033[34m{self.url}\033[0m ✅')

    @staticmethod
    def upload_worker_process(upload_queue: Queue, status_queue: Queue, token: dict, project: str):
        """Worker process that handles uploads"""
        client = httpx.Client(timeout=180)  
        
        while True:
            item = upload_queue.get()  
            if item is None:  break
            atom_string, frame_num, run_id, energy = item

            if dev: url = "https://alexander-mathiasen--logmd-upload-frame-dev.modal.run"
            else: url = "https://alexander-mathiasen--logmd-upload-frame.modal.run"

            data = {
                "user_id": "public" if token is None else token['email'],
                "run_id": run_id,
                "frame_num": frame_num,
                "energy": str(energy),
                "file_contents": atom_string,
                "token": None if token is None else token['token'] ,
                "project": project 
            }

            response = client.post(url, json=data)
            status_queue.put((frame_num, response.status_code))
        
        client.close()

    # for openmm
    def describeNextReport(self, simulation):
        steps = self.interval 
        return (steps, True, True, True, False)
    # for openmm
    def report(self, simulation, state):
        """ Method openmm calls: simulation.reporters.append(LogMD(template='1crn.pdb', interval=100)). """
        self.template.positions = state.getPositions(asNumpy=True).value_in_unit(unit.angstrom) 
        self.__call__(self.template)

    # for ase 
    def __call__(self, atoms):
        """Method ASE calls:  dyn.attach(logmd) """
        self.frame_num += 1
        
        if atoms.calc is not None: energy = float(atoms.get_potential_energy())
        else: energy = 0

        temp_pdb = StringIO()
        ase.io.write(temp_pdb, atoms, format='proteindatabank')
        atom_string = temp_pdb.getvalue()
        temp_pdb.close()

        self.upload_queue.put((atom_string, self.frame_num, self.run_id, energy))

    def num_files(self):
        """Returns the number of files in the current project."""
        if not self.logged_in:
            print("Not logged in. Cannot list project files.")
            return 0

        url = "https://alexander-mathiasen--logmd-list-project-dev.modal.run"  # Replace with the actual URL
        data = {
            "user_id": self.token['email'],
            "token": self.token['token'],
            "project": self.project
        }

        try:
            response = httpx.post(url, json=data)
            if response.status_code == 200:
                result = response.json()
                if "projects" in result:
                    return len(result["projects"]) 
                else:
                    print("Error:", result.get("error", "Unknown error"))
            else:
                print(f"Failed to list project files with status {response.status_code}: {response.text}")
        except Exception as e:
            print("Error while listing project files:", str(e))

        return 0
