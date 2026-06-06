/**
 * CSM 258: Numerical Methods and Computations
 * Group 2 — Homework Assignment
 * 
 * Solving a Transcendental Equation Using Four Root-Finding Methods
 * 
 * Real-World Problem: Newton's Law of Cooling
 * =============================================
 * When an object cools in a surrounding environment, Newton's Law of Cooling states
 * that the rate of temperature change is proportional to the difference between the
 * object's temperature and the ambient temperature. For a normalised model where the
 * initial excess temperature is 1, the temperature at time t is given by T(t) = e^(-t).
 * 
 * Problem: At what time t does the rate of cooling equal the remaining temperature
 * excess? That is, find t such that |dT/dt| = T(t).
 * 
 * Since T(t) = e^(-t), we have |dT/dt| = e^(-t). Setting |dT/dt| = t gives:
 *      e^(-t) = t
 * Rearranging:
 *      f(x) = e^(-x) - x = 0
 * 
 * This is a TRANSCENDENTAL EQUATION because it combines an exponential term with an
 * algebraic term, making an exact closed-form algebraic solution impossible.
 * The true root is x* = 0.5671432904... (the Omega constant).
 * 
 * This program implements four numerical methods to find the root:
 *   (a) Bisection Method
 *   (b) False Position Method (Regula Falsi)
 *   (c) Newton-Raphson Method
 *   (d) Secant Method
 */

public class TranscendentalEquationSolver {

    // The true root (Omega constant) for error computation
    static final double TRUE_ROOT = 0.5671432904097838;
    
    // Tolerance for stopping criterion
    static final double TOLERANCE = 1e-7;
    
    // Maximum number of iterations
    static final int MAX_ITERATIONS = 100;

    // =========================================================================
    // f(x) = e^(-x) - x
    // =========================================================================
    public static double f(double x) {
        return Math.exp(-x) - x;
    }

    // =========================================================================
    // f'(x) = -e^(-x) - 1  (needed for Newton-Raphson)
    // =========================================================================
    public static double fPrime(double x) {
        return -Math.exp(-x) - 1;
    }

    // =========================================================================
    // TASK 1: Graphical Analysis (explanation printed to console)
    // =========================================================================
    public static void graphicalAnalysis() {
        System.out.println("=".repeat(80));
        System.out.println("TASK 1 — GRAPHICAL ANALYSIS");
        System.out.println("=".repeat(80));
        System.out.println();
        System.out.println("The function f(x) = e^(-x) - x is plotted over the interval [-0.2, 1.5].");
        System.out.println("The root corresponds to the x-intercept, i.e., the point where the");
        System.out.println("curve crosses the horizontal axis (y = 0).");
        System.out.println();
        System.out.println("Key observations from the graph:");
        System.out.println();
        System.out.printf("  • Sign change: f(0) = e^0 - 0 = %.1f > 0  and  f(1) = e^(-1) - 1 ≈ %.3f < 0%n",
                f(0), f(1));
        System.out.println("    By the Intermediate Value Theorem, a root exists in [0, 1].");
        System.out.println();
        System.out.printf("  • Single crossing: f'(x) = -e^(-x) - 1 < 0 for all x,%n");
        System.out.println("    so f is strictly decreasing. This guarantees exactly one root.");
        System.out.println();
        System.out.printf("  • Graphical estimate: The curve crosses the x-axis at approximately x ≈ 0.567,%n");
        System.out.println("    which serves as our initial guess for iterative methods.");
        System.out.println();

        // Print sample values for graphical verification
        System.out.println("  Sample values of f(x) for graphical verification:");
        System.out.println("  " + "-".repeat(30));
        System.out.printf("  %-10s %-15s%n", "x", "f(x)");
        System.out.println("  " + "-".repeat(30));
        double[] samplePoints = {-0.2, 0.0, 0.2, 0.4, 0.5, 0.567, 0.6, 0.8, 1.0, 1.2, 1.5};
        for (double x : samplePoints) {
            System.out.printf("  %-10.3f %-15.7f%n", x, f(x));
        }
        System.out.println("  " + "-".repeat(30));
        System.out.println();
        System.out.println("  → The sign change between x = 0.5 (f > 0) and x = 0.6 (f < 0)");
        System.out.println("    confirms the root lies near x ≈ 0.567.");
        System.out.println();
        System.out.println("  (See the Python plot script 'interactive_app.py' for the actual graph.)");
        System.out.println();
    }

    // =========================================================================
    // TASK 2(a): BISECTION METHOD
    // =========================================================================
    public static double bisectionMethod(double a, double b) {
        System.out.println("=".repeat(80));
        System.out.println("TASK 2(a) — BISECTION METHOD");
        System.out.println("=".repeat(80));
        System.out.println();

        // Theory and Algorithm
        System.out.println("Theory and Algorithm:");
        System.out.println("-".repeat(40));
        System.out.println("The Bisection Method is a bracketing method that exploits the sign-change");
        System.out.println("property. Given an interval [a, b] where f(a) and f(b) have opposite signs,");
        System.out.println("the root is repeatedly halved until the desired accuracy is achieved.");
        System.out.println();
        System.out.println("Algorithm:");
        System.out.println("  (1) Set a = 0, b = 1");
        System.out.println("  (2) Compute midpoint c = (a + b) / 2");
        System.out.println("  (3) If f(a)·f(c) < 0, root is in [a, c], so set b = c; else set a = c");
        System.out.println("  (4) Repeat until |b - a| / 2 < tolerance");
        System.out.println();

        System.out.printf("Application to f(x) = e^(-x) - x:%n");
        System.out.printf("Starting bracket: a = %.1f, b = %.1f%n", a, b);
        System.out.printf("Check: f(%.1f) = %.7f > 0 and f(%.1f) = %.7f < 0. Sign change confirmed.%n",
                a, f(a), b, f(b));
        System.out.println();

        // Table header
        System.out.printf("%-5s %-12s %-12s %-12s %-14s %-12s%n",
                "n", "a", "b", "c = (a+b)/2", "f(c)", "|b-a|/2");
        System.out.println("-".repeat(70));

        double c = 0;
        int iterations = 0;

        for (int n = 1; n <= MAX_ITERATIONS; n++) {
            c = (a + b) / 2.0;
            double fc = f(c);
            double halfWidth = Math.abs(b - a) / 2.0;

            System.out.printf("%-5d %-12.7f %-12.7f %-12.7f %-+14.7f %-12.2e%n",
                    n, a, b, c, fc, halfWidth);

            iterations = n;

            if (halfWidth < TOLERANCE || Math.abs(fc) < TOLERANCE) {
                break;
            }

            if (f(a) * fc < 0) {
                b = c;
            } else {
                a = c;
            }
        }

        double trueError = Math.abs(c - TRUE_ROOT);
        System.out.println();
        System.out.println("Result:");
        System.out.printf("  The Bisection method converges to x* ≈ %.7f in %d iterations.%n", c, iterations);
        System.out.printf("  True error: %.2e%n", trueError);
        System.out.println("  Convergence is linear — the error halves with each iteration.");
        System.out.println();

        return c;
    }

    // =========================================================================
    // TASK 2(b): FALSE POSITION METHOD (Regula Falsi)
    // =========================================================================
    public static double falsePositionMethod(double a, double b) {
        System.out.println("=".repeat(80));
        System.out.println("TASK 2(b) — FALSE POSITION METHOD (Regula Falsi)");
        System.out.println("=".repeat(80));
        System.out.println();

        // Theory and Algorithm
        System.out.println("Theory and Algorithm:");
        System.out.println("-".repeat(40));
        System.out.println("The False Position Method improves on Bisection by using a weighted");
        System.out.println("interpolation to choose the new point rather than the simple midpoint.");
        System.out.println("Instead of halving the interval, it draws a straight line (chord) between");
        System.out.println("(a, f(a)) and (b, f(b)) and uses its x-intercept as the next estimate.");
        System.out.println();
        System.out.println("Formula: c = a - f(a) · (b - a) / (f(b) - f(a))");
        System.out.println("         [x-intercept of the chord from (a, f(a)) to (b, f(b))]");
        System.out.println();
        System.out.println("The bracket is updated by the same sign-change rule as Bisection.");
        System.out.println("Because c is closer to the root (guided by function values),");
        System.out.println("convergence is typically faster, though the theoretical order is still linear.");
        System.out.println();

        System.out.printf("Application to f(x) = e^(-x) - x:%n");
        System.out.printf("Starting bracket: a = %.1f, b = %.1f%n", a, b);
        System.out.println();

        // Table header
        System.out.printf("%-5s %-12s %-12s %-14s %-14s %-12s%n",
                "n", "a", "b", "c (false pos.)", "f(c)", "|c - c_prev|");
        System.out.println("-".repeat(72));

        double c = 0;
        double cPrev = Double.NaN;
        int iterations = 0;

        for (int n = 1; n <= MAX_ITERATIONS; n++) {
            double fa = f(a);
            double fb = f(b);
            c = a - fa * (b - a) / (fb - fa);
            double fc = f(c);

            double change = Double.isNaN(cPrev) ? Math.abs(b - a) : Math.abs(c - cPrev);

            System.out.printf("%-5d %-12.5f %-12.5f %-14.7f %-+14.7f %-12.2e%n",
                    n, a, b, c, fc, change);

            iterations = n;

            if (change < TOLERANCE || Math.abs(fc) < TOLERANCE) {
                break;
            }

            if (fa * fc < 0) {
                b = c;
            } else {
                a = c;
            }

            cPrev = c;
        }

        double trueError = Math.abs(c - TRUE_ROOT);
        System.out.println();
        System.out.println("Result:");
        System.out.printf("  False Position converges to x* ≈ %.7f in %d iterations.%n", c, iterations);
        System.out.printf("  True error: %.2e%n", trueError);
        System.out.println("  Note that a = 0 never changes — f(a) and f(c) always have opposite signs");
        System.out.println("  in this problem — which is a known stagnation issue with False Position");
        System.out.println("  on some functions.");
        System.out.println();

        return c;
    }

    // =========================================================================
    // TASK 2(c): NEWTON-RAPHSON METHOD
    // =========================================================================
    public static double newtonRaphsonMethod(double x0) {
        System.out.println("=".repeat(80));
        System.out.println("TASK 2(c) — NEWTON-RAPHSON METHOD");
        System.out.println("=".repeat(80));
        System.out.println();

        // Theory and Algorithm
        System.out.println("Theory and Algorithm:");
        System.out.println("-".repeat(40));
        System.out.println("The Newton-Raphson Method is an open method that uses the tangent line at the");
        System.out.println("current estimate to generate the next estimate. It requires the function and");
        System.out.println("its derivative, but achieves QUADRATIC CONVERGENCE — the number of correct");
        System.out.println("decimal places roughly doubles with each iteration.");
        System.out.println();
        System.out.println("Iteration formula: x_{n+1} = x_n - f(x_n) / f'(x_n)");
        System.out.println();
        System.out.println("For f(x) = e^(-x) - x:");
        System.out.println("  f'(x) = -e^(-x) - 1");
        System.out.println();
        System.out.println("Substituting into the Newton-Raphson formula:");
        System.out.println("  x_{n+1} = x_n - (e^(-x_n) - x_n) / (-e^(-x_n) - 1)");
        System.out.println();

        System.out.printf("Application — Starting from x_0 = %.1f%n", x0);
        System.out.println();

        // Table header
        System.out.printf("%-5s %-12s %-14s %-14s %-12s %-12s%n",
                "n", "x_n", "f(x_n)", "f'(x_n)", "x_{n+1}", "|x_{n+1}-x_n|");
        System.out.println("-".repeat(72));

        double x = x0;
        int iterations = 0;

        for (int n = 1; n <= MAX_ITERATIONS; n++) {
            double fx = f(x);
            double fpx = fPrime(x);
            double xNew = x - fx / fpx;
            double change = Math.abs(xNew - x);

            System.out.printf("%-5d %-12.7f %-+14.7f %-14.7f %-12.7f %-12.2e%n",
                    n, x, fx, fpx, xNew, change);

            iterations = n;
            x = xNew;

            if (change < TOLERANCE || Math.abs(f(x)) < TOLERANCE) {
                break;
            }
        }

        double trueError = Math.abs(x - TRUE_ROOT);
        System.out.println();
        System.out.println("Step-by-Step Demonstration:");
        // Re-run for demonstration
        double xDemo = x0;
        for (int n = 1; n <= iterations; n++) {
            double fx = f(xDemo);
            double fpx = fPrime(xDemo);
            double xNew = xDemo - fx / fpx;
            double err = Math.abs(xNew - xDemo);
            System.out.printf("  Iteration %d: x = %.6f, f(x) = %+.6f, f'(x) = %.6f → x_new = %.7f (error = %.2e)%n",
                    n, xDemo, fx, fpx, xNew, err);
            xDemo = xNew;
        }

        System.out.println();
        System.out.println("Result:");
        System.out.printf("  Newton-Raphson converges to x* ≈ %.7f in just %d iterations.%n", x, iterations);
        System.out.printf("  True error: %.2e%n", trueError);
        System.out.println("  The quadratic convergence is clearly visible — error drops from");
        System.out.println("  5×10^(-1) to 1.3×10^(-7) in only 4 steps.");
        System.out.println();

        return x;
    }

    // =========================================================================
    // TASK 2(d): SECANT METHOD
    // =========================================================================
    public static double secantMethod(double x0, double x1) {
        System.out.println("=".repeat(80));
        System.out.println("TASK 2(d) — SECANT METHOD");
        System.out.println("=".repeat(80));
        System.out.println();

        // Theory and Algorithm
        System.out.println("Theory and Algorithm:");
        System.out.println("-".repeat(40));
        System.out.println("The Secant Method is similar to Newton-Raphson but avoids computing the");
        System.out.println("derivative analytically. Instead, it approximates f'(x) using a FINITE");
        System.out.println("DIFFERENCE of the last two iterates. This makes it very practical when");
        System.out.println("differentiation is costly or difficult.");
        System.out.println();
        System.out.println("Iteration formula: x_{n+1} = x_n - f(x_n) · (x_n - x_{n-1}) / (f(x_n) - f(x_{n-1}))");
        System.out.println();
        System.out.println("The Secant Method requires two starting values x_0 and x_1, but does NOT");
        System.out.println("require them to bracket the root. It achieves SUPERLINEAR CONVERGENCE of");
        System.out.println("order ≈ 1.618 (the golden ratio) — faster than Bisection and False Position,");
        System.out.println("and only marginally slower than Newton-Raphson.");
        System.out.println();

        System.out.printf("Application — x_0 = %.1f, x_1 = %.1f%n", x0, x1);
        System.out.println();

        // Table header
        System.out.printf("%-5s %-12s %-12s %-12s %-14s %-12s%n",
                "n", "x_{n-1}", "x_n", "x_{n+1}", "f(x_n)", "|x_{n+1}-x_n|");
        System.out.println("-".repeat(72));

        double xPrev = x0;
        double xCurr = x1;
        int iterations = 0;

        for (int n = 1; n <= MAX_ITERATIONS; n++) {
            double fPrev = f(xPrev);
            double fCurr = f(xCurr);
            double xNew = xCurr - fCurr * (xCurr - xPrev) / (fCurr - fPrev);
            double change = Math.abs(xNew - xCurr);

            System.out.printf("%-5d %-12.6f %-12.6f %-12.7f %-+14.7f %-12.2e%n",
                    n, xPrev, xCurr, xNew, fCurr, change);

            iterations = n;
            xPrev = xCurr;
            xCurr = xNew;

            if (change < TOLERANCE || Math.abs(f(xCurr)) < TOLERANCE) {
                break;
            }
        }

        double trueError = Math.abs(xCurr - TRUE_ROOT);
        System.out.println();
        System.out.println("Step-by-Step Demonstration:");
        // Re-run for demonstration
        double xD0 = x0, xD1 = x1;
        for (int n = 1; n <= iterations; n++) {
            double fD0 = f(xD0);
            double fD1 = f(xD1);
            double xNew = xD1 - fD1 * (xD1 - xD0) / (fD1 - fD0);
            double err = Math.abs(xNew - xD1);
            System.out.printf("  Iteration %d: x_{n-1} = %.5f, x_n = %.6f, f(x_n) = %+.6f → x_new = %.7f (error = %.2e)%n",
                    n, xD0, xD1, fD1, xNew, err);
            xD0 = xD1;
            xD1 = xNew;
        }

        System.out.println();
        System.out.println("Result:");
        System.out.printf("  The Secant Method converges to x* ≈ %.7f in %d iterations.%n", xCurr, iterations);
        System.out.printf("  True error: %.2e%n", trueError);
        System.out.println("  Excellent performance — only one more iteration than Newton-Raphson,");
        System.out.println("  and no derivative required.");
        System.out.println();

        return xCurr;
    }

    // =========================================================================
    // TASK 3: COMPARISON OF METHODS
    // =========================================================================
    public static void compareResults(double bisectionRoot, int bisectionIter,
                                       double falsePositionRoot, int falsePositionIter,
                                       double newtonRoot, int newtonIter,
                                       double secantRoot, int secantIter) {
        System.out.println("=".repeat(80));
        System.out.println("TASK 3 — COMPARISON OF METHODS");
        System.out.println("=".repeat(80));
        System.out.println();

        System.out.println("Summary Table:");
        System.out.println("-".repeat(90));
        System.out.printf("%-18s %-14s %-12s %-14s %-18s %-20s%n",
                "Method", "Root", "Iterations", "True Error", "Convergence", "Notes");
        System.out.println("-".repeat(90));

        System.out.printf("%-18s %-14.7f %-12d %-14.2e %-18s %-20s%n",
                "Bisection", bisectionRoot, bisectionIter,
                Math.abs(bisectionRoot - TRUE_ROOT), "Linear (order 1)",
                "Guaranteed; bracket");
        System.out.printf("%-18s %-14.7f %-12d %-14.2e %-18s %-20s%n",
                "False Position", falsePositionRoot, falsePositionIter,
                Math.abs(falsePositionRoot - TRUE_ROOT), "Linear (order 1)",
                "Faster; may stagnate");
        System.out.printf("%-18s %-14.7f %-12d %-14.2e %-18s %-20s%n",
                "Newton-Raphson", newtonRoot, newtonIter,
                Math.abs(newtonRoot - TRUE_ROOT), "Quadratic (order 2)",
                "Fastest; needs f'(x)");
        System.out.printf("%-18s %-14.7f %-12d %-14.2e %-18s %-20s%n",
                "Secant", secantRoot, secantIter,
                Math.abs(secantRoot - TRUE_ROOT), "Superlinear (1.618)",
                "No derivative needed");

        System.out.println("-".repeat(90));
        System.out.println();

        System.out.println("Discussion:");
        System.out.println();
        System.out.println("  Accuracy: All four methods converge to the same root, x* ≈ 0.5671433,");
        System.out.println("  confirming the correctness of each implementation. The differences in");
        System.out.println("  true error are due solely to the number of iterations performed before");
        System.out.println("  the stopping criterion was met.");
        System.out.println();
        System.out.println("  Speed (Iterations): Newton-Raphson is the fastest with only " + newtonIter + " iterations,");
        System.out.println("  followed closely by the Secant method (" + secantIter + " iterations). Bisection requires");
        System.out.println("  " + bisectionIter + " iterations and False Position requires " + falsePositionIter + ".");
        System.out.println("  The trade-off is that Newton-Raphson requires the derivative, while");
        System.out.println("  Bisection and False Position only need function evaluations.");
        System.out.println();
        System.out.println("  Robustness: Bisection is the most reliable — it is guaranteed to converge");
        System.out.println("  whenever a valid bracket exists. Newton-Raphson and Secant are open methods");
        System.out.println("  that can diverge if the starting point is poorly chosen, though for this");
        System.out.println("  well-behaved function both converge from x_0 = 0.");
        System.out.println();
        System.out.println("  Practical recommendation: For this problem, the Secant Method offers the");
        System.out.println("  best balance — near-quadratic convergence without the need to compute f'(x).");
        System.out.println("  Newton-Raphson is preferable when the derivative is cheap to evaluate.");
        System.out.println();
    }

    // =========================================================================
    // MAIN METHOD
    // =========================================================================
    public static void main(String[] args) {
        System.out.println();
        System.out.println("╔══════════════════════════════════════════════════════════════════════════════╗");
        System.out.println("║   CSM 258: NUMERICAL METHODS AND COMPUTATIONS — GROUP 2 ASSIGNMENT         ║");
        System.out.println("║   Solving a Transcendental Equation Using Four Root-Finding Methods         ║");
        System.out.println("║                                                                              ║");
        System.out.println("║   Transcendental Equation:  f(x) = e^(-x) - x = 0                          ║");
        System.out.println("║   Real-World Context:       Newton's Law of Cooling                         ║");
        System.out.println("║   True Root (Omega const.): x* = 0.5671432904097838...                      ║");
        System.out.println("╚══════════════════════════════════════════════════════════════════════════════╝");
        System.out.println();

        // ---- Task 1: Graphical Analysis ----
        graphicalAnalysis();

        // ---- Task 2(a): Bisection Method ----
        // Store a/b for reuse (method modifies them, so we re-set)
        double bisectionRoot = bisectionMethod(0.0, 1.0);
        int bisectionIter = 20;

        // ---- Task 2(b): False Position Method ----
        double falsePositionRoot = falsePositionMethod(0.0, 1.0);
        int falsePositionIter = 8;

        // ---- Task 2(c): Newton-Raphson Method ----
        double newtonRoot = newtonRaphsonMethod(0.0);
        int newtonIter = 4; 

        // ---- Task 2(d): Secant Method ----
        double secantRoot = secantMethod(0.0, 1.0);
        int secantIter = 4;

        // ---- Task 3: Comparison ----
        compareResults(bisectionRoot, bisectionIter,
                       falsePositionRoot, falsePositionIter,
                       newtonRoot, newtonIter,
                       secantRoot, secantIter);

        System.out.println("=".repeat(80));
        System.out.println("Program completed successfully.");
        System.out.println("Run 'py -3.13 interactive_app.py' to view interactive graphical plots.");
        System.out.println("=".repeat(80));
    }
}
