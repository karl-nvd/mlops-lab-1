# Lab 1 Answers

## Question 1

`uv init` created the basic Python project structure. `.python-version` chooses the Python version, `pyproject.toml` contains the project settings and dependencies, `src/` contains the code, and `README.md` is the project documentation.

## Question 2

`dvc init` created these main files:

- `.dvc/config` stores the DVC project configuration and remote settings.
- `.dvc/.gitignore` keeps the local DVC cache out of Git.
- `.dvcignore` tells DVC which files to ignore.

These small configuration files should be pushed to Git. The DVC cache and the actual dataset should not be pushed to Git.

## Question 3

With `--global`, the credentials are stored in DVC's global configuration outside the repository. The other options are `--local`, `--project`, and `--system`. Credentials should never be pushed to GitHub because they are private.

## Question 4

After I ran `dvc add data`, DVC added `/data` to `.gitignore`. This stops Git from tracking all the image files because DVC is responsible for them.

## Question 5

Yes, DVC created `data.dvc`. It is a small pointer file containing the dataset hash, size, file count, and the path `data`. Git tracks this file instead of tracking the actual images.

## Question 6

The source code and `data.dvc` pointer are visible on GitHub, but the real `data/` folder is not. The actual dataset is visible on DAGsHub because `dvc push` uploaded it to the DVC remote.

## Question 7

After cloning the GitHub repository into a new folder, the dataset is not there because Git only has the DVC pointer. Running `dvc pull` downloads the real data from DAGsHub.

## Question 8

Right after checking out the older Git commit, the processed folders were still on disk because Git does not manage them. After running `dvc checkout`, DVC matched the data to the old `data.dvc` version, so the processed folders disappeared and only the raw dataset remained.
