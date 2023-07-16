"""
Use this script to generate critical chi-square values.

For each number of degrees of freedom, there is a critical value.
Therefore, the output is a list of chi-square values.
These values additionally depend on the so-called significance level.
You can adjust both parameters below; then run the main method.

You need scipy to run this script!
"""

from scipy.stats import chi2

degrees_freedom = range(1, 10000)
"""
Range of degrees of freedom.
Distributions with many different values (bins) have many degrees of freedom.

From 1 to any positive integer.
"""

significance = 0.05
"""
Significance level.
Probability of rejecting the null hypothesis when it is in fact true (false negative).

A lower significance level means you are conservative
and require more evidence before rejecting the null hypothesis.
This increases the number of true positives and of false positives.

A higher significance level means you are lenient
and require less evidence before rejecting the null hypothesis.
This increases the number true negatives and of false negatives.

From 0 to 1.
"""

chi_squared_values = [chi2.ppf(1 - significance, df) for df in degrees_freedom]
print("({})".format(", ".join(["{:0.2f}".format(x) for x in chi_squared_values])))
