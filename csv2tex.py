#!/usr/bin/env python3

"""
Copyright 2022 Davide Peressoni

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


import sys, fileinput, re
from typing import List


############################
########### Help ###########
############################

me = sys.argv[0]

__doc__ = f"""
csv2tex
Convert CSV files to LaTeX tables.

usage:

  {me} input.csv > output.tex

or

  cat input.csv | {me} | tee output.tex

Supports both comma-separated and semicolon-separated files.

Released under Apache 2.0 License.
"""

if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
  print(__doc__)
  exit()


###########################
######## Variables ########
###########################

n_cols: int = 0
rows: List[List[str]] = []


############################
######### Read CSV #########
############################

col_re = re.compile(r'\s*(?:"([^"]*)"|([^",;\s][^",;]*?))\s*(?:[,;]|\n?$)|[,;]')

for line in fileinput.input(sys.argv[1:]):
  row = (
    m.group(1) or m.group(2) or ''
    for m in col_re.finditer(str(line))
  )
  rows.append(row := [
    col.replace('&', r"\&").replace('%', r"\%")
    for col in row
  ])
  n_cols = max(n_cols, len(row))


############################
### Generate LaTeX table ###
############################

header: bool = True

print(r"""\begin{table}
	\begin{tabular}{""" + 'c' * n_cols + r"""}
		\hline""")

for row in rows:
  if len(row):
    print("\t\t" + ( "\t& ".join(row) ) + r"	\\")
    if header:
      print(r"		\hline")
      header = False

print(r"""		\hline
	\end{tabular}
	\caption{}
	\label{tab:}
\end{table}""")

