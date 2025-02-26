
# # # # import subprocess
# # # # import os
# # # # from litellm import completion
# # # # import weave


# # # # class DiffAgent:
# # # #     def __init__(self, api_base='http://localhost:11434', model="ollama/llama2", prompt="You are a helpful assistant.",
# # # #                  strong_model=None, strong_model_threshold=500, max_diff_len=5000):
# # # #         """
# # # #         Initialize DiffAgent.

# # # #         :param api_base: The base URL for the Litellm API
# # # #         :param model: The default model to use for summarization
# # # #         :param prompt: The system message for Litellm
# # # #         :param strong_model: Optional, stronger model for large diffs
# # # #         :param strong_model_threshold: Threshold (in characters) for when to use strong_model
# # # #         :param max_diff_len: Maximum number of characters to use for the diff. Limits absolute size of diff passed to the model.
# # # #         """
# # # #         self.api_base = api_base
# # # #         self.model = model
# # # #         self.prompt = prompt
# # # #         self.strong_model = strong_model
# # # #         self.strong_model_threshold = strong_model_threshold
# # # #         self.max_diff_len = max_diff_len

# # # #         # Initialize weave for tracking operations
# # # #         weave.init("diff-agent")

# # # #     def find_git_root(self):
# # # #         """Finds the closest .git directory and returns the root repo path."""
# # # #         try:
# # # #             repo_root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode("utf-8").strip()
# # # #             return repo_root
# # # #         except subprocess.CalledProcessError:
# # # #             raise RuntimeError("Not inside a Git repository.")

# # # #     def switch_to_agent_branch(self):
# # # #         """Creates or switches to the 'agent' branch, handling empty repos."""
# # # #         try:
# # # #             # Check if any commits exist
# # # #             head_exists = subprocess.run(["git", "rev-parse", "--verify", "HEAD"], check=True,
# # # #                                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
# # # #         except subprocess.CalledProcessError:
# # # #             head_exists = False  # No commits yet

# # # #         try:
# # # #             if head_exists:
# # # #                 # Get the current branch
# # # #                 current_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode("utf-8").strip()
# # # #             else:
# # # #                 current_branch = None

# # # #             if current_branch != "agent":
# # # #                 if not head_exists:
# # # #                     # Create an orphan branch if no commits exist
# # # #                     subprocess.run(["git", "checkout", "--orphan", "agent"], check=True)
# # # #                     subprocess.run(["git", "commit", "--allow-empty", "-m", "Initial commit on agent branch"], check=True)
# # # #                 else:
# # # #                     subprocess.run(["git", "checkout", "-B", "agent"], check=True)

# # # #         except subprocess.CalledProcessError:
# # # #             raise RuntimeError("Failed to switch to 'agent' branch.")

# # # #     def check_changes(self):
# # # #         """Checks if there are any changes in the repository and returns a boolean."""
# # # #         try:
# # # #             diff_summary = subprocess.check_output(["git", "diff"]).decode("utf-8").strip()
# # # #             return diff_summary != ""  # Return True if there are changes
# # # #         except subprocess.CalledProcessError:
# # # #             return False  # No changes or error getting diff

# # # #     def auto_commit(self):
# # # #         """Commits all changes and returns the new commit hash."""
# # # #         try:
# # # #             subprocess.run(["git", "add", "."], check=True)
# # # #             commit_message = "Auto-commit from script"
# # # #             subprocess.run(["git", "commit", "-m", commit_message], check=True)
# # # #             commit_hash = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode("utf-8").strip()
# # # #             return commit_hash
# # # #         except subprocess.CalledProcessError:
# # # #             return None  # No changes to commit

# # # #     def summarize_changes_with_litellm(self, diff_summary, new_files_contents=None, model=None):
# # # #         """Uses litellm to summarize the changes in the diff and newly created files."""
# # # #         try:
# # # #             # Prepare the prompt and content for the summarizer
# # # #             summary_content = diff_summary
# # # #             if new_files_contents:
# # # #                 # Append contents of new files to the summary
# # # #                 summary_content += "\n\nNewly created files:\n" + "\n\n".join(new_files_contents)
            
# # # #             # Use provided model or default to the instance's model
# # # #             model_to_use = model if model else self.model
# # # #             if 'ollama' not in model_to_use:
# # # #                 api_base = None 

# # # #             response = completion(
# # # #                 model=model_to_use,
# # # #                 messages=[
# # # #                     {"content": self.prompt, "role": "system"},
# # # #                     {"content": f"Summarize the following changes:\n{summary_content}", "role": "user"}
# # # #                 ],
# # # #                 api_base=api_base
# # # #             )
# # # #             return response['choices'][0]['message']['content']
# # # #         except Exception as e:
# # # #             print(f"Error summarizing changes: {e}")
# # # #             return "Could not summarize changes."

# # # #     def summarize_changes_locally(self, diff_summary):
# # # #         """Fallback: Summarize the diff using local logic if litellm is unavailable."""
# # # #         lines = diff_summary.splitlines()
# # # #         return f"Summary of changes: {len(lines)} lines modified."

# # # #     def summarize_changes_logic(self, diff_summary):
# # # #         """Summarize the diff directly based on the number of changes (basic method)."""
# # # #         if diff_summary:
# # # #             return f"Changes detected: {len(diff_summary.splitlines())} lines modified."
# # # #         return "No changes detected."

# # # #     def get_newly_created_files(self):
# # # #         """Returns a list of newly created files in the repository."""
# # # #         try:
# # # #             # Get newly created files by checking the diff for added files
# # # #             diff_summary = subprocess.check_output(["git", "diff", "--name-status"]).decode("utf-8").strip()
# # # #             added_files = [line.split()[1] for line in diff_summary.splitlines() if line.startswith("A")]
            
# # # #             file_contents = []
# # # #             for file in added_files:
# # # #                 if os.path.exists(file):
# # # #                     with open(file, 'r') as f:
# # # #                         file_contents.append(f.read())
            
# # # #             return file_contents

# # # #         except subprocess.CalledProcessError:
# # # #             return []

# # # #     def summarize_changes(self):
# # # #         """Summarizes the changes in the entire repository."""
# # # #         try:
# # # #             # Check for modifications in the entire repo (not just v1.py)
# # # #             diff_summary = subprocess.check_output(["git", "diff"]).decode("utf-8").strip()

# # # #             # Limit the diff size based on max_diff_len
# # # #             if len(diff_summary) > self.max_diff_len:
# # # #                 diff_summary = diff_summary[:self.max_diff_len]

# # # #             # Get newly created files and their contents
# # # #             new_files_contents = self.get_newly_created_files()

# # # #             # Decide which model to use based on the diff length
# # # #             model_to_use = self.model
# # # #             if len(diff_summary) > self.strong_model_threshold and self.strong_model:
# # # #                 model_to_use = self.strong_model

# # # #             if diff_summary or new_files_contents:
# # # #                 # Summarize both diff and new files
# # # #                 summary = self.summarize_changes_with_litellm(diff_summary, new_files_contents, model_to_use)
# # # #                 return f"Changes in the repository:\n{diff_summary}\n\nSummary: {summary}"
# # # #             else:
# # # #                 return "No changes detected in the repository."
# # # #         except subprocess.CalledProcessError:
# # # #             return "Error getting git diff for the repository."

# # # #     @weave.op
# # # #     def run(self):
# # # #         """Run the auto-commit and summarize process."""
# # # #         # Set repo root
# # # #         os.chdir(self.find_git_root())

# # # #         # Ensure we are on the agent branch
# # # #         self.switch_to_agent_branch()

# # # #         # Check for changes before committing
# # # #         if self.check_changes():
# # # #             # Summarize changes
# # # #             change_summary = self.summarize_changes()
            
# # # #             # Auto-commit changes
# # # #             commit_hash = self.auto_commit()

# # # #             return change_summary
# # # #         else:
# # # #             return "No changes detected. Skipping commit."


# # # import subprocess
# # # import os
# # # from litellm import completion
# # # import weave


# # # class DiffAgent:
# # #     def __init__(self, api_base='http://localhost:11434', model="ollama/llama2", prompt="You are a helpful assistant.",
# # #                  strong_model=None, strong_model_threshold=500, max_diff_len=5000,
# # #                  log_file="whatIdid.txt"):
# # #         """
# # #         Initialize DiffAgent.

# # #         :param api_base: The base URL for the Litellm API
# # #         :param model: The default model to use for summarization
# # #         :param prompt: The system message for Litellm
# # #         :param strong_model: Optional, stronger model for large diffs
# # #         :param strong_model_threshold: Threshold (in characters) for when to use strong_model
# # #         :param max_diff_len: Maximum number of characters to use for the diff. Limits absolute size of diff passed to the model.
# # #         :param log_file: File to log changes to
# # #         """
# # #         self.api_base = api_base
# # #         self.model = model
# # #         self.prompt = prompt
# # #         self.strong_model = strong_model
# # #         self.strong_model_threshold = strong_model_threshold
# # #         self.max_diff_len = max_diff_len
# # #         self.log_file = log_file

# # #         # Initialize weave for tracking operations
# # #         weave.init("diff-agent")

# # #     def find_git_root(self):
# # #         """Finds the closest .git directory and returns the root repo path."""
# # #         try:
# # #             repo_root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode("utf-8").strip()
# # #             return repo_root
# # #         except subprocess.CalledProcessError:
# # #             raise RuntimeError("Not inside a Git repository.")

# # #     def switch_to_agent_branch(self):
# # #         """Creates or switches to the 'agent' branch, handling empty repos."""
# # #         try:
# # #             # Check if any commits exist
# # #             head_exists = subprocess.run(["git", "rev-parse", "--verify", "HEAD"], check=True,
# # #                                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
# # #         except subprocess.CalledProcessError:
# # #             head_exists = False  # No commits yet

# # #         try:
# # #             if head_exists:
# # #                 # Get the current branch
# # #                 current_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode("utf-8").strip()
# # #             else:
# # #                 current_branch = None

# # #             if current_branch != "agent":
# # #                 if not head_exists:
# # #                     # Create an orphan branch if no commits exist
# # #                     subprocess.run(["git", "checkout", "--orphan", "agent"], check=True)
# # #                     subprocess.run(["git", "commit", "--allow-empty", "-m", "Initial commit on agent branch"], check=True)
# # #                 else:
# # #                     subprocess.run(["git", "checkout", "-B", "agent"], check=True)

# # #         except subprocess.CalledProcessError:
# # #             raise RuntimeError("Failed to switch to 'agent' branch.")

# # #     def check_changes(self):
# # #         """Checks if there are any changes in the repository and returns a boolean."""
# # #         try:
# # #             diff_summary = subprocess.check_output(["git", "diff"]).decode("utf-8").strip()
# # #             return diff_summary != ""  # Return True if there are changes
# # #         except subprocess.CalledProcessError:
# # #             return False  # No changes or error getting diff

# # #     def auto_commit(self):
# # #         """Commits all changes and returns the new commit hash."""
# # #         try:
# # #             subprocess.run(["git", "add", "."], check=True)
# # #             commit_message = "Auto-commit from script"
# # #             subprocess.run(["git", "commit", "-m", commit_message], check=True)
# # #             commit_hash = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode("utf-8").strip()
# # #             return commit_hash
# # #         except subprocess.CalledProcessError:
# # #             return None  # No changes to commit

# # #     def summarize_changes_with_litellm(self, diff_summary, new_files_contents=None, model=None):
# # #         """Uses litellm to summarize the changes in the diff and newly created files."""
# # #         try:
# # #             # Prepare the prompt and content for the summarizer
# # #             summary_content = diff_summary
# # #             if new_files_contents:
# # #                 # Append contents of new files to the summary
# # #                 summary_content += "\n\nNewly created files:\n" + "\n\n".join(new_files_contents)
            
# # #             # Use provided model or default to the instance's model
# # #             model_to_use = model if model else self.model
# # #             if 'ollama' not in model_to_use:
# # #                 api_base = None 

# # #             response = completion(
# # #                 model=model_to_use,
# # #                 messages=[
# # #                     {"content": self.prompt, "role": "system"},
# # #                     {"content": f"Summarize the following changes:\n{summary_content}", "role": "user"}
# # #                 ],
# # #                 api_base=api_base
# # #             )
# # #             return response['choices'][0]['message']['content']
# # #         except Exception as e:
# # #             print(f"Error summarizing changes: {e}")
# # #             return "Could not summarize changes."

# # #     def summarize_changes_locally(self, diff_summary):
# # #         """Fallback: Summarize the diff using local logic if litellm is unavailable."""
# # #         lines = diff_summary.splitlines()
# # #         return f"Summary of changes: {len(lines)} lines modified."

# # #     def summarize_changes_logic(self, diff_summary):
# # #         """Summarize the diff directly based on the number of changes (basic method)."""
# # #         if diff_summary:
# # #             return f"Changes detected: {len(diff_summary.splitlines())} lines modified."
# # #         return "No changes detected."

# # #     def get_newly_created_files(self):
# # #         """Returns a list of newly created files in the repository."""
# # #         try:
# # #             # Get newly created files by checking the diff for added files
# # #             diff_summary = subprocess.check_output(["git", "diff", "--name-status"]).decode("utf-8").strip()
# # #             added_files = [line.split()[1] for line in diff_summary.splitlines() if line.startswith("A")]
            
# # #             file_contents = []
# # #             for file in added_files:
# # #                 if os.path.exists(file):
# # #                     with open(file, 'r') as f:
# # #                         file_contents.append(f.read())
            
# # #             return file_contents

# # #         except subprocess.CalledProcessError:
# # #             return []

# # #     def summarize_changes(self):
# # #         """Summarizes the changes in the entire repository."""
# # #         try:
# # #             # Check for modifications in the entire repo (not just v1.py)
# # #             diff_summary = subprocess.check_output(["git", "diff"]).decode("utf-8").strip()

# # #             # Limit the diff size based on max_diff_len
# # #             if len(diff_summary) > self.max_diff_len:
# # #                 diff_summary = diff_summary[:self.max_diff_len]

# # #             # Get newly created files and their contents
# # #             new_files_contents = self.get_newly_created_files()

# # #             # Decide which model to use based on the diff length
# # #             model_to_use = self.model
# # #             if len(diff_summary) > self.strong_model_threshold and self.strong_model:
# # #                 model_to_use = self.strong_model

# # #             if diff_summary or new_files_contents:
# # #                 # Summarize both diff and new files
# # #                 summary = self.summarize_changes_with_litellm(diff_summary, new_files_contents, model_to_use)
# # #                 return summary
# # #             else:
# # #                 return "No changes detected in the repository."
# # #         except subprocess.CalledProcessError:
# # #             return "Error getting git diff for the repository."

# # #     def log_to_file(self, summary, commit_hash):
# # #         """Log the change summary and commit hash to the log file."""
# # #         try:
# # #             # Create the separator line
# # #             separator = "\n" + "#" * 50 + "\n"
            
# # #             # Format the log entry
# # #             log_entry = f"Commit: {commit_hash}\n\n{summary}{separator}"
            
# # #             # Write to the log file, creating it if it doesn't exist
# # #             with open(self.log_file, 'a') as f:
# # #                 f.write(log_entry)
                
# # #             return True
# # #         except Exception as e:
# # #             print(f"Error logging to file: {e}")
# # #             return False

# # #     @weave.op
# # #     def run(self):
# # #         """Run the auto-commit and summarize process."""
# # #         # Set repo root
# # #         os.chdir(self.find_git_root())

# # #         # Ensure we are on the agent branch
# # #         self.switch_to_agent_branch()

# # #         # Check for changes before committing
# # #         if self.check_changes():
# # #             # Summarize changes
# # #             change_summary = self.summarize_changes()
            
# # #             # Auto-commit changes
# # #             commit_hash = self.auto_commit()
            
# # #             # Log changes to the whatIdid.txt file
# # #             if commit_hash and change_summary:
# # #                 self.log_to_file(change_summary, commit_hash)
            
# # #             return f"Changes committed (hash: {commit_hash})\n\n{change_summary}"
# # #         else:
# # #             return "No changes detected. Skipping commit."

# # import subprocess
# # import os
# # from litellm import completion
# # import weave


# # class DiffAgent:
# #     def __init__(self, api_base='http://localhost:11434', model="ollama/llama2", prompt="You are a helpful assistant.",
# #                  strong_model=None, strong_model_threshold=500, max_diff_len=5000,
# #                  log_file="whatIdid.txt"):
# #         """
# #         Initialize DiffAgent.

# #         :param api_base: The base URL for the Litellm API
# #         :param model: The default model to use for summarization
# #         :param prompt: The system message for Litellm
# #         :param strong_model: Optional, stronger model for large diffs
# #         :param strong_model_threshold: Threshold (in characters) for when to use strong_model
# #         :param max_diff_len: Maximum number of characters to use for the diff. Limits absolute size of diff passed to the model.
# #         :param log_file: File to log changes to
# #         """
# #         self.api_base = api_base
# #         self.model = model
# #         self.prompt = prompt
# #         self.strong_model = strong_model
# #         self.strong_model_threshold = strong_model_threshold
# #         self.max_diff_len = max_diff_len
# #         self.log_file = log_file

# #         # Initialize weave for tracking operations
# #         weave.init("diff-agent")

# #     def find_git_root(self):
# #         """Finds the closest .git directory and returns the root repo path."""
# #         try:
# #             repo_root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode("utf-8").strip()
# #             return repo_root
# #         except subprocess.CalledProcessError:
# #             raise RuntimeError("Not inside a Git repository.")

# #     def switch_to_agent_branch(self):
# #         """Creates or switches to the 'agent' branch, handling empty repos."""
# #         try:
# #             # Check if any commits exist
# #             head_exists = subprocess.run(["git", "rev-parse", "--verify", "HEAD"], check=True,
# #                                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
# #         except subprocess.CalledProcessError:
# #             head_exists = False  # No commits yet

# #         try:
# #             if head_exists:
# #                 # Get the current branch
# #                 current_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode("utf-8").strip()
# #             else:
# #                 current_branch = None

# #             if current_branch != "agent":
# #                 if not head_exists:
# #                     # Create an orphan branch if no commits exist
# #                     subprocess.run(["git", "checkout", "--orphan", "agent"], check=True)
# #                     subprocess.run(["git", "commit", "--allow-empty", "-m", "Initial commit on agent branch"], check=True)
# #                 else:
# #                     subprocess.run(["git", "checkout", "-B", "agent"], check=True)

# #         except subprocess.CalledProcessError:
# #             raise RuntimeError("Failed to switch to 'agent' branch.")

# #     def check_changes(self):
# #         """Checks if there are any changes in the repository and returns a boolean."""
# #         try:
# #             diff_summary = subprocess.check_output(["git", "diff"]).decode("utf-8").strip()
# #             return diff_summary != ""  # Return True if there are changes
# #         except subprocess.CalledProcessError:
# #             return False  # No changes or error getting diff

# #     def auto_commit(self):
# #         """Commits all changes and returns the new commit hash."""
# #         try:
# #             subprocess.run(["git", "add", "."], check=True)
# #             commit_message = "Auto-commit from script"
# #             subprocess.run(["git", "commit", "-m", commit_message], check=True)
# #             commit_hash = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode("utf-8").strip()
# #             return commit_hash
# #         except subprocess.CalledProcessError:
# #             return None  # No changes to commit

# #     def summarize_changes_with_litellm(self, diff_summary, new_files_contents=None, model=None):
# #         """Uses litellm to summarize the changes in the diff and newly created files."""
# #         try:
# #             # Prepare the prompt and content for the summarizer
# #             summary_content = diff_summary
# #             if new_files_contents:
# #                 # Append contents of new files to the summary
# #                 summary_content += "\n\nNewly created files:\n" + "\n\n".join(new_files_contents)
            
# #             # Use provided model or default to the instance's model
# #             model_to_use = model if model else self.model
# #             if 'ollama' not in model_to_use:
# #                 api_base = None 

# #             response = completion(
# #                 model=model_to_use,
# #                 messages=[
# #                     {"content": self.prompt, "role": "system"},
# #                     {"content": f"Summarize the following changes:\n{summary_content}", "role": "user"}
# #                 ],
# #                 api_base=api_base
# #             )
# #             return response['choices'][0]['message']['content']
# #         except Exception as e:
# #             print(f"Error summarizing changes: {e}")
# #             return "Could not summarize changes."

# #     def summarize_changes_locally(self, diff_summary):
# #         """Fallback: Summarize the diff using local logic if litellm is unavailable."""
# #         lines = diff_summary.splitlines()
# #         return f"Summary of changes: {len(lines)} lines modified."

# #     def summarize_changes_logic(self, diff_summary):
# #         """Summarize the diff directly based on the number of changes (basic method)."""
# #         if diff_summary:
# #             return f"Changes detected: {len(diff_summary.splitlines())} lines modified."
# #         return "No changes detected."

# #     def get_newly_created_files(self):
# #         """Returns a list of newly created files in the repository."""
# #         try:
# #             # Get newly created files using git status instead of git diff
# #             # This will detect untracked (newly created) files
# #             status_output = subprocess.check_output(["git", "status", "--porcelain"]).decode("utf-8").strip()
            
# #             # Lines starting with '??' are untracked files, lines starting with 'A' are added files
# #             added_files = []
# #             for line in status_output.splitlines():
# #                 if line.startswith("?? ") or line.startswith("A "):
# #                     # Extract filename (remove the status prefix and any quotes)
# #                     filename = line[3:].strip().strip('"')
# #                     added_files.append(filename)
            
# #             file_contents = []
# #             for file in added_files:
# #                 if os.path.exists(file) and os.path.isfile(file):
# #                     try:
# #                         with open(file, 'r', errors='replace') as f:
# #                             file_contents.append(f"File: {file}\n{f.read()}")
# #                     except Exception as e:
# #                         file_contents.append(f"File: {file}\n[Error reading file: {str(e)}]")
            
# #             return file_contents

# #         except subprocess.CalledProcessError:
# #             return []

# #     def summarize_changes(self):
# #         """Summarizes the changes in the entire repository."""
# #         try:
# #             # Check for modifications in the entire repo
# #             diff_summary = subprocess.check_output(["git", "diff"]).decode("utf-8").strip()
            
# #             # Also get information about status changes (including new files)
# #             status_summary = subprocess.check_output(["git", "status", "--short"]).decode("utf-8").strip()

# #             # Combine both for a complete picture of changes
# #             full_diff_summary = f"Git diff:\n{diff_summary}\n\nGit status:\n{status_summary}"

# #             # Limit the diff size based on max_diff_len
# #             if len(full_diff_summary) > self.max_diff_len:
# #                 full_diff_summary = full_diff_summary[:self.max_diff_len]
                
# #             # Use the combined summary for further processing
# #             diff_summary = full_diff_summary

# #             # Get newly created files and their contents
# #             new_files_contents = self.get_newly_created_files()

# #             # Decide which model to use based on the diff length
# #             model_to_use = self.model
# #             if len(diff_summary) > self.strong_model_threshold and self.strong_model:
# #                 model_to_use = self.strong_model

# #             if diff_summary or new_files_contents:
# #                 # Summarize both diff and new files
# #                 summary = self.summarize_changes_with_litellm(diff_summary, new_files_contents, model_to_use)
# #                 return summary
# #             else:
# #                 return "No changes detected in the repository."
# #         except subprocess.CalledProcessError:
# #             return "Error getting git diff for the repository."

# #     def log_to_file(self, summary, commit_hash):
# #         """Log the change summary and commit hash to the log file."""
# #         try:
# #             # Create the separator line
# #             separator = "\n" + "#" * 50 + "\n"
            
# #             # Format the log entry
# #             log_entry = f"Commit: {commit_hash}\n\n{summary}{separator}"
            
# #             # Write to the log file, creating it if it doesn't exist
# #             with open(self.log_file, 'a') as f:
# #                 f.write(log_entry)
                
# #             return True
# #         except Exception as e:
# #             print(f"Error logging to file: {e}")
# #             return False

# #     @weave.op
# #     def run(self):
# #         """Run the auto-commit and summarize process."""
# #         # Set repo root
# #         os.chdir(self.find_git_root())

# #         # Ensure we are on the agent branch
# #         self.switch_to_agent_branch()

# #         # Check for changes before committing
# #         if self.check_changes():
# #             # Summarize changes
# #             change_summary = self.summarize_changes()
            
# #             # Auto-commit changes
# #             commit_hash = self.auto_commit()
            
# #             # Log changes to the whatIdid.txt file
# #             if commit_hash and change_summary:
# #                 self.log_to_file(change_summary, commit_hash)
            
# #             return f"Changes committed (hash: {commit_hash})\n\n{change_summary}"
# #         else:
# #             return "No changes detected. Skipping commit."

# import subprocess
# import os
# from litellm import completion
# import weave


# class DiffAgent:
#     def __init__(self, api_base='http://localhost:11434', model="ollama/llama2", prompt="You are a helpful assistant.",
#                  strong_model=None, strong_model_threshold=500, max_diff_len=5000,
#                  log_file="whatIdid.txt"):
#         """
#         Initialize DiffAgent.

#         :param api_base: The base URL for the Litellm API
#         :param model: The default model to use for summarization
#         :param prompt: The system message for Litellm
#         :param strong_model: Optional, stronger model for large diffs
#         :param strong_model_threshold: Threshold (in characters) for when to use strong_model
#         :param max_diff_len: Maximum number of characters to use for the diff. Limits absolute size of diff passed to the model.
#         :param log_file: File to log changes to
#         """
#         self.api_base = api_base
#         self.model = model
#         self.prompt = prompt
#         self.strong_model = strong_model
#         self.strong_model_threshold = strong_model_threshold
#         self.max_diff_len = max_diff_len
#         self.log_file = log_file

#         # Initialize weave for tracking operations
#         weave.init("diff-agent")

#     def find_git_root(self):
#         """Finds the closest .git directory and returns the root repo path."""
#         try:
#             repo_root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode("utf-8").strip()
#             return repo_root
#         except subprocess.CalledProcessError:
#             raise RuntimeError("Not inside a Git repository.")

#     def switch_to_agent_branch(self):
#         """Creates or switches to the 'agent' branch, handling empty repos."""
#         try:
#             # Check if any commits exist
#             head_exists = subprocess.run(["git", "rev-parse", "--verify", "HEAD"], check=True,
#                                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
#         except subprocess.CalledProcessError:
#             head_exists = False  # No commits yet

#         try:
#             if head_exists:
#                 # Get the current branch
#                 current_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode("utf-8").strip()
#             else:
#                 current_branch = None

#             if current_branch != "agent":
#                 if not head_exists:
#                     # Create an orphan branch if no commits exist
#                     subprocess.run(["git", "checkout", "--orphan", "agent"], check=True)
#                     subprocess.run(["git", "commit", "--allow-empty", "-m", "Initial commit on agent branch"], check=True)
#                 else:
#                     subprocess.run(["git", "checkout", "-B", "agent"], check=True)

#         except subprocess.CalledProcessError:
#             raise RuntimeError("Failed to switch to 'agent' branch.")

#     def check_changes(self):
#         """Checks if there are any changes in the repository and returns a boolean."""
#         try:
#             # Get diff but exclude the log file
#             diff_summary = subprocess.check_output(["git", "diff", "--", ".", f":!{self.log_file}"]).decode("utf-8").strip()
            
#             # Also check untracked files, excluding the log file
#             status_output = subprocess.check_output(["git", "status", "--porcelain"]).decode("utf-8").strip()
#             has_other_changes = any(line.split()[-1] != self.log_file for line in status_output.splitlines() if line)
            
#             return diff_summary != "" or has_other_changes  # Return True if there are changes
#         except subprocess.CalledProcessError:
#             return False  # No changes or error getting diff

#     def auto_commit(self):
#         """Commits all changes and returns the new commit hash."""
#         try:
#             # Add whatIdid.txt to gitignore if it's not already there
#             gitignore_path = os.path.join(self.find_git_root(), ".gitignore")
#             add_to_gitignore = True
            
#             if os.path.exists(gitignore_path):
#                 with open(gitignore_path, 'r') as f:
#                     if self.log_file in f.read():
#                         add_to_gitignore = False
            
#             if add_to_gitignore:
#                 with open(gitignore_path, 'a+') as f:
#                     f.write(f"\n{self.log_file}\n")
                
#             # Add everything except the log file
#             subprocess.run(["git", "add", "--all", "--", ".", f":!{self.log_file}"], check=True)
            
#             commit_message = "Auto-commit from script"
#             subprocess.run(["git", "commit", "-m", commit_message], check=True)
#             commit_hash = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode("utf-8").strip()
#             return commit_hash
#         except subprocess.CalledProcessError:
#             return None  # No changes to commit

#     def summarize_changes_with_litellm(self, diff_summary, new_files_contents=None, model=None):
#         """Uses litellm to summarize the changes in the diff and newly created files."""
#         try:
#             # Prepare the prompt and content for the summarizer
#             summary_content = diff_summary
#             if new_files_contents:
#                 # Append contents of new files to the summary
#                 summary_content += "\n\nNewly created files:\n" + "\n\n".join(new_files_contents)
            
#             # Use provided model or default to the instance's model
#             model_to_use = model if model else self.model
#             if 'ollama' not in model_to_use:
#                 api_base = None 

#             response = completion(
#                 model=model_to_use,
#                 messages=[
#                     {"content": self.prompt, "role": "system"},
#                     {"content": f"Summarize the following changes:\n{summary_content}", "role": "user"}
#                 ],
#                 api_base=api_base
#             )
#             return response['choices'][0]['message']['content']
#         except Exception as e:
#             print(f"Error summarizing changes: {e}")
#             return "Could not summarize changes."

#     def summarize_changes_locally(self, diff_summary):
#         """Fallback: Summarize the diff using local logic if litellm is unavailable."""
#         lines = diff_summary.splitlines()
#         return f"Summary of changes: {len(lines)} lines modified."

#     def summarize_changes_logic(self, diff_summary):
#         """Summarize the diff directly based on the number of changes (basic method)."""
#         if diff_summary:
#             return f"Changes detected: {len(diff_summary.splitlines())} lines modified."
#         return "No changes detected."

#     def get_newly_created_files(self):
#         """Returns a list of newly created files in the repository."""
#         try:
#             # Get newly created files using git status instead of git diff
#             # This will detect untracked (newly created) files
#             status_output = subprocess.check_output(["git", "status", "--porcelain"]).decode("utf-8").strip()
            
#             # Lines starting with '??' are untracked files, lines starting with 'A' are added files
#             added_files = []
#             for line in status_output.splitlines():
#                 if line.startswith("?? ") or line.startswith("A "):
#                     # Extract filename (remove the status prefix and any quotes)
#                     filename = line[3:].strip().strip('"')
#                     added_files.append(filename)
            
#             file_contents = []
#             for file in added_files:
#                 if os.path.exists(file) and os.path.isfile(file):
#                     try:
#                         with open(file, 'r', errors='replace') as f:
#                             file_contents.append(f"File: {file}\n{f.read()}")
#                     except Exception as e:
#                         file_contents.append(f"File: {file}\n[Error reading file: {str(e)}]")
            
#             return file_contents

#         except subprocess.CalledProcessError:
#             return []

#     def summarize_changes(self):
#         """Summarizes the changes in the entire repository."""
#         try:
#             # Check for modifications in the entire repo, excluding whatIdid.txt
#             diff_summary = subprocess.check_output(["git", "diff", "--", ".", f":!{self.log_file}"]).decode("utf-8").strip()
            
#             # Also get information about status changes (including new files), filtering out the log file
#             status_output = subprocess.check_output(["git", "status", "--porcelain"]).decode("utf-8").strip()
#             status_lines = [line for line in status_output.splitlines() if self.log_file not in line]
#             status_summary = "\n".join(status_lines)

#             # Combine both for a complete picture of changes
#             full_diff_summary = f"Git diff:\n{diff_summary}\n\nGit status:\n{status_summary}"

#             # Limit the diff size based on max_diff_len
#             if len(full_diff_summary) > self.max_diff_len:
#                 full_diff_summary = full_diff_summary[:self.max_diff_len]
                
#             # Use the combined summary for further processing
#             diff_summary = full_diff_summary

#             # Get newly created files and their contents
#             new_files_contents = self.get_newly_created_files()

#             # Decide which model to use based on the diff length
#             model_to_use = self.model
#             if len(diff_summary) > self.strong_model_threshold and self.strong_model:
#                 model_to_use = self.strong_model

#             if diff_summary or new_files_contents:
#                 # Summarize both diff and new files
#                 summary = self.summarize_changes_with_litellm(diff_summary, new_files_contents, model_to_use)
#                 return summary
#             else:
#                 return "No changes detected in the repository."
#         except subprocess.CalledProcessError:
#             return "Error getting git diff for the repository."

#     def log_to_file(self, summary, commit_hash):
#         """Log the change summary and commit hash to the log file."""
#         try:
#             # Create the separator line
#             separator = "\n" + "#" * 50 + "\n"
            
#             # Format the log entry
#             log_entry = f"Commit: {commit_hash}\n\n{summary}{separator}"
            
#             # Write to the log file, creating it if it doesn't exist
#             with open(self.log_file, 'a') as f:
#                 f.write(log_entry)
                
#             return True
#         except Exception as e:
#             print(f"Error logging to file: {e}")
#             return False

#     @weave.op
#     def run(self):
#         """Run the auto-commit and summarize process."""
#         # Set repo root
#         os.chdir(self.find_git_root())

#         # Ensure we are on the agent branch
#         self.switch_to_agent_branch()

#         # Check for changes before committing
#         if self.check_changes():
#             # Summarize changes
#             change_summary = self.summarize_changes()
            
#             # Auto-commit changes
#             commit_hash = self.auto_commit()
            
#             # Log changes to the whatIdid.txt file
#             if commit_hash and change_summary:
#                 self.log_to_file(change_summary, commit_hash)
            
#             return f"Changes committed (hash: {commit_hash})\n\n{change_summary}"
#         else:
#             return "No changes detected. Skipping commit."




import os
from litellm import completion
import weave
import subprocess


class DiffAgent:
    def __init__(self, api_base='http://localhost:11434', model="ollama/llama2", prompt="You are a helpful assistant.",
                 strong_model=None, strong_model_threshold=500, max_diff_len=5000,
                 log_file="whatIdid.txt"):
        """
        Initialize DiffAgent.

        :param api_base: The base URL for the Litellm API
        :param model: The default model to use for summarization
        :param prompt: The system message for Litellm
        :param strong_model: Optional, stronger model for large diffs
        :param strong_model_threshold: Threshold (in characters) for when to use strong_model
        :param max_diff_len: Maximum number of characters to use for the diff. Limits absolute size of diff passed to the model.
        :param log_file: File to log changes to
        """
        self.api_base = api_base
        self.model = model
        self.prompt = prompt
        self.strong_model = strong_model
        self.strong_model_threshold = strong_model_threshold
        self.max_diff_len = max_diff_len
        self.log_file = log_file

        # Initialize weave for tracking operations
        weave.init("diff-agent")

    def find_git_root(self):
        """Finds the closest .git directory and returns the root repo path."""
        try:
            repo_root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode("utf-8").strip()
            return repo_root
        except subprocess.CalledProcessError:
            raise RuntimeError("Not inside a Git repository.")


    def switch_to_branch(self, branch_name):
            """Switches to the specified branch if it exists."""
            if branch_name and branch_name != "agent":
                try:
                    # Check if the branch exists
                    branch_exists = subprocess.run(
                        ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{branch_name}"],
                        check=False
                    ).returncode == 0
                    
                    if branch_exists:
                        subprocess.run(["git", "checkout", branch_name], check=True)
                        return True
                    return False
                except subprocess.CalledProcessError:
                    print(f"Failed to switch to branch '{branch_name}'")
                    return False
            return False

    def switch_to_agent_branch(self):
        """Creates or switches to the 'agent' branch, handling empty repos. Returns the original branch name."""
        try:
            # Check if any commits exist
            head_exists = subprocess.run(["git", "rev-parse", "--verify", "HEAD"], check=True,
                                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
        except subprocess.CalledProcessError:
            head_exists = False  # No commits yet

        try:
            original_branch = None
            if head_exists:
                # Get the current branch
                original_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode("utf-8").strip()
            
            if original_branch != "agent":
                if not head_exists:
                    # Create an orphan branch if no commits exist
                    subprocess.run(["git", "checkout", "--orphan", "agent"], check=True)
                    subprocess.run(["git", "commit", "--allow-empty", "-m", "Initial commit on agent branch"], check=True)
                else:
                    subprocess.run(["git", "checkout", "-B", "agent"], check=True)
            
            return original_branch
            
        except subprocess.CalledProcessError:
            raise RuntimeError("Failed to switch to 'agent' branch.")

    def check_changes(self):
        """Checks if there are any changes in the repository and returns a boolean."""
        try:
            # Get diff but exclude the log file
            diff_summary = subprocess.check_output(["git", "diff", "--", ".", f":!{self.log_file}"]).decode("utf-8").strip()
            
            # Also check untracked files, excluding the log file
            status_output = subprocess.check_output(["git", "status", "--porcelain"]).decode("utf-8").strip()
            has_other_changes = any(line.split()[-1] != self.log_file for line in status_output.splitlines() if line)
            
            return diff_summary != "" or has_other_changes  # Return True if there are changes
        except subprocess.CalledProcessError:
            return False  # No changes or error getting diff

    def auto_commit(self):
        """Commits all changes and returns the new commit hash."""
        try:
            # Add whatIdid.txt to gitignore if it's not already there
            gitignore_path = os.path.join(self.find_git_root(), ".gitignore")
            add_to_gitignore = True
            
            if os.path.exists(gitignore_path):
                with open(gitignore_path, 'r') as f:
                    if self.log_file in f.read():
                        add_to_gitignore = False
            
            if add_to_gitignore:
                with open(gitignore_path, 'a+') as f:
                    f.write(f"\n{self.log_file}\n")
                
            # Add everything except the log file
            subprocess.run(["git", "add", "--all", "--", ".", f":!{self.log_file}"], check=True)
            
            commit_message = "Auto-commit from script"
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            commit_hash = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode("utf-8").strip()
            return commit_hash
        except subprocess.CalledProcessError:
            return None  # No changes to commit

    def summarize_changes_with_litellm(self, diff_summary, new_files_contents=None, model=None):
        """Uses litellm to summarize the changes in the diff and newly created files."""
        try:
            # Prepare the prompt and content for the summarizer
            summary_content = diff_summary
            if new_files_contents:
                # Append contents of new files to the summary
                summary_content += "\n\nNewly created files:\n" + "\n\n".join(new_files_contents)
            
            # Use provided model or default to the instance's model
            model_to_use = model if model else self.model
            if 'ollama' not in model_to_use:
                api_base = None 

            response = completion(
                model=model_to_use,
                messages=[
                    {"content": self.prompt, "role": "system"},
                    {"content": f"Summarize the following changes:\n{summary_content}", "role": "user"}
                ],
                api_base=api_base
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error summarizing changes: {e}")
            return "Could not summarize changes."

    def summarize_changes_locally(self, diff_summary):
        """Fallback: Summarize the diff using local logic if litellm is unavailable."""
        lines = diff_summary.splitlines()
        return f"Summary of changes: {len(lines)} lines modified."

    def summarize_changes_logic(self, diff_summary):
        """Summarize the diff directly based on the number of changes (basic method)."""
        if diff_summary:
            return f"Changes detected: {len(diff_summary.splitlines())} lines modified."
        return "No changes detected."

    def get_newly_created_files(self):
        """Returns a list of newly created files in the repository."""
        try:
            # Get newly created files using git status instead of git diff
            # This will detect untracked (newly created) files
            status_output = subprocess.check_output(["git", "status", "--porcelain"]).decode("utf-8").strip()
            
            # Lines starting with '??' are untracked files, lines starting with 'A' are added files
            added_files = []
            for line in status_output.splitlines():
                if line.startswith("?? ") or line.startswith("A "):
                    # Extract filename (remove the status prefix and any quotes)
                    filename = line[3:].strip().strip('"')
                    added_files.append(filename)
            
            file_contents = []
            for file in added_files:
                if os.path.exists(file) and os.path.isfile(file):
                    try:
                        with open(file, 'r', errors='replace') as f:
                            file_contents.append(f"File: {file}\n{f.read()}")
                    except Exception as e:
                        file_contents.append(f"File: {file}\n[Error reading file: {str(e)}]")
            
            return file_contents

        except subprocess.CalledProcessError:
            return []

    def summarize_changes(self):
        """Summarizes the changes in the entire repository."""
        try:
            # Check for modifications in the entire repo, excluding whatIdid.txt
            diff_summary = subprocess.check_output(["git", "diff", "--", ".", f":!{self.log_file}"]).decode("utf-8").strip()
            
            # Also get information about status changes (including new files), filtering out the log file
            status_output = subprocess.check_output(["git", "status", "--porcelain"]).decode("utf-8").strip()
            status_lines = [line for line in status_output.splitlines() if self.log_file not in line]
            status_summary = "\n".join(status_lines)

            # Combine both for a complete picture of changes
            full_diff_summary = f"Git diff:\n{diff_summary}\n\nGit status:\n{status_summary}"

            # Limit the diff size based on max_diff_len
            if len(full_diff_summary) > self.max_diff_len:
                full_diff_summary = full_diff_summary[:self.max_diff_len]
                
            # Use the combined summary for further processing
            diff_summary = full_diff_summary

            # Get newly created files and their contents
            new_files_contents = self.get_newly_created_files()

            # Decide which model to use based on the diff length
            model_to_use = self.model
            if len(diff_summary) > self.strong_model_threshold and self.strong_model:
                model_to_use = self.strong_model

            if diff_summary or new_files_contents:
                # Summarize both diff and new files
                summary = self.summarize_changes_with_litellm(diff_summary, new_files_contents, model_to_use)
                return summary
            else:
                return "No changes detected in the repository."
        except subprocess.CalledProcessError:
            return "Error getting git diff for the repository."

    def log_to_file(self, summary, commit_hash):
        """Log the change summary and commit hash to the log file."""
        try:
            # Create the separator line
            separator = "\n" + "#" * 50 + "\n"
            
            # Format the log entry
            log_entry = f"Commit: {commit_hash}\n\n{summary}{separator}"
            
            # Write to the log file, creating it if it doesn't exist
            with open(self.log_file, 'a') as f:
                f.write(log_entry)
                
            return True
        except Exception as e:
            print(f"Error logging to file: {e}")
            return False

    @weave.op
    def run(self):
        """Run the auto-commit and summarize process."""
        # Set repo root
        os.chdir(self.find_git_root())

        # Ensure we are on the agent branch and save original branch
        original_branch = self.switch_to_agent_branch()

        try:
            # Check for changes before committing
            if self.check_changes():
                # Summarize changes
                change_summary = self.summarize_changes()
                
                # Auto-commit changes
                commit_hash = self.auto_commit()
                
                # Log changes to the whatIdid.txt file
                if commit_hash and change_summary:
                    self.log_to_file(change_summary, commit_hash)
                
                result = f"Changes committed (hash: {commit_hash})\n\n{change_summary}"
            else:
                result = "No changes detected. Skipping commit."
            
            # Switch back to the original branch if it exists and isn't already on it
            if original_branch and original_branch != "agent":
                self.switch_to_branch(original_branch)
                result += f"\nSwitched back to branch '{original_branch}'"
            
            return result
            
        except Exception as e:
            # Try to switch back to original branch even if there was an error
            if original_branch and original_branch != "agent":
                try:
                    self.switch_to_branch(original_branch)
                except:
                    pass
            raise e