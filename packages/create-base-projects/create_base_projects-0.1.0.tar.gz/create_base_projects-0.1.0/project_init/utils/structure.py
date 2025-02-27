import os
from rich import print

def create_project_structure(directories: list[str], 
                             files: list[str], dependencies: list[str]) -> None:
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"[blue]Directory created: {directory}[/blue]")
    
    for file in files:
        with open(file, 'w') as f:
            pass
        print(f"[blue]Created file: {file}[/blue]")
        
    with open(f"requirements.txt", "w") as f:
        for dependency in dependencies:
            f.write(f"{dependency}\n")
            
        print("[blue]Created requirements.txt with dependencies.[/blue]")
    
    print("[green]Project structure created.[/green]")