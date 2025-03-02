#!/usr/bin/env python3

# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "gitpython",
#   "tqdm",
#   "transformers",
#   "rich",
# ]
# ///

import os
import sys
import shutil
import tempfile
import warnings
from pathlib import Path
from typing import Dict, List, Tuple

# Set environment variable to suppress transformers warnings
os.environ['TRANSFORMERS_VERBOSITY'] = 'error'

from git import Repo
from tqdm import tqdm
from transformers import AutoTokenizer
from rich.console import Console
from rich.table import Table
from rich.progress import track
from rich import print as rprint

# Initialize the console and tokenizer
warnings.filterwarnings('ignore')
console = Console()
tokenizer = AutoTokenizer.from_pretrained("gpt2")

# File extensions mapped to their technologies
FILE_EXTENSIONS = {
    # Python and related
    '.py': 'Python',
    '.pyi': 'Python Interface',
    '.pyx': 'Cython',
    '.pxd': 'Cython Header',
    '.ipynb': 'Jupyter Notebook',
    '.requirements.txt': 'Python Requirements',
    '.pipfile': 'Python Pipenv',
    '.pyproject.toml': 'Python Project',
    '.txt': 'Plain Text',
    '.md': 'Markdown',

    # Web Technologies
    '.html': 'HTML',
    '.htm': 'HTML',
    '.css': 'CSS',
    '.scss': 'SASS',
    '.sass': 'SASS',
    '.less': 'LESS',
    '.js': 'JavaScript',
    '.jsx': 'React JSX',
    '.ts': 'TypeScript',
    '.tsx': 'React TSX',
    '.vue': 'Vue.js',
    '.svelte': 'Svelte',
    '.php': 'PHP',
    '.blade.php': 'Laravel Blade',
    '.hbs': 'Handlebars',
    '.ejs': 'EJS Template',
    '.astro': 'Astro',

    # System Programming
    '.c': 'C',
    '.h': 'C Header',
    '.cpp': 'C++',
    '.hpp': 'C++ Header',
    '.cc': 'C++',
    '.hh': 'C++ Header',
    '.cxx': 'C++',
    '.rs': 'Rust',
    '.go': 'Go',
    '.swift': 'Swift',
    '.m': 'Objective-C',
    '.mm': 'Objective-C++',

    # JVM Languages
    '.java': 'Java',
    '.class': 'Java Bytecode',
    '.jar': 'Java Archive',
    '.kt': 'Kotlin',
    '.kts': 'Kotlin Script',
    '.groovy': 'Groovy',
    '.scala': 'Scala',
    '.clj': 'Clojure',

    # .NET Languages
    '.cs': 'C#',
    '.vb': 'Visual Basic',
    '.fs': 'F#',
    '.fsx': 'F# Script',
    '.xaml': 'XAML',

    # Shell and Scripts
    '.sh': 'Shell Script',
    '.bash': 'Bash Script',
    '.zsh': 'Zsh Script',
    '.fish': 'Fish Script',
    '.ps1': 'PowerShell',
    '.bat': 'Batch File',
    '.cmd': 'Windows Command',
    '.nu': 'Nushell Script',

    # Ruby and Related
    '.rb': 'Ruby',
    '.erb': 'Ruby ERB Template',
    '.rake': 'Ruby Rake',
    '.gemspec': 'Ruby Gem Spec',

    # Other Programming Languages
    '.pl': 'Perl',
    '.pm': 'Perl Module',
    '.ex': 'Elixir',
    '.exs': 'Elixir Script',
    '.erl': 'Erlang',
    '.hrl': 'Erlang Header',
    '.hs': 'Haskell',
    '.lhs': 'Literate Haskell',
    '.hcl': 'HCL (Terraform)',
    '.lua': 'Lua',
    '.r': 'R',
    '.rmd': 'R Markdown',
    '.jl': 'Julia',
    '.dart': 'Dart',
    '.nim': 'Nim',
    '.ml': 'OCaml',
    '.mli': 'OCaml Interface',

    # Configuration and Data
    '.json': 'JSON',
    '.yaml': 'YAML',
    '.yml': 'YAML',
    '.toml': 'TOML',
    '.ini': 'INI',
    '.conf': 'Configuration',
    '.config': 'Configuration',
    '.env': 'Environment Variables',
    '.properties': 'Properties',
    '.xml': 'XML',
    '.xsd': 'XML Schema',
    '.dtd': 'Document Type Definition',
    '.csv': 'CSV',
    '.tsv': 'TSV',

    # Documentation and Text
    '.md': 'Markdown',
    '.mdx': 'MDX',
    '.rst': 'reStructuredText',
    '.txt': 'Plain Text',
    '.tex': 'LaTeX',
    '.adoc': 'AsciiDoc',
    '.wiki': 'Wiki Markup',
    '.org': 'Org Mode',

    # Database
    '.sql': 'SQL',
    '.psql': 'PostgreSQL',
    '.plsql': 'PL/SQL',
    '.tsql': 'T-SQL',
    '.prisma': 'Prisma Schema',

    # Build and Package
    '.gradle': 'Gradle',
    '.maven': 'Maven POM',
    '.cmake': 'CMake',
    '.make': 'Makefile',
    '.dockerfile': 'Dockerfile',
    '.containerfile': 'Container File',
    '.nix': 'Nix Expression',

    # Web Assembly
    '.wat': 'WebAssembly Text',
    '.wasm': 'WebAssembly Binary',

    # GraphQL
    '.graphql': 'GraphQL',
    '.gql': 'GraphQL',

    # Protocol Buffers and gRPC
    '.proto': 'Protocol Buffers',

    # Mobile Development
    '.xcodeproj': 'Xcode Project',
    '.pbxproj': 'Xcode Project',
    '.gradle': 'Android Gradle',
    '.plist': 'Property List',

    # Game Development
    '.unity': 'Unity Scene',
    '.prefab': 'Unity Prefab',
    '.godot': 'Godot Resource',
    '.tscn': 'Godot Scene',

    # AI/ML
    '.onnx': 'ONNX Model',
    '.h5': 'HDF5 Model',
    '.pkl': 'Pickle Model',
    '.model': 'Model File',
}

# Set of all text extensions for quick lookup
TEXT_EXTENSIONS = set(FILE_EXTENSIONS.keys())

def is_binary(file_path: str) -> bool:
    """Check if a file is binary."""
    try:
        with open(file_path, 'tr') as check_file:
            check_file.read(1024)
            return False
    except UnicodeDecodeError:
        return True

def count_tokens(content: str) -> int:
    """Count tokens in the given content using GPT-2 tokenizer."""
    return len(tokenizer.encode(content))

def format_number(num: int) -> str:
    """Format a number with thousands separator and appropriate suffix."""
    if num >= 1_000_000_000:
        return f"{num/1_000_000_000:.1f}B"
    elif num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    return f"{num:,}"

def process_repository(repo_path: str, total_only: bool = False) -> Tuple[int, Dict[str, int], Dict[str, int]]:
    """Process all files in the repository and count tokens."""
    total_tokens = 0
    extension_stats = {}
    file_counts = {}

    # Define directories to exclude
    exclude_dirs = {'.git', 'venv', '.venv', '__pycache__', '.pytest_cache', '.mypy_cache'}

    # Get list of all files
    all_files = []
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            file_path = os.path.join(root, file)
            extension = os.path.splitext(file)[1].lower()
            if extension in FILE_EXTENSIONS and not is_binary(file_path):
                all_files.append((file_path, extension))
                file_counts[extension] = file_counts.get(extension, 0) + 1

    # Process files
    for file_path, extension in (track(all_files, description="[bold blue]Processing files") if not total_only else all_files):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                tokens = count_tokens(content)
                total_tokens += tokens
                if extension not in extension_stats:
                    extension_stats[extension] = tokens
                else:
                    extension_stats[extension] += tokens
        except Exception as e:
            if not total_only:
                console.print(f"[red]Error processing {file_path}: {str(e)}[/red]")

    return total_tokens, extension_stats, file_counts

def main():
    # Check for correct number of arguments
    if len(sys.argv) < 2:
        console.print("[red]Usage: token-counter <repository_url_or_path> [-total][/red]")
        sys.exit(1)
        
    # Check for -total flag
    total_only = "-total" in sys.argv
    target = sys.argv[1] if sys.argv[1] != "-total" else sys.argv[2]
    
    # Suppress all warnings if total_only is True
    if total_only:
        import logging
        logging.getLogger('transformers').setLevel(logging.ERROR)

    temp_dir = None

    # Check if the target is a local directory
    if os.path.isdir(target):
        if not total_only:
            console.print(f"[green]Analyzing local directory: {target}[/green]")
        analyze_path = target
    else:
        # Clone the repository to a temporary directory
        temp_dir = tempfile.mkdtemp()
        if not total_only:
            console.print(f"[yellow]Cloning t
    else console.piten:8les = '.ctarg_)
torectory, temporarokens = count_ {target}[/greenemporarn_stats[extension] += tokens
        except total_only:
               c   console.print(f"[or processing {f     except import.rmtloc(temporarokens = count_h> [-total][heck if a file is str(e)}[/red]")

    return total_tokens, ree
    return f"{num: {target}[/gss_repositor)
ts[extension] += tokens
        exc tempfile.mkdtemp()
        if not total_only:
           flows/testole.print(f"[or processing {f     excemp_emporar:f     except import.rmtloc(temporarokens = coh> [-total][heck .getrt ts):

!srnings if total_only is Truev
solymport tr inst    ():
  y is Truel_onlystr(e)}[/red)       analyze_path len(sys.argv) \nack(alcyan]utput (t[/ck(alcyan] {f     excnot total_only:
xt only):

```       {nizer.encode(cstr(e)}[/red)ing local ({str(e)}[/red000) {file_p tempfile.mkdtemp()
       ```

### Usinmparestom_pretrain le imn_stats[ext   e imp=nsole
(title= \nack(a]tokens: 5.9K (5,942)

  [/ck(a] {f     excxt   e im.addokelumn("”â”â”â",rocyle= cyan {f     excxt   e im.addokelumn("tokens",rjustify="right",rocyle=  loca {f     excxt   e im.addokelumn("ology",rjustify="right",rocyle= oning ")
rs if d not ixt , files g
  ernam()

    return t.   ms(), key=lambda x: xet .)
-ens e=l wa and not is_binxt   e im.addorow(
s
                e,pend((file_path, e"{nizer.encode(cfiles)} ({files000) ,pend((file_path, e"{nxtension))
   ]}.9K ({'s'p tenxtension))
   ]= sy1] if s''}"pend((file_pa{f     excnot total_onlyxt   e im)
rs if d n#Technots):

!stegorâ”â”â”cng bintory to a techtal_tokens = 0
 o a techt   extension_stats if d not ixt , files g
 )

    return t.   ms()and not is_bintech_pat           if 
   ]nd not is_bintech       tech   exech      nts[exech = filefilesnd not is_bintech nxtension))
tech   exech    file_counts[exech = filenxtension))
   ]
)
       ```

### Usinmparestomrâ”â”â”le imn_stats[exech  e imp=nsole
(title= \nack(a]tokens: 5.”â”â”â”[/ck(a] {f     excxech  e im.addokelumn("tâ”â”â”",rocyle= ”€â”nta {f     excxech  e im.addokelumn("tokens",rjustify="right",rocyle=  loca {f     excxech  e im.addokelumn("ology",rjustify="right",rocyle= oning ")
rs if d not ixech =files g
  ernam(xech      n   ms(), key=lambda x: xet .)
-ens e=l wa and not is_binxech  e im.addorow(
s
              xech pend((file_path, e"{nizer.encode(cfiles)} ({files000) ,pend((file_path, e"{tech nxtension))
tech }.9K ({'s'p tetech nxtension))
tech   sy1] if s''}"pend((file_pa{f     excnot total_onlyxech  e im)
)
       ```

### Usinmparestome types
- Inclle imn_stats[etage of echnolog is Truev
sr LLM contexnolog is True"”â”â”â”â": 4096,nolog is True"”â”‚     ": 8192,nolog is True"”â”‚  18.1": 32768,nolog is True"”â”‚         18.1":  18000,
nolog is Truev
.5, GPT-4, GPT-4nolog is True"  â”‚          ":     00,nolog is True"  â”‚          5.9% ": 2   00,nolog is True"  â”‚          3.0% â”": 2   00,nolog is True"  â”‚          3.0% â": 2   00,nnolog is Truev
e 2, Claude 3nolog is True"” â”‚          3": 32768,nolog is True"  â”‚      ": 8192,nnolog is Truev
ls (Gemini nolog is True"  â”‚       ": 4096,nolog is True"  â”‚        145.":     00,nnolog is Truev
s (Llama 2, nolog is True"  â”‚          5.9%": 32768,nolog is True"  â”‚         18.1": 32768,nolog is True"  â”‚        ": 2   00,nolog is True"  â”‚          3.0% â":  18000,
 is True}

ding='utf-8')t   e imp=nsole
(title= \nack(a]â”€â”€â”€â”€â”€â”˜

      [/ck(a] {f     excf-8')t   e im.addokelumn("ma 2,",rocyle= l_fi {f     excf-8')t   e im.addokelumn(" Model       ",rjustify="right")
rs if d not ipkl':,
- Inclg
 tage of.   ms()and not is_binpContext Wi= cstr(e)}[/red / tage o) *    )
        if nolory d"sin"p tepContext Wi>    ] if s  loca 
encoding='utf-8')t   e im.addorow(pkl':,
:
 {nolor}]{pContext W     %[/{nolor}] {f     excnot total_onlyf-8')t   e im{file_p te_emporar:f     excimport.rmtloc(temporarok
 te__ntern_co d"__ion___":f    ion_st       22 mtime=1740869882.0
