# ModelScout

**ModelScout** is a command-line tool designed to help users pick the best LLM for their needs. Modelscout uses the same recommendation algorithm as [Macros On Demand](https://github.com/Hadi-M-Ibrahim/Macros-On-Demand) a more in-depth example of my SWE work. While ModelScout is simple it serves as a useful stop-gap in the quickly evolving field of LLMs. As the name suggests ModelScout is simply a scout and should serve as the beginning, not the end of your LLM search. Subjective metrics such as performance and the degree to which a model is supported are gathered from various sources and forums (ie. Benchmarks, Reddit, Google trends. etc) and are based largely on community sentiment so should be taken with a grain of salt. Further not the cost per million tokens for open source models are very rough estimates as well.

---

## Features

- **Interactive filtering**: Easily select filters step by step.
- **Customizable**: Filter models by company, cost, performance, context length, and API/tool availability.
- **Lightweight & Easy to Use**: Requires only Python and a CSV file.

---

## Command-Line Arguments

| Argument                         | Description                                                 |
| -------------------------------- | ----------------------------------------------------------- |
| `file` (Default: `./models.csv`) | Path to the CSV file                                        |
| `--scout`                        | Launch interactive mode for selecting filters (Recommended) |
| `--top`                          | Number of recommended models to display (5 by default)      |
| `--license`                      | Ideal license (1 for open source, 0 for no preference)      |
| `--performance`                  | Ideal performance rating (1.0-10.0)                         |
| `--cost`                         | Ideal cost per million tokens                               |
| `--context_length`               | Ideal context length                                        |
| `--Support`                      | Ideal API/tools availability (1.0-10.0)                     |

---

## CSV format

```
Model Name,Company,Context Length,Cost per Million Tokens,Performance,license,Support
```

--

## Installation

Ensure you have Python installed, then install ModelScout using pip:

```sh
pip install git+https://github.com/yourusername/ModelScout.git
```

Alternatively, clone the repository manually:

```sh
git clone https://github.com/yourusername/ModelScout.git
cd ModelScout
```
