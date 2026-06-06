# CSM 258: Numerical Methods and Computations - Group 2 Assignment

## Solving Transcendental Equations

This project solves the transcendental equation **f(x) = e^(-x) - x = 0** using four numerical root-finding methods, with a real-world application to **Newton's Law of Cooling**.

The true root is **x\* = 0.5671433** (the Omega constant).

---

## Project Structure

```
Algebra/
|-- src/
|   |-- TranscendentalEquationSolver.java   # Main Java program (all 4 methods)
|-- interactive_app.py                      # Interactive GUI with hover/zoom + PNG export
|-- plots/                                  # Generated plot images (PNG)
|-- Group2_Assignment1.pdf                  # Original assignment PDF
|-- README.md                              # This file
```

---

## Prerequisites

### Java (for the numerical solver)
- **Java JDK 17+** (tested with JDK 25)
- Verify: `java --version`

### Python (for plotting and interactive visualization)
- **Python 3.12 or 3.13** (3.15 does NOT work with matplotlib)
- Verify: `py -3.13 --version`

### Python Packages
Install the required packages for Python 3.13:

```bash
py -3.13 -m pip install matplotlib numpy
```

---

## How to Run

### Step 1: Compile and Run the Java Solver

```bash
javac src/TranscendentalEquationSolver.java -d out
java -cp out TranscendentalEquationSolver
```

This prints:
- Full theory and algorithm explanations for each method
- Detailed iteration tables with step-by-step calculations
- A comparison summary table of all four methods

### Step 2: Launch the Interactive Visualization App

```bash
py -3.13 interactive_app.py
```

This opens a GUI window with:
- **6 clickable figure cards** -- click any card to open its interactive plot
- **Hover** over any data point to see its exact (x, y) coordinates
- **Zoom** in/out using the toolbar magnifying glass
- **Pan** the plot by clicking and dragging
- **Save All Figures as PNG** button -- exports all 6 publication-quality PNGs to `plots/`

The 6 figures are:

| Figure | Description |
|--------|-------------|
| Figure 1 | Graph of f(x) with root identification |
| Figure 2 | Bisection Method -- successive midpoints |
| Figure 3 | False Position Method -- chord lines |
| Figure 4 | Newton-Raphson Method -- tangent line iterations |
| Figure 5 | Secant Method -- chord line iterations |
| Figure 6 | Convergence comparison of all four methods (log scale) |

---

## Methods Implemented

| Method | Iterations | True Error | Convergence | Notes |
|--------|-----------|------------|-------------|-------|
| Bisection | 20 | 3.06e-08 | Linear (order 1) | Guaranteed convergence |
| False Position | 8 | 9.52e-09 | Linear (order 1) | Faster; may stagnate |
| Newton-Raphson | 4 | 2.78e-15 | Quadratic (order 2) | Fastest; needs f'(x) |
| Secant | 4 | 1.62e-08 | Superlinear (~1.618) | No derivative needed |

All four methods converge to **x\* = 0.5671433**.

---

## Troubleshooting

### "No module named 'matplotlib'"
Make sure you are using Python 3.13 (not 3.15):
```bash
py -3.13 -m pip install matplotlib numpy
```

### IDE shows "No base Python found"
Click **"Select Python Interpreter"** in the VS Code status bar and choose **Python 3.13**.

### matplotlib "building font cache" on first run
This is normal on the first run. It takes about 15-30 seconds and only happens once.
