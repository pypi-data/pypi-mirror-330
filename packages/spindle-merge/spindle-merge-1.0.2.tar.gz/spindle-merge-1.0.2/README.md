# Spindle

Spindle is a command-line tool that merges multiple text files into a single output, making it easier to input into ChatGPT and similar AI tools. It supports wildcard patterns for flexible file selection and automatically reads a predefined file list from `SpindleLists.txt`.

## Features

- **Merge multiple files**  
  Combines multiple text files into one output file.

- **Wildcard support**  
  Selects target files using patterns such as `*.txt` or `*.py`.

- **Automatic file list loading**  
  Reads merge target file paths from `SpindleLists.txt` in the current directory.

- **Simple command-line interface**  
  Use the `-o` option to specify the output file; if omitted, the default is `spindle_output.txt`.

## Installation

### Install from PyPI (Future Release)

Once released on PyPI, Spindle can be installed using:

```bash
pip install spindle-merge
```

### Install from Source

To install from the GitHub repository, run:

```bash
git clone https://github.com/ll3ynxnj/spindle.git
cd spindle
pip install .
```

## Usage

### Prepare the file list

Create a `SpindleLists.txt` file in the current directory and list the file paths or wildcard patterns for merging, for example:

```txt
# Example list of files to merge
~/projects/example/file1.txt
~/projects/example/*.log
~/projects/example/subdir/*.txt
```

### Execute the merge

Run the following command:

```bash
spindle -o combined_output.txt
```

This merges the specified files into `combined_output.txt`.

### Clipboard Output

The merged text is also copied to the clipboard for easy pasting into AI tools.

### Check Help Options

For additional options, use:

```bash
spindle --help
```

## Contributing & License

### Contributing

Bug reports, feature requests, and pull requests are welcome on GitHub.

### License

This project is released under the MIT License. See the [LICENCE](./LICENCE) file for details.
