import subprocess

def get_default_branch():
    try:
        result = subprocess.run(
            ['git', 'symbolic-ref', 'refs/remotes/origin/HEAD'],
            capture_output=True,
            text=True,
            check=True,
        )
        # Extract the branch name after "refs/remotes/origin/"
        return result.stdout.strip().split('/')[-1]
    except subprocess.CalledProcessError:
        raise RuntimeError("Unable to determine the default branch.")

def main():
    default_branch = get_default_branch()
    try:
        result = subprocess.run(
            ['git', 'log', f'origin/{default_branch}..HEAD', '--pretty=%s'],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Command failed: {e.cmd}\nReturn code: {e.returncode}\n"
            f"Stdout: {e.stdout}\nStderr: {e.stderr}"
        ) from e

if __name__ == "__main__":
    main()