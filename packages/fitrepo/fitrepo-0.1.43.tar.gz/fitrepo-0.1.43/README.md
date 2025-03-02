# Fitrepo - Fossil Import Tool

Fitrepo is a command-line tool for managing Git repositories inside a Fossil repository.

## Usage

### Initializing a New Repository
```bash
pip install fitrepo
uv tool run fitrepo --help
```

## How to Use

Run the script from the directory where you want the Fossil repository (`monorepo.fossil`) and configuration file (`fitrepo.json`) to reside.

### Commands

1. **Initialize the Fossil Repository**
   ```bash
   uv tool run fitrepo init
   ```
   - Creates `monorepo.fossil` if it doesn’t exist.
   - Creates an empty `fitrepo.json` configuration file if it doesn’t exist.
   - Supports: `--help`, `--version`, `--verbose`, `--quiet`, `--config FILE`, `--force`, `--dry-run`

2. **Import a Git Repository**
   ```bash
   uv tool run fitrepo import <git-repo-url> <subdir-name>
   ```
   - Example: `uv tool run fitrepo import https://github.com/user/repo.git hotbox`
   - Clones the Git repository, moves its files into the `hotbox` subdirectory, prefixes its branches (e.g., `hotbox/master`), and imports it into the Fossil repository.
   - Stores configuration details in `fitrepo.json`.
   - Supports: `--help`, `--version`, `--verbose`, `--quiet`, `--config FILE`, `--no-fetch`, `--force`, `--dry-run`

3. **Update an Existing Git Repository**
   ```bash
   uv tool run fitrepo update <subdir-name>
   ```
   - Example: `uv tool run fitrepo update hotbox`
   - Pulls the latest changes from the Git repository associated with `hotbox`, reapplies the filters, and incrementally updates the Fossil repository.
   - Supports: `--help`, `--version`, `--verbose`, `--quiet`, `--config FILE`, `--no-fetch`, `--no-push`, `--force`, `--dry-run`

### Command-line Options

The tool supports several global options that can be used with any command:

- `--help`: Show help message and exit.
- `--version`: Show the version of the tool and exit.
- `--verbose`: Enable verbose output.
- `--quiet`: Suppress non-error messages.
- `--config FILE`: Specify a custom configuration file.
- `--no-fetch`: Do not fetch the latest changes from the remote repository.
- `--no-push`: Do not push changes to the remote repository.
- `--force`: Force the operation to proceed even if there are warnings or errors.
- `--dry-run`: Show what would be done without making any changes.

### Configuration File (`fitrepo.json`)

The tool maintains a `fitrepo.json` file to track imported repositories. Example content after importing a repository:

```json
{
    "hotbox": {
        "git_repo_url": "https://github.com/user/repo.git",
        "git_clone_path": ".git_clones/hotbox",
        "git_marks_file": ".marks/hotbox_git.marks",
        "fossil_marks_file": ".marks/hotbox_fossil.marks"
    }
}
```

## Features

- **Subdirectory Organization**: Each Git repository’s files are placed in a unique subdirectory within the Fossil repository.
- **Branch Prefixing**: Branches are renamed with the subdirectory name as a prefix (e.g., `master` becomes `hotbox/master`).
- **Incremental Updates**: Uses marks files to ensure only new changes are imported during updates.
- **Error Handling**: Provides informative error messages for common issues (e.g., duplicate subdirectory names, command failures).
- **User Feedback**: Logs progress and errors to the console.

## Requirements

- **Python 3.12+**
- **Git**
- **git-filter-repo** (automatically installed as a dependency)
- **Fossil** (installed and accessible from the command line)

## Notes

- Run the tool in the directory where you want `monorepo.fossil` to reside.
- The tool assumes `.git_clones/` and `.marks/` directories are subdirectories of the current working directory.
- Only branches are prefixed; tags retain their original names. To prefix tags, modify the `refname_rewriter` string in the code.

This implementation fulfills your intention to create a CLI tool that seamlessly manages multiple Git repositories within a single Fossil repository, with isolated subdirectories and prefixed branches.