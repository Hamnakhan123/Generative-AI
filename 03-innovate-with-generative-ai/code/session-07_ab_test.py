"""
Session 7 · Example 2 — Did headline B really win? A two-proportion z-test.

AI can write ten headline variants in seconds, but "B got more clicks" might
be luck. The z-test compares two click-through rates:
  p = pooled rate, SE = sqrt(p(1-p)(1/nA + 1/nB)),  z = (pB - pA) / SE
|z| >= 1.96 means the difference is significant at the 95% level.
Only the standard library is needed (math.erf gives the normal curve).

Run:  python session-07_ab_test.py
"""
from math import erf, sqrt


def ab_test(clicks_a, n_a, clicks_b, n_b):
    pa, pb = clicks_a / n_a, clicks_b / n_b
    pooled = (clicks_a + clicks_b) / (n_a + n_b)
    se = sqrt(pooled * (1 - pooled) * (1 / n_a + 1 / n_b))
    z = (pb - pa) / se
    p_value = 2 * (1 - 0.5 * (1 + erf(abs(z) / sqrt(2))))
    return pa, pb, z, p_value


tests = [
    ("Small test", 12, 400, 19, 400),
    ("Same rates, 10x traffic", 120, 4000, 190, 4000),
]
print("A: 'Admissions open for 2027'   B: 'Your CS career starts here: apply by 15 Jan'")
for name, ca, na, cb, nb in tests:
    pa, pb, z, p = ab_test(ca, na, cb, nb)
    verdict = "B wins (significant)" if p < 0.05 else "not significant: keep testing"
    print(f"{name:24} CTR A={pa:.2%} B={pb:.2%}  lift={(pb/pa-1):+.0%}  z={z:.2f}  p={p:.4f}  -> {verdict}")
