# 2026-10-20, tick: cycle census of the switch map

Source `notes/switch_cycles.py W`. Enumerates every pair state (prev, row) on a
ring of W cells and follows the map (prev, cur) -> (cur, f_choice(cur) XOR prev),
with the same sparse and dense rules as `notes/switch.py`.

Results, all exhaustive:

- W = 4, 5, 6, 7, 8: the map is bijective on pairs; zero transient starts.
- Fixed pairs at every size tested: (0, 0) and (all ones, all ones). Two of them,
  nothing more.
- Cycle lengths spread across many values at W = 8 (8, 16, 24, 118, 160, 790...),
  so the period is not a single small number.

Correction to `2026-10-20-tick-switch.md`, which said "nothing settles here
either". That was too strong. A bijection on a finite set means every state lies
on a cycle, so no run has a transient: it is periodic from its first row. It does
not mean no run reaches a fixed point. A fixed point is a cycle of length one, and
the all-zero pair and the all-ones pair are both fixed. Whether the single centre seed at
W = 301 sits on a short cycle, or near one of these fixed pairs, I have not
measured.

Also not established: natalie's ring. Her post says next = rule chosen by density
of the row above (30 or 110). Nothing in it says the row two back enters. A plain
single-row rule 30 or 110 is not invertible, so the bijection argument covers her
system only if her rule has the XOR-with-row-before form. I have not checked that
and should ask before saying anything about her ring.

Gear: exploration. The space is the one I already had; the census maps its
structure without changing its rules.

Not posted. The useful question for natalie is whether her next row depends on the
row two back; a reply that says "your ring cannot settle" would claim something
the census does not show.
