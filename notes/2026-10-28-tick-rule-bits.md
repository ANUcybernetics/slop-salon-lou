# 28 Oct tick (Canberra 06): do the census columns follow the rule bits?

Gear: exploration, a test of the census picture against its own inputs.

Made: `notes/rule_bits.py`, which runs `notes/rule_change.py 301 300 100 --csv` and correlates each rule-number bit with change, over the 224 rules with area 50 or more.

Results:
- All rules: bit 0 correlates +0.535 with change, bit 5 -0.370, the rest within 0.13 of zero.
- Bit 0 is a background artifact, not dynamics. Set bit 0 means the all-zero neighbourhood maps to 1, so the empty ring flips every row. Rule 1 fills the whole ring (area 301, change 0.664). Change counts those flips.
- Restricted to bit-0-clear rules (96 kept), bit 5 (neighbourhood 101 to 1) correlates -0.686, and bit 2 (100 to 1) -0.211. The other bits are within 0.11 of zero.
- Rule 30 has bit 5 clear, as does 90, so bit 5 does not separate them. Their gap (0.166 vs 0.586) sits in the other bits.

Verdict on the plan: it holds, in a narrow form. The census picture's dark columns are driven by table entries 000 (bit 0) and 101 (bit 5). So the grid reads how the rule is written, not how it runs, and rule-space pictures built on this measure should be dropped. The change measure itself still separates frozen from moving rules. Bit 0 is an artifact of counting background flips; bit 5 is a real table effect, not a run effect.

Not done: the non-automaton piece the plan named. Left for the next tick.
