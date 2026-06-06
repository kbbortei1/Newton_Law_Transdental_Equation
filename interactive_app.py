"""
CSM 258: Numerical Methods and Computations - Group 2 Assignment
================================================================
Interactive Visualization Application

A Python GUI app with:
  - A beautiful main menu with 6 figure buttons
  - Each button opens a FULLY INTERACTIVE matplotlib plot
  - Hover over any point to see its exact (x, y) coordinates
  - Zoom, pan, and explore the data freely

Prerequisites:
  py -3.13 -m pip install matplotlib numpy

Run:
  py -3.13 interactive_app.py
"""

import tkinter as tk
import numpy as np
import math
import os

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

# ============================================================================
# Constants
# ============================================================================
TRUE_ROOT = 0.5671432904097838  # Omega constant
TOLERANCE = 1e-7

# ============================================================================
# Function definitions
# ============================================================================
def f_np(x):
    """Numpy vectorized version for plotting curves."""
    return np.exp(-x) - x

def f(x):
    """Scalar version for single-value computations."""
    return math.exp(-x) - x

def f_prime(x):
    """f'(x) = -e^(-x) - 1  (scalar)."""
    return -math.exp(-x) - 1

# ============================================================================
# Color palette
# ============================================================================
COLORS = {
    'bg_dark': '#0f172a',
    'bg_card': '#1e293b',
    'bg_hover': '#334155',
    'accent_blue': '#3b82f6',
    'accent_cyan': '#06b6d4',
    'accent_green': '#22c55e',
    'accent_orange': '#f97316',
    'accent_red': '#ef4444',
    'accent_purple': '#a855f7',
    'text_primary': '#f1f5f9',
    'text_secondary': '#94a3b8',
    'text_muted': '#64748b',
}

FIGURE_BUTTONS = [
    ("Figure 1", "Graph of f(x) = e^(-x) - x", "Root Identification", COLORS['accent_blue']),
    ("Figure 2", "Bisection Method", "Successive Midpoints", COLORS['accent_green']),
    ("Figure 3", "False Position Method", "Chord Lines to Root", COLORS['accent_cyan']),
    ("Figure 4", "Newton-Raphson Method", "Tangent Line Iterations", COLORS['accent_orange']),
    ("Figure 5", "Secant Method", "Chord Line Iterations", COLORS['accent_purple']),
    ("Figure 6", "Convergence Comparison", "All Four Methods (Log Scale)", COLORS['accent_red']),
]


# ============================================================================
# Interactive Plot Window
# ============================================================================
class InteractivePlotWindow(tk.Toplevel):
    """A window that displays an interactive matplotlib figure."""

    def __init__(self, master, title, plot_func, color):
        super().__init__(master)
        self.title(title)
        self.geometry("1100x750")
        self.configure(bg=COLORS['bg_dark'])
        self.minsize(800, 600)

        # Title bar
        title_frame = tk.Frame(self, bg=color, height=4)
        title_frame.pack(fill='x')

        header = tk.Frame(self, bg=COLORS['bg_dark'], pady=8)
        header.pack(fill='x')
        tk.Label(header, text=title, font=('Segoe UI', 14, 'bold'),
                 fg=COLORS['text_primary'], bg=COLORS['bg_dark']).pack()

        # Coordinate display label
        self.coord_label = tk.Label(
            self, text="  Hover over the plot to see coordinates",
            font=('Consolas', 11), fg=COLORS['accent_cyan'],
            bg=COLORS['bg_card'], padx=15, pady=6, anchor='w',
            relief='flat'
        )
        self.coord_label.pack(fill='x', padx=10, pady=(0, 5))

        # Create the matplotlib figure
        self.fig = Figure(figsize=(10, 6), dpi=100, facecolor='white')
        self.ax = self.fig.add_subplot(111)

        # Call the specific plotting function
        self.scatter_data = []  # Will hold (x, y, label) tuples for hover
        plot_func(self.fig, self.ax, self)

        # Embed in tkinter
        canvas_frame = tk.Frame(self, bg=COLORS['bg_dark'])
        canvas_frame.pack(fill='both', expand=True, padx=10, pady=(0, 5))

        self.canvas = FigureCanvasTkAgg(self.fig, master=canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        # Navigation toolbar (zoom, pan, save)
        toolbar_frame = tk.Frame(self, bg='#e5e7eb')
        toolbar_frame.pack(fill='x', padx=10, pady=(0, 10))
        self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        self.toolbar.update()

        # --- Hover annotation ---
        self.annot = self.ax.annotate(
            "", xy=(0, 0), xytext=(15, 15),
            textcoords="offset points",
            bbox=dict(boxstyle="round,pad=0.4", fc="#1e293b", ec="#3b82f6", alpha=0.95),
            arrowprops=dict(arrowstyle="->", color="#3b82f6", lw=1.5),
            fontsize=9, color='white', fontfamily='monospace',
            zorder=100
        )
        self.annot.set_visible(False)
        self._annot_visible = False  # Track state to avoid redundant redraws

        # Connect mouse events
        self.canvas.mpl_connect("motion_notify_event", self._on_hover)

    def add_scatter_point(self, x, y, label=""):
        """Register a point for hover detection."""
        self.scatter_data.append((x, y, label))

    def _on_hover(self, event):
        """Handle mouse hover to show coordinates."""
        if event.inaxes != self.ax:
            if self._annot_visible:
                self.annot.set_visible(False)
                self._annot_visible = False
                self.canvas.draw_idle()
            self.coord_label.config(text="  Hover over the plot to see coordinates")
            return

        x, y = event.xdata, event.ydata

        # Update the coordinate display bar
        try:
            fx_val = f(x)
            self.coord_label.config(
                text=f"  Cursor: x = {x:.6f}   |   y = {y:.6f}   |   f(x) = {fx_val:.6f}"
            )
        except (OverflowError, ValueError):
            self.coord_label.config(
                text=f"  Cursor: x = {x:.6f}   |   y = {y:.6f}"
            )

        # Check if near any registered scatter point
        if self.scatter_data:
            try:
                display_coords = self.ax.transData.transform(
                    np.array([(px, py) for px, py, _ in self.scatter_data])
                )
                cursor_display = self.ax.transData.transform(np.array([[x, y]]))[0]

                distances = np.sqrt(np.sum((display_coords - cursor_display) ** 2, axis=1))
                min_idx = np.argmin(distances)
                min_dist = distances[min_idx]

                if min_dist < 25:  # Within 25 pixels
                    px, py, label = self.scatter_data[min_idx]
                    self.annot.xy = (px, py)
                    text = f"x = {px:.7f}\ny = {py:.7f}"
                    if label:
                        text = f"{label}\n{text}"
                    self.annot.set_text(text)
                    if not self._annot_visible:
                        self.annot.set_visible(True)
                        self._annot_visible = True
                    self.canvas.draw_idle()
                    return
            except Exception:
                pass

        if self._annot_visible:
            self.annot.set_visible(False)
            self._annot_visible = False
            self.canvas.draw_idle()


# ============================================================================
# FIGURE 1: Graph of f(x)
# ============================================================================
def plot_figure1(fig, ax, window):
    x = np.linspace(-0.5, 2.0, 500)
    y = f_np(x)

    ax.plot(x, y, color='#2563eb', linewidth=2.5, label=r'$f(x) = e^{-x} - x$', zorder=3)

    # Shade regions
    x_pos = x[y >= 0]
    y_pos = y[y >= 0]
    x_neg = x[y < 0]
    y_neg = y[y < 0]
    ax.fill_between(x_pos, y_pos, 0, alpha=0.12, color='#22c55e', label=r'$f(x) > 0$')
    ax.fill_between(x_neg, y_neg, 0, alpha=0.12, color='#ef4444', label=r'$f(x) < 0$')

    # Root marker
    ax.plot(TRUE_ROOT, 0, 'o', color='#ef4444', markersize=12, zorder=5,
            markeredgecolor='white', markeredgewidth=2,
            label=r'Root $x^* \approx 0.5671433$')
    window.add_scatter_point(TRUE_ROOT, 0, "ROOT")

    # Annotate
    ax.annotate(r'Root $x^* \approx 0.5671$',
                xy=(TRUE_ROOT, 0), xytext=(TRUE_ROOT + 0.3, 0.5),
                fontsize=12, fontweight='bold', color='#ef4444',
                arrowprops=dict(arrowstyle='->', color='#ef4444', lw=2),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#fef2f2', edgecolor='#ef4444', alpha=0.9))

    # Bracket points
    f0 = f(0)
    f1 = f(1)
    ax.plot(0, f0, 's', color='#22c55e', markersize=8, zorder=4)
    ax.annotate(f'f(0) = {f0:.1f}', xy=(0, f0), xytext=(-0.4, f0 + 0.15),
                fontsize=10, color='#22c55e', fontweight='bold')
    window.add_scatter_point(0, f0, "f(0)")

    ax.plot(1, f1, 's', color='#ef4444', markersize=8, zorder=4)
    ax.annotate(f'f(1) = {f1:.3f}', xy=(1, f1), xytext=(1.1, f1 - 0.15),
                fontsize=10, color='#ef4444', fontweight='bold')
    window.add_scatter_point(1, f1, "f(1)")

    # Sample points along the curve for hover
    sample_x = np.linspace(-0.3, 1.8, 40)
    for sx in sample_x:
        window.add_scatter_point(float(sx), float(f(float(sx))), "f(x)")

    ax.axhline(y=0, color='#6b7280', linewidth=1, linestyle='--', alpha=0.7)
    ax.axvline(x=TRUE_ROOT, color='#ef4444', linewidth=0.8, linestyle=':', alpha=0.5)
    ax.set_xlabel('x', fontsize=13)
    ax.set_ylabel('f(x)', fontsize=13)
    ax.set_title(r'Figure 1: Graph of $f(x) = e^{-x} - x$ -- Root Identification',
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=10, loc='upper right', framealpha=0.9)
    ax.set_xlim(-0.5, 2.0)
    ax.set_ylim(-1.2, 1.8)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()


# ============================================================================
# FIGURE 2: Bisection Method
# ============================================================================
def plot_figure2(fig, ax, window):
    x = np.linspace(-0.1, 1.2, 500)
    y = f_np(x)
    ax.plot(x, y, color='#2563eb', linewidth=2.5, label=r'$f(x) = e^{-x} - x$', zorder=2)
    ax.axhline(y=0, color='#6b7280', linewidth=1, linestyle='--', alpha=0.7)

    # Run bisection
    a, b = 0.0, 1.0
    midpoints = []
    for _ in range(20):
        c = (a + b) / 2.0
        midpoints.append(c)
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c

    # Plot first 10 midpoints
    n_show = 10
    cmap = plt.cm.YlOrRd
    colors = [cmap(0.15 + 0.75 * i / (n_show - 1)) for i in range(n_show)]

    for i in range(n_show):
        c = midpoints[i]
        fc = f(c)
        ax.plot(c, fc, 's', markersize=9, color=colors[i], zorder=5,
                markeredgecolor='white', markeredgewidth=1.5,
                label=f'$c_{{{i+1}}}$ = {c:.4f}')
        ax.plot([c, c], [0, fc], '--', color=colors[i], linewidth=0.8, alpha=0.6)
        window.add_scatter_point(c, fc, f"Midpoint c{i+1}")

    # True root
    ax.plot(TRUE_ROOT, 0, '*', color='#ef4444', markersize=18, zorder=6,
            markeredgecolor='white', markeredgewidth=1, label=r'True root $x^*$')
    window.add_scatter_point(TRUE_ROOT, 0, "TRUE ROOT")

    # Set limits before placing text so positions are correct
    ax.set_xlim(-0.05, 1.1)
    ax.set_ylim(-0.5, 1.1)

    ax.axvspan(0, 1, alpha=0.04, color='#3b82f6')
    ax.text(0.02, -0.4, '$a = 0$', fontsize=10, color='#3b82f6', fontweight='bold')
    ax.text(0.92, -0.4, '$b = 1$', fontsize=10, color='#3b82f6', fontweight='bold')

    ax.set_xlabel('x', fontsize=13)
    ax.set_ylabel('f(x)', fontsize=13)
    ax.set_title('Figure 2: Bisection Method -- Successive Midpoints',
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=8, loc='upper right', ncol=2, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()


# ============================================================================
# FIGURE 3: False Position Method
# ============================================================================
def plot_figure3(fig, ax, window):
    x = np.linspace(-0.1, 1.2, 500)
    y = f_np(x)
    ax.plot(x, y, color='#2563eb', linewidth=2.5, label=r'$f(x) = e^{-x} - x$', zorder=2)
    ax.axhline(y=0, color='#6b7280', linewidth=1, linestyle='--', alpha=0.7)

    a, b = 0.0, 1.0
    n_show = 6
    cmap = plt.cm.cool
    colors = [cmap(0.15 + 0.7 * i / (n_show - 1)) for i in range(n_show)]

    for i in range(8):
        fa, fb = f(a), f(b)
        c = a - fa * (b - a) / (fb - fa)

        if i < n_show:
            x_chord = np.linspace(a - 0.05, b + 0.05, 50)
            slope = (fb - fa) / (b - a)
            y_chord = fa + slope * (x_chord - a)
            ax.plot(x_chord, y_chord, '--', color=colors[i], linewidth=1.2, alpha=0.7)

            fc = f(c)
            ax.plot(c, fc, 'o', markersize=9, color=colors[i], zorder=5,
                    markeredgecolor='white', markeredgewidth=1.5,
                    label=f'$c_{{{i+1}}}$ = {c:.5f}')
            window.add_scatter_point(c, fc, f"Estimate c{i+1}")

        if fa * f(c) < 0:
            b = c
        else:
            a = c

    ax.plot(TRUE_ROOT, 0, '*', color='#ef4444', markersize=18, zorder=6,
            markeredgecolor='white', markeredgewidth=1, label=r'True root $x^*$')
    window.add_scatter_point(TRUE_ROOT, 0, "TRUE ROOT")

    ax.set_xlabel('x', fontsize=13)
    ax.set_ylabel('f(x)', fontsize=13)
    ax.set_title('Figure 3: False Position Method -- Chord Lines to Root',
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=9, loc='upper right', framealpha=0.9)
    ax.set_xlim(-0.1, 1.15)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()


# ============================================================================
# FIGURE 4: Newton-Raphson Method
# ============================================================================
def plot_figure4(fig, ax, window):
    x = np.linspace(-0.2, 1.2, 500)
    y = f_np(x)
    ax.plot(x, y, color='#2563eb', linewidth=2.5, label=r'$f(x) = e^{-x} - x$', zorder=2)
    ax.axhline(y=0, color='#6b7280', linewidth=1, linestyle='--', alpha=0.7)

    xn = 0.0
    colors_nr = ['#e11d48', '#f97316', '#eab308', '#22c55e']
    markers = ['o', 's', 'D', '^']

    for i in range(4):
        fx = f(xn)
        fpx = f_prime(xn)
        xn_new = xn - fx / fpx

        # Tangent line
        t = np.linspace(xn - 0.25, xn + 0.7, 100)
        tangent = fx + fpx * (t - xn)
        ax.plot(t, tangent, '--', color=colors_nr[i], linewidth=1.3, alpha=0.7)

        # Point on curve
        ax.plot(xn, fx, markers[i], markersize=10, color=colors_nr[i], zorder=5,
                markeredgecolor='white', markeredgewidth=1.5,
                label=f'$x_{{{i}}}$ = {xn:.5f}')
        window.add_scatter_point(xn, fx, f"Iterate x{i}")

        # Vertical drop
        ax.plot([xn, xn], [0, fx], ':', color=colors_nr[i], linewidth=1, alpha=0.5)

        # Arrow on x-axis
        if i < 3:
            ax.annotate('', xy=(xn_new, 0.015), xytext=(xn, 0.015),
                        arrowprops=dict(arrowstyle='->', color=colors_nr[i], lw=1.5))

        xn = xn_new

    ax.plot(TRUE_ROOT, 0, '*', color='#ef4444', markersize=18, zorder=6,
            markeredgecolor='white', markeredgewidth=1, label=r'True root $x^*$')
    window.add_scatter_point(TRUE_ROOT, 0, "TRUE ROOT")

    ax.set_xlabel('x', fontsize=13)
    ax.set_ylabel('f(x)', fontsize=13)
    ax.set_title('Figure 4: Newton-Raphson Method -- Tangent Line Iterations',
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=9, loc='upper right', framealpha=0.9)
    ax.set_xlim(-0.2, 1.15)
    ax.set_ylim(-0.7, 1.2)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()


# ============================================================================
# FIGURE 5: Secant Method
# ============================================================================
def plot_figure5(fig, ax, window):
    x = np.linspace(-0.2, 1.2, 500)
    y = f_np(x)
    ax.plot(x, y, color='#2563eb', linewidth=2.5, label=r'$f(x) = e^{-x} - x$', zorder=2)
    ax.axhline(y=0, color='#6b7280', linewidth=1, linestyle='--', alpha=0.7)

    x_prev, x_curr = 0.0, 1.0
    colors_sec = ['#7c3aed', '#a855f7', '#c084fc', '#d8b4fe', '#ede9fe']

    # Mark x0
    ax.plot(0, f(0), 'o', markersize=9, color='#4b5563', zorder=5,
            markeredgecolor='white', markeredgewidth=1.5, label='$x_0$ = 0.000')
    window.add_scatter_point(0, f(0), "x0")

    # Mark x1
    ax.plot(1, f(1), 'o', markersize=9, color='#6b7280', zorder=5,
            markeredgecolor='white', markeredgewidth=1.5, label='$x_1$ = 1.000')
    window.add_scatter_point(1, f(1), "x1")

    for i in range(5):
        fp_val = f(x_prev)
        fc_val = f(x_curr)
        x_new = x_curr - fc_val * (x_curr - x_prev) / (fc_val - fp_val)

        if i < 4:
            lo = min(x_prev, x_curr) - 0.15
            hi = max(x_prev, x_curr) + 0.15
            t = np.linspace(lo, hi, 100)
            slope = (fc_val - fp_val) / (x_curr - x_prev)
            secant_y = fc_val + slope * (t - x_curr)
            ax.plot(t, secant_y, '--', color=colors_sec[i], linewidth=1.3, alpha=0.7)

            fn = f(x_new)
            ax.plot(x_new, fn, 'D', markersize=8, color=colors_sec[i], zorder=5,
                    markeredgecolor='white', markeredgewidth=1.5,
                    label=f'$x_{{{i+2}}}$ = {x_new:.5f}')
            window.add_scatter_point(x_new, fn, f"Iterate x{i+2}")

        x_prev = x_curr
        x_curr = x_new

    ax.plot(TRUE_ROOT, 0, '*', color='#ef4444', markersize=18, zorder=6,
            markeredgecolor='white', markeredgewidth=1, label=r'True root $x^*$')
    window.add_scatter_point(TRUE_ROOT, 0, "TRUE ROOT")

    ax.set_xlabel('x', fontsize=13)
    ax.set_ylabel('f(x)', fontsize=13)
    ax.set_title('Figure 5: Secant Method -- Chord Line Iterations',
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=9, loc='upper right', framealpha=0.9)
    ax.set_xlim(-0.2, 1.15)
    ax.set_ylim(-0.7, 1.2)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()


# ============================================================================
# FIGURE 6: Convergence Comparison
# ============================================================================
def plot_figure6(fig, ax, window):
    # Bisection errors
    a, b = 0.0, 1.0
    bisection_errors = []
    for _ in range(20):
        c = (a + b) / 2.0
        bisection_errors.append(abs(c - TRUE_ROOT))
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c

    # False Position errors
    a, b = 0.0, 1.0
    fp_errors = []
    for _ in range(8):
        fa, fb = f(a), f(b)
        c = a - fa * (b - a) / (fb - fa)
        fp_errors.append(abs(c - TRUE_ROOT))
        if fa * f(c) < 0:
            b = c
        else:
            a = c

    # Newton-Raphson errors
    xn = 0.0
    nr_errors = []
    for _ in range(4):
        fpx = f_prime(xn)
        xn_new = xn - f(xn) / fpx
        nr_errors.append(abs(xn_new - TRUE_ROOT))
        xn = xn_new

    # Secant errors
    x_prev, x_curr = 0.0, 1.0
    sec_errors = []
    for _ in range(5):
        fp_val = f(x_prev)
        fc_val = f(x_curr)
        x_new = x_curr - fc_val * (x_curr - x_prev) / (fc_val - fp_val)
        sec_errors.append(abs(x_new - TRUE_ROOT))
        x_prev = x_curr
        x_curr = x_new

    # Plot
    ax.semilogy(range(1, len(bisection_errors) + 1), bisection_errors,
                'o-', color='#e74c3c', linewidth=2, markersize=5,
                markeredgecolor='white', markeredgewidth=1, label='Bisection')
    ax.semilogy(range(1, len(fp_errors) + 1), fp_errors,
                's-', color='#2ecc71', linewidth=2, markersize=6,
                markeredgecolor='white', markeredgewidth=1, label='False Position')
    ax.semilogy(range(1, len(nr_errors) + 1), nr_errors,
                '^-', color='#3498db', linewidth=2, markersize=8,
                markeredgecolor='white', markeredgewidth=1, label='Newton-Raphson')
    ax.semilogy(range(1, len(sec_errors) + 1), sec_errors,
                'D-', color='#9b59b6', linewidth=2, markersize=7,
                markeredgecolor='white', markeredgewidth=1, label='Secant')

    # Register all data points for hover
    for i, e in enumerate(bisection_errors):
        window.add_scatter_point(i + 1, e, f"Bisection iter {i+1}")
    for i, e in enumerate(fp_errors):
        window.add_scatter_point(i + 1, e, f"False Position iter {i+1}")
    for i, e in enumerate(nr_errors):
        window.add_scatter_point(i + 1, e, f"Newton-Raphson iter {i+1}")
    for i, e in enumerate(sec_errors):
        window.add_scatter_point(i + 1, e, f"Secant iter {i+1}")

    ax.set_xlabel('Iteration', fontsize=13)
    ax.set_ylabel('Absolute Error (log scale)', fontsize=13)
    ax.set_title('Figure 6: Convergence Comparison -- All Four Methods',
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=11, loc='upper right', framealpha=0.9)
    ax.grid(True, alpha=0.3, which='both')
    ax.set_xlim(0.5, 20.5)
    fig.tight_layout()


# ============================================================================
# Save All Figures as PNG (replaces plot_graphs.py)
# ============================================================================
FIGURE_FILENAMES = [
    'figure1_graph.png',
    'figure2_bisection.png',
    'figure3_false_position.png',
    'figure4_newton_raphson.png',
    'figure5_secant.png',
    'figure6_convergence.png',
]

PLOT_FUNCTIONS_LIST = [plot_figure1, plot_figure2, plot_figure3,
                       plot_figure4, plot_figure5, plot_figure6]


class _DummyWindow:
    """Minimal stand-in for InteractivePlotWindow so plot functions can call add_scatter_point."""
    def add_scatter_point(self, x, y, label=""):
        pass  # No-op for static export


def save_all_figures(status_callback=None):
    """Render all 6 figures and save as PNG files to the plots/ directory."""
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plots")
    os.makedirs(output_dir, exist_ok=True)
    dummy = _DummyWindow()

    for i, (plot_func, filename) in enumerate(zip(PLOT_FUNCTIONS_LIST, FIGURE_FILENAMES)):
        fig = Figure(figsize=(10, 6), dpi=200, facecolor='white')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#f8f9fa')
        ax.grid(True, alpha=0.3)
        plot_func(fig, ax, dummy)
        filepath = os.path.join(output_dir, filename)
        fig.savefig(filepath, bbox_inches='tight')
        plt.close('all')
        if status_callback:
            status_callback(i + 1, 6, filename)

    return output_dir


# ============================================================================
# Main Application Window
# ============================================================================
class MainApp(tk.Tk):
    """Main menu window with buttons to open each interactive figure."""

    PLOT_FUNCTIONS = [plot_figure1, plot_figure2, plot_figure3,
                      plot_figure4, plot_figure5, plot_figure6]

    def __init__(self):
        super().__init__()
        self.title("CSM 258 - Numerical Methods Visualization")
        self.geometry("720x680")
        self.configure(bg=COLORS['bg_dark'])
        self.resizable(True, True)
        self.minsize(600, 550)

        self._build_ui()

    def _build_ui(self):
        # ---- Gradient accent line ----
        accent = tk.Frame(self, bg=COLORS['accent_blue'], height=3)
        accent.pack(fill='x')

        # ---- Title ----
        title_frame = tk.Frame(self, bg=COLORS['bg_card'], pady=20, padx=20)
        title_frame.pack(fill='x', padx=15, pady=(15, 5))

        tk.Label(title_frame,
                 text="CSM 258: Numerical Methods and Computations",
                 font=('Segoe UI', 18, 'bold'),
                 fg=COLORS['accent_cyan'], bg=COLORS['bg_card']).pack()
        tk.Label(title_frame,
                 text="Group 2 Assignment - Solving Transcendental Equations",
                 font=('Segoe UI', 11),
                 fg=COLORS['text_secondary'], bg=COLORS['bg_card']).pack(pady=(4, 0))

        # ---- Equation box ----
        eq_frame = tk.Frame(self, bg='#0c4a6e', pady=10, padx=15)
        eq_frame.pack(fill='x', padx=15, pady=10)

        tk.Label(eq_frame,
                 text="f(x) = e^(-x) - x = 0   |   True Root: x* = 0.5671433 (Omega constant)",
                 font=('Consolas', 11, 'bold'),
                 fg=COLORS['accent_cyan'], bg='#0c4a6e').pack()

        # ---- Instruction ----
        tk.Label(self,
                 text="Click any figure below to open an interactive plot:",
                 font=('Segoe UI', 10),
                 fg=COLORS['text_muted'], bg=COLORS['bg_dark']).pack(pady=(5, 8))

        # ---- Button Grid ----
        grid_frame = tk.Frame(self, bg=COLORS['bg_dark'])
        grid_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)

        for i, (title, subtitle, desc, color) in enumerate(FIGURE_BUTTONS):
            row = i // 2
            col = i % 2
            self._create_button(grid_frame, i, title, subtitle, desc, color, row, col)

        # ---- Save All Button ----
        save_frame = tk.Frame(self, bg=COLORS['bg_dark'], pady=5)
        save_frame.pack(fill='x', padx=15)

        self.save_btn = tk.Button(
            save_frame, text="  Save All Figures as PNG  ",
            font=('Segoe UI', 10, 'bold'),
            fg='white', bg='#16a34a', activebackground='#15803d',
            activeforeground='white', cursor='hand2', relief='flat',
            padx=15, pady=6, command=self._save_all
        )
        self.save_btn.pack(side='left')

        self.save_status = tk.Label(
            save_frame, text="",
            font=('Segoe UI', 9), fg=COLORS['accent_green'],
            bg=COLORS['bg_dark']
        )
        self.save_status.pack(side='left', padx=10)

        # ---- Footer ----
        footer = tk.Frame(self, bg=COLORS['bg_dark'], pady=8)
        footer.pack(fill='x')
        tk.Label(footer,
                 text="Hover over data points to see exact coordinates  |  Use toolbar to zoom & pan",
                 font=('Segoe UI', 9),
                 fg=COLORS['text_muted'], bg=COLORS['bg_dark']).pack()

    def _create_button(self, parent, index, title, subtitle, desc, color, row, col):
        """Create a styled card button."""
        btn_frame = tk.Frame(parent, bg=COLORS['bg_card'], padx=2, pady=2,
                             highlightbackground=color, highlightthickness=1)
        btn_frame.grid(row=row, column=col, padx=6, pady=6, sticky='nsew')
        parent.rowconfigure(row, weight=1)

        # Color accent bar at top
        accent_bar = tk.Frame(btn_frame, bg=color, height=4)
        accent_bar.pack(fill='x')

        # Content
        content = tk.Frame(btn_frame, bg=COLORS['bg_card'], padx=12, pady=10, cursor='hand2')
        content.pack(fill='both', expand=True)

        lbl_title = tk.Label(content, text=title, font=('Segoe UI', 13, 'bold'),
                             fg=color, bg=COLORS['bg_card'], cursor='hand2')
        lbl_title.pack(anchor='w')

        lbl_sub = tk.Label(content, text=subtitle, font=('Segoe UI', 10),
                           fg=COLORS['text_primary'], bg=COLORS['bg_card'], cursor='hand2')
        lbl_sub.pack(anchor='w', pady=(2, 0))

        lbl_desc = tk.Label(content, text=desc, font=('Segoe UI', 9),
                            fg=COLORS['text_muted'], bg=COLORS['bg_card'], cursor='hand2')
        lbl_desc.pack(anchor='w', pady=(1, 0))

        # All clickable widgets
        all_widgets = [content, lbl_title, lbl_sub, lbl_desc]

        def on_click(event, idx=index):
            self._open_figure(idx)

        def on_enter(event):
            for w in all_widgets:
                w.configure(bg=COLORS['bg_hover'])
            btn_frame.configure(highlightthickness=2)

        def on_leave(event):
            # Only leave if mouse actually left the card entirely
            x, y = btn_frame.winfo_pointerxy()
            widget_under = btn_frame.winfo_containing(x, y)
            if widget_under and (widget_under == btn_frame or
                                 widget_under in all_widgets or
                                 widget_under == accent_bar):
                return  # Still inside the card
            for w in all_widgets:
                w.configure(bg=COLORS['bg_card'])
            btn_frame.configure(highlightthickness=1)

        for widget in all_widgets:
            widget.bind('<Button-1>', on_click)
            widget.bind('<Enter>', on_enter)
            widget.bind('<Leave>', on_leave)

        # Also bind leave to the frame itself
        btn_frame.bind('<Leave>', on_leave)

    def _open_figure(self, index):
        """Open the interactive plot window for the given figure index."""
        title, subtitle, desc, color = FIGURE_BUTTONS[index]
        full_title = f"{title}: {subtitle} - {desc}"
        plot_func = self.PLOT_FUNCTIONS[index]
        InteractivePlotWindow(self, full_title, plot_func, color)

    def _save_all(self):
        """Save all 6 figures as PNG files."""
        self.save_btn.config(state='disabled', text='  Saving...  ', bg='#4b5563')
        self.save_status.config(text="")
        self.update_idletasks()

        def on_progress(current, total, filename):
            self.save_status.config(text=f"Saved {current}/{total}: {filename}")
            self.update_idletasks()

        try:
            output_dir = save_all_figures(status_callback=on_progress)
            self.save_status.config(
                text=f"All 6 figures saved to: {output_dir}",
                fg=COLORS['accent_green']
            )
        except Exception as e:
            self.save_status.config(text=f"Error: {e}", fg=COLORS['accent_red'])
        finally:
            self.save_btn.config(state='normal', text='  Save All Figures as PNG  ', bg='#16a34a')


# ============================================================================
# Entry Point
# ============================================================================
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
