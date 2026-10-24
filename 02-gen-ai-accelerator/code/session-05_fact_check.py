"""Verify AI claims against a trusted source before you reuse them.
Here the 'trusted source' is a small dictionary; in real life it is an official site or textbook."""
trusted = {"boiling point of water at sea level (C)": 100,
           "speed of light (km/s)": 299792,
           "number of provinces in Pakistan": 4}
ai_claims = {"boiling point of water at sea level (C)": 100,
             "speed of light (km/s)": 300000,
             "number of provinces in Pakistan": 5}

for claim, value in ai_claims.items():
    truth = trusted[claim]
    err = abs(value - truth) / truth
    verdict = "OK" if err == 0 else ("ROUNDED" if err < 0.01 else "WRONG - fix before use")
    print(f"{claim:42} AI={value:<8} source={truth:<8} {verdict}")
