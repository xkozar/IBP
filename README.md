# Parsing for ET0L systems

This is implementation part of my **bachelor thesis**. It includes two types of parsing algorithms. First type is based on Cocke-Younger-Kasami parsing algorithm. Second one is based on top-down principle.

Both variations are implemented for **context-free grammars**, **E0L** and **ET0L** systems.

## Prerequisites

Only thing you need to run these parsers is [**Python 3+**](https://www.python.org/downloads/).

## Contents

- **_src/_**
    contains all of the source files
- **_src/test-rules/_**
    production rules used for testing
- **_src/misc-rules/_**
    miscellaneous production rules that can be used for playing with parsers
- **_src/parser&ast;.py_**
    Implementations of parsers based on Cocke-Younger-Kasami parsing algorithm
- **_src/topDownParser&ast;.py_**
    Implementations of parsers based on top-down principle
- **_src/parsing.py_**
    command line interface for running parsers
- **_src/parserTest.py_**
    tests for parsers
- **_thesis/_**
    contains source files for thesis in latex and generated thesis in *.pdf*

## Usage of parsers

It's really easy to run parsers

```shell
python parsing.py <arguments>
```

### Command-line arguments

```shell
-C -> use parser for context free grammar
-E -> use parser for E0L system
-T -> use parser for ET0L system
Exactly 1 command above has to be used.
-w <word> -> specifies word to be parsed !MANDATORY!
-r <rules> -> specifies file with rules for parser !MANDATORY!
```

## Running tests

Running tests is also easy

```shell
python parserTest.py
```

Execution of tests might be slow!

#### Author
Author of these source codes and thesis is Tomáš Kožár. This thesis was done under supervision of prof.RNDr. Alexander Meduna,CSc.