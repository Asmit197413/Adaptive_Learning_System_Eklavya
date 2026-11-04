"""Evidence for the adaptive engine: simulate students whose true level is known and
measure how well each method finds it.   python evaluate.py
Simulated student: answers correctly 90% of the time at or below their true level, 15% above it."""
import random

import engine

STUDENTS, CHECK = 3000, (1, 2, 3, 5, 8)


class Step:                      # simple rule: one level up after right, one down after wrong
    def __init__(self, start): self.l = start
    def level(self): return self.l
    def update(self, d, ok): self.l = min(3, self.l + 1) if ok else max(1, self.l - 1)


class Mastery:                   # the engine's mastery model
    def __init__(self): self.p = engine.START_MASTERY
    def level(self): return engine.level_from_mastery(self.p)
    def update(self, d, ok): self.p = engine.bkt_update(self.p, ok, d)


def simulate(make, learn_rate, seed=11):
    rng, hits, steady = random.Random(seed), {k: 0 for k in CHECK}, 0.0
    for _ in range(STUDENTS):
        true, m, late = rng.choice((1, 2, 3)), make(), 0
        for k in range(1, 9):
            d = m.level()
            m.update(d, rng.random() < (0.9 if d <= true else 0.15))
            if true < 3 and rng.random() < learn_rate: true += 1   # the student improves with practice
            hit = m.level() == true
            if k in hits: hits[k] += hit
            if k >= 4: late += hit
        steady += late / 5
    return [round(100 * hits[k] / STUDENTS) for k in CHECK], round(100 * steady / STUDENTS)


if __name__ == "__main__":
    print(f"{STUDENTS} simulated students, true level 1/2/3 (random guessing finds it ~33% of the time)")
    for title, rate in (("Students who do NOT improve", 0.0), ("Students who improve (10% chance per question)", 0.10)):
        print(f"\n{title}\n{'method':<24}" + "".join(f"{'Q'+str(k):>6}" for k in CHECK) + f"{'steady Q4-8':>13}")
        for name, make in (("+-1 step, start easy", lambda: Step(1)), ("+-1 step, start medium", lambda: Step(2)),
                           ("mastery model (ours)", Mastery)):
            row, steady = simulate(make, rate)
            print(f"{name:<24}" + "".join(f"{str(v)+'%':>6}" for v in row) + f"{str(steady)+'%':>13}")
