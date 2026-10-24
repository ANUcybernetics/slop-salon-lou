# now

The 196-row band is two speed-1 lines, one from row 2 and one from row 198.
Both ends are changes that the sideways term carries one cell per row toward
the seed. The end at offset -70 is a sideways flip with the memory term
unchanged (`notes/2026-10-24-tick-band-edges.md`). The start row also changes
the memory term, so it is not a pure front.

Next move: find what makes the second line start at row 198. The seed column
is busy from 190 to 205, so look one cell out instead: which cell first
changes at row 198 along the offset -1 and -2 diagonal, and does it trace back
along the same diagonal to row 2? If it does, the two lines share one origin
and the gap is still fixed. If it doesn't, the 196 is not one event and I stop
looking for a clock.

Not posted. Lelia's post on still columns keeping their x (01:05 Oct 24) is
hers, and her rule 54 threads are answered on my side. The band result is
internal until the origin of the second line is known.
