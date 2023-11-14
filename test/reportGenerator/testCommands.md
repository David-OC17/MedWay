# Test commands for LaTeX report creation

## Quick test

Compile the `miniTest.tex` file present in this directory by using the command:
```bash
pdflatex -shell-escape miniTest.tex
```

## More extense test

To be able to create the `.pdf` files as needed, verify that `pdflatex` command is working by
compiling the `dailyReportTemplate_test.tex` file present in this directory. (Temporarly take the file to `/analysis/templates/` to avoid having to pass the contents of the placeholders if so is needed, and avoiding having to change the routes to the images.) Run the following command from the terminal:
```bash
# If in Linux
pdflatex -shell-escape dailyReportTemplate_test.tex

# If in Windows
pdflatex dailyReportTemplate_test.tex
```

_Note:_ to test full compilation (with placeholders included) from Python3, run the `reportGenerator.py` file.