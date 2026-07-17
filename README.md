\# Python Blackjack



A standalone Blackjack desktop application built with Python and Tkinter, compiled into a portable executable.



\## 🎴 Assets \& Attribution

\* \*\*Card Faces:\*\* Public domain vector assets obtained from the \[Vector Playing Cards Archive](https://code.google.com/archive/p/vector-playing-cards/).

\* \*\*Card Backs:\*\* Custom procedural graphics generated directly using Python (generation script included).

\* \*\*Optimization:\*\* All raw asset graphics have been renamed, cropped, and resized for performance efficiency (asset pipeline utility scripts are included in this repository).



> \*\*Setup Note:\*\* Ensure all finalized card assets are placed inside a folder named `cards/` located in the root script directory before running or compiling.



\---



\## 🛠️ Compilation \& Deployment



This project uses \*\*PyInstaller\*\* to package the Python runtime, script logic, and user asset folders into a single, zero-dependency executable file.



\### 1. Prerequisite Installation

Install the compiler package via pip:

```bash

pip install pyinstaller

