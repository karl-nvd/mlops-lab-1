# mlops-lab-1
Q1 : uv init created a basic Python project structure
.python-version: specifies the Python version to use, currently Python 3.13.
pyproject.toml: the main project configuration file. It contains:
Project name and version
Python version requirement
Project description
Dependencies list
Build system configuration
A command-line entry point
src: source-code directory for the project.
README.md: basic project documentation file.

Q2 : Created Files & Purpose:
.dvc/config: Stores DVC project settings and remote storage locations.
.dvc/.gitignore: Prevents Git from tracking DVC's local cache (.dvc/cache/).
.dvcignore: Tells DVC which local files to ignore.

Which to push to Git?

Push all three files (.dvc/config, .dvc/.gitignore, .dvcignore). They are small metadata text files that team members need to pull datasets.
Do NOT push .dvc/cache/ or actual raw datasets—Git tracks code and configs, while DVC tracks data.

Q3 : Where are credentials stored?
In a global file on your computer (outside the project folder), so they stay private to your machine.

Options other than --global:
--local: Saves in .dvc/config.local (kept on your PC, ignored by Git).
--project: Saves in .dvc/config (inside the project).
--system: Saves system-wide for every user on the PC.

Should credentials be pushed to GitHub?
NO. Never push passwords or tokens to GitHub, as anyone could access your account.

Q4 : When I ran dvc add data, DVC automatically updated .gitignore by adding data to it. This ensures Git ignores the raw dataset folder so we don't accidentally push thousands of heavy image files to our GitHub repository.

Q5 : Yes, a data.dvc file was created in the project root. It's a small tracking file that Git uses as a pointer instead of storing the real dataset. Looking inside, it contains an MD5 hash (a3a457d03c51ff8b037a833440f6ad13.dir) representing the directory version, the total size of 1,188,442,712 bytes (around 1.18 GB), the total file count of 16,643 files, and the relative path data pointing to the folder being tracked.

Q6 : all the source code and configuration files are present on GitHub, but the raw data/ folder is not there because .gitignore excludes it. Instead, GitHub has the data.dvc file, which acts as the pointer by storing the dataset's hash and file details. On the DAGsHub web UI, the actual dataset is visible because dvc push uploaded the raw files directly to DAGsHub's remote storage.

Q7 : No, the data/ folder is not there after cloning the repository because Git only tracked the lightweight data.dvc pointer file instead of the actual images. To pull the dataset down from DAGsHub remote storage into the local project folder, you run dvc pull.

Q8 : Right after running git checkout 1e8af6f: Yes, I can still see food11_processed and food11_processed_mini in the data/ folder. Git only tracked the data.dvc pointer file and ignored the actual data directories via .gitignore, so switching Git branches leaves the untracked physical files on the hard drive untouched.

After running dvc checkout: No, the folders disappear. Running dvc checkout forces DVC to sync the local workspace with the older data.dvc pointer file, leaving only food11_raw.
