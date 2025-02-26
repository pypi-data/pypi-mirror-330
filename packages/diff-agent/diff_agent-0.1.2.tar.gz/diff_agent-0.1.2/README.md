# DiffAgent

A tool for automatically committing and summarizing git changes.

## Installation

Install via pip:
```
pip install diff_agent
```

## Usage

```python
from diff_agent import DiffAgent

# Initialize the DiffAgent with desired model and prompt
agent = DiffAgent(
    model="ollama/llama3.1",  # Default model
    prompt="Summarize the code changes clearly and concisely",
    strong_model="openai/gpt-4o-mini",  # Strong model for larger diffs
    strong_model_threshold=10,  # Threshold to switch to strong model
    max_diff_len=5000,  # Max chars to send to the model
    log_file="whatIdid.txt"  # Optional log file to track changes
)

# Run the process and get the summary of changes
change_summary = agent.run()

# Print the result
print(change_summary)
```

## Features

- Automatically switch to a branch for commits and back to your original branch
- Summarize code changes using LLMs
- Ignore specified files from Git tracking
- Log changes to a human-readable file
- Switch to a more powerful model for complex changes

## License

This project is licensed under the MIT License - see the LICENSE file for details.
