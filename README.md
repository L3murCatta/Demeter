# Demeter

Query language for LaTeX data.

name {LaTeX file with extension} within {environment or command}([{number of instance}]) (> {environment or command}([{number of instance}])[...] print

Examples:

name displaymath.tex within sc print

name displaymath.tex within tabular[0] print

name displaymath.tex within tabular[0] > ArrayRow[1] > ArrayCell[2] print
