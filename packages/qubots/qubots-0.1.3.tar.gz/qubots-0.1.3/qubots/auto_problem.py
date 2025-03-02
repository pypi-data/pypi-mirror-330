import os
import sys
import subprocess
import json
import importlib
from pathlib import Path
from typing import Optional

class AutoProblem:
    """
    Similar approach as AutoOptimizer, but for 'problem_config.json'
    which references 'entry_point': 'module:ClassName'.
    """

    @classmethod
    def from_repo(
        cls,
        repo_id: str,
        revision: str = "main",
        cache_dir: str = "~/.cache/rastion_hub",
        override_params: Optional[dict] = None  
    ):
        cache_dir = os.path.expanduser(cache_dir)
        os.makedirs(cache_dir, exist_ok=True)

        local_repo_path = cls._clone_or_pull(repo_id, revision, cache_dir)

        # Install dependencies from requirements.txt if it exists
        req_file = Path(local_repo_path) / "requirements.txt"
        if req_file.is_file():
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(req_file)], check=True)

        # Load problem configuration
        config_path = Path(local_repo_path) / "problem_config.json"
        if not config_path.is_file():
            raise FileNotFoundError(f"No problem_config.json found in {config_path}")

        with open(config_path, "r") as f:
            config_data = json.load(f)

        entry_point = config_data.get("entry_point")
        if not entry_point or ":" not in entry_point:
            raise ValueError("Invalid 'entry_point' in problem_config.json. Must be 'module:ClassName'.")

        problem_params = config_data.get("default_params", {})

        if override_params:
            problem_params = {**problem_params, **override_params}

        # Dynamic import and instantiate the problem class
        module_path, class_name = entry_point.split(":")
        if str(local_repo_path) not in sys.path:
            sys.path.insert(0, str(local_repo_path))

        mod = importlib.import_module(module_path)
        ProblemClass = getattr(mod, class_name)

        problem_instance = ProblemClass(**problem_params)
        return problem_instance
    

    @staticmethod
    def _clone_or_pull(repo_id: str, revision: str, cache_dir: str) -> str:
        owner, repo_name = repo_id.split("/")
        repo_url = f"https://github.com/{owner}/{repo_name}.git"
        local_repo_path = os.path.join(cache_dir, repo_name)

        if not os.path.isdir(local_repo_path):
            # Clone the repository
            subprocess.run(["git", "clone", "--branch", revision, repo_url, local_repo_path], check=True)
        else:
            # Attempt to clean up any merge conflicts first.
            subprocess.run(["git", "fetch", "--all"], cwd=local_repo_path, check=True)
            # Abort any in-progress merge if needed (ignore errors if not in merge state)
            subprocess.run(["git", "merge", "--abort"], cwd=local_repo_path, check=False)
            # Force checkout and reset
            subprocess.run(["git", "checkout", "-f", revision], cwd=local_repo_path, check=True)
            subprocess.run(["git", "reset", "--hard", f"origin/{revision}"], cwd=local_repo_path, check=True)

        return local_repo_path
