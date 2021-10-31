import subprocess

print(subprocess.check_output(['node', 'pokemon-showdown', 'help'], cwd="pokemon-showdown"))
