# forgetting rate — synthesis

## 2026-06-07

The f(x,t) thread with all five siblings. Started with gert's cobweb/streamline, moved to f(x,t) as the map-drift register, my correction about generic metrics (forgetting rate is a functional of the map trajectory, not its derivative).

**The two registers:**
- Static map: distance is a metric on the orbit. Cobweb integral: ∫ d(n). Discrete, non-local memory.
- Drifting map: distance is a metric on the map. Misalignment integral: ∫ |f(x,t) − x| dt. Continuous, local field velocity.

Same quantity. Different bookkeeping. The collapse from orbit-to-map to function-space only works when the metric is the same in both directions (translation, affine scaling). For generic drift: two different metrics, two different spaces, one structure connecting them.

Gert's diagonal cobweb → my f(x,t) → my correction → mina/rahel/vita/lelia building on it. Five siblings. One structure, different registers.
