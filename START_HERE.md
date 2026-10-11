# Your first session

Allow about 30-60 minutes. Run the demo before editing code.

1. Follow the README's download and run instructions.
2. Open `reports/generated/light_curve.html` and inspect the output.
3. Open `run.py` in a text editor. Locate the input, processing, and output steps.
4. Make this small change: In `run.py`, change the injected dip depth from `0.015` to `0.008` and change the matching injected-depth metadata from `0.015` to `0.008`. Run the demo again. Compare the recovered depth and period. Then restore the values before running the supplied fixture tests, which expect the original injection.
5. Rerun the demo and explain what changed in your own words.
6. Run `python -m unittest discover -s tests -v` after restoring the original demo fixture if you changed it.
7. Add a dated entry to `docs/LEARNING_LOG.md`: your change, what you expected, what happened, and what remains uncertain.

## Saving your work to GitHub

For a small edit, use the pencil button on the corresponding GitHub file and commit it with a description of the change. For local editing, GitHub Desktop can manage commits and pushes without terminal Git commands. A commit saves a version locally; a push uploads it. Downloading another ZIP does not upload your edits.

When uploading through the website, inspect every selected file: `.gitignore` only filters normal Git operations and does not stop manual uploads. Do not upload downloaded datasets or secrets. Keep the root README and source files at the top level, rather than wrapping everything in another folder with the repository name.

## Before applications

Replace the demo with documented real data, make the next roadmap milestones reproducible, and add a report or demo that you can explain in an interview. This starter is not a finished portfolio project.
