
# DirScope

**A lightweight directory analysis tool built with Python.**

DirScope is a command-line utility that inspects a directory and generates a
summary of its contents. It reports file counts, directory counts, file type
distribution, total storage usage, and the largest files found during a scan.

Designed to be simple, portable, and dependency-free.

## Features

- **Directory statistics** — Count files and directories recursively.
- **File type breakdown** — Group files by extension and calculate their sizes.
- **Largest file detection** — Identify the largest files in a directory tree.
- **Human-readable output** — Display sizes in bytes, KB, MB, GB, or TB.
- **JSON export** — Produce machine-readable reports for other tools.
- **Safe scanning** — Does not modify or delete files.
- **No dependencies** — Uses only the Python standard library.
- **Error handling** — Handles missing paths and inaccessible entries.

## Requirements

- Python 3.10 or newer
- Windows, macOS, or Linux

No third-party packages are required.

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/dirscope.git
cd dirscope
```

Alternatively, download `dirscope.py` directly.

## Usage

Analyze the current directory:

```bash
python dirscope.py
```

Analyze a specific directory:

```bash
python dirscope.py ./my-project
```

Display the top 20 entries in each report section:

```bash
python dirscope.py ./my-project --top 20
```

Export the complete report as JSON:

```bash
python dirscope.py ./my-project --json
```

Check the installed script version:

```bash
python dirscope.py --version
```

Display available options:

```bash
python dirscope.py --help
```

## Example Output

```text
DirScope — Directory Analysis
======================================
Location     : /home/user/my-project
Files        : 148
Directories  : 23
Total size   : 18.4 MB
Skipped      : 0

FILE TYPES
----------------------------------------------------
Extension               Count     Total size
.py                        32        1.8 MB
.json                     21        2.1 MB
.md                        15      124.0 KB
.png                       12        8.3 MB
.txt                       10      256.0 KB

LARGEST FILES
----------------------------------------------------
 1.     4.2 MB  assets/banner.png
 2.     2.8 MB  data/archive.json
 3.     1.6 MB  assets/preview.png

Analysis complete. No files were modified.
```

*Output above is illustrative; actual results depend on the directory scanned.*

## JSON Output

The `--json` option outputs the full report, including all file types and
the largest-file list.

Example:

```json
{
  "root": "/home/user/my-project",
  "summary": {
    "total_files": 148,
    "total_directories": 23,
    "total_size_bytes": 19293798,
    "total_size": "18.4 MB",
    "skipped_entries": 0
  },
  "file_types": [],
  "largest_files": []
}
```

The empty arrays are illustrative placeholders. Actual output includes the
collected file type statistics and file entries.

## How It Works

DirScope traverses the specified directory tree, gathers file metadata,
groups files by extension, and sorts files by size.

Symbolic links are excluded from file results, and symbolic-link directories
are not traversed. Entries that cannot be accessed may be skipped.

The tool reads filesystem metadata rather than opening file contents.
Scan duration depends on the size of the directory tree and the underlying
storage device.

## Limitations

- Hidden files are included when accessible.
- Symbolic links are excluded.
- File sizes represent reported filesystem sizes, not necessarily physical
  disk usage.
- Results may be incomplete when filesystem permissions prevent access.
- The tool does not calculate checksums or inspect file contents.

## Project Structure

```text
dirscope/
├── dirscope.py
└── README.md
```

## License

This project is released under the MIT License.

If you intend to distribute the project publicly, add a separate `LICENSE`
file containing the full MIT License text.

## Contributing

Bug reports, improvements, and feature suggestions are welcome.
Keep the project dependency-free and maintain compatibility with Python 3.10+.

## Author

Your Name

GitHub: https://github.com/YOUR_USERNAME
```

---

## 3. Run it locally

<box border radius="lg" padding={3} gap={3}>
  <row align="start" gap={3}>
    <icon name="terminal" size="xl" color="#16A34A"/>
    <box flex="1" gap={1}>
      **Step 1 — Create the files**

      Save the two code blocks as `dirscope.py` and `README.md` in the same folder.
    </box>
  </row>
  <divider color="subtle"/>
  <row align="start" gap={3}>
    <icon name="play" size="xl" color="#16A34A"/>
    <box flex="1" gap={1}>
      **Step 2 — Run the tool**

      ```bash
      python dirscope.py .
      ```
    </box>
  </row>
  <divider color="subtle"/>
  <row align="start" gap={3}>
    <icon name="check-circle" size="xl" color="#16A34A"/>
    <box flex="1" gap={1}>
      **Step 3 — Test JSON output**

      ```bash
      python dirscope.py . --json
      ```
    </box>
  </row>
</box>

**To make the repository look polished:** replace `YOUR_USERNAME` with your actual GitHub username, verify the commands on your machine, and add a real MIT license if you plan to publish it. The project deliberately stays at exactly two files for now.
