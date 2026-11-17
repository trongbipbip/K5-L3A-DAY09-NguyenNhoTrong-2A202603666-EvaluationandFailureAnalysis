"""Statistics students implement (M2 judge calibration, M4 paired bootstrap).

Rules: a judge is a classifier -- measure it like one. A higher mean is not
"better" until the paired CI of the difference excludes 0.
Reference values to self-check are in tests/test_lab9_stats.py.
"""

from __future__ import annotations

from collections.abc import Sequence

POS = "FAIL"   # the judge's job is to FIND failures, so FAIL is the positive class


def confusion(human: Sequence[str], judge: Sequence[str]) -> dict[str, int]:
    """tp/fp/fn/tn with FAIL as positive."""
    if len(human) != len(judge):
        raise ValueError("human and judge must have the same length")
    tp = fp = fn = tn = 0
    for h, j in zip(human, judge):
        h_fail, j_fail = h == POS, j == POS
        if h_fail and j_fail:
            tp += 1
        elif not h_fail and j_fail:
            fp += 1
        elif h_fail and not j_fail:
            fn += 1
        else:
            tn += 1
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn}


def precision_recall(human: Sequence[str], judge: Sequence[str]) -> tuple[float, float]:
    # Precision = tp/(tp+fp), recall = tp/(tp+fn); zero when a denominator is 0.
    cm = confusion(human, judge)
    precision = cm["tp"] / (cm["tp"] + cm["fp"]) if cm["tp"] + cm["fp"] else 0.0
    recall = cm["tp"] / (cm["tp"] + cm["fn"]) if cm["tp"] + cm["fn"] else 0.0
    return precision, recall


def cohen_kappa(human: Sequence[str], judge: Sequence[str]) -> float:
    """kappa = (p_o - p_e) / (1 - p_e). Raise ValueError when undefined (p_e == 1):
    a constant judge has no signal and must FAIL calibration, not pass on a technicality."""
    if len(human) != len(judge):
        raise ValueError("human and judge must have the same length")
    n = len(human)
    if not n:
        raise ValueError("kappa is undefined for an empty sample")
    cm = confusion(human, judge)
    p_o = (cm["tp"] + cm["tn"]) / n
    human_fail = (cm["tp"] + cm["fn"]) / n
    judge_fail = (cm["tp"] + cm["fp"]) / n
    p_e = human_fail * judge_fail + (1.0 - human_fail) * (1.0 - judge_fail)
    if p_e == 1.0:
        raise ValueError("kappa is undefined when expected agreement is 1")
    return (p_o - p_e) / (1.0 - p_e)


def rogan_gladen(observed_rate: float, sensitivity: float, specificity: float) -> float:
    """Correct an observed failure rate for judge error; clip to [0, 1]."""
    denominator = sensitivity + specificity - 1.0
    if denominator <= 0:
        raise ValueError("sensitivity + specificity must be greater than 1")
    corrected = (observed_rate + specificity - 1.0) / denominator
    return max(0.0, min(1.0, corrected))


def paired_bootstrap(a: Sequence[float], b: Sequence[float], *, n_resamples: int = 1000,
                     rng: int = 2027, confidence: float = 0.95) -> tuple[float, float, float]:
    """a[i], b[i] = per-item mean over seeds, SAME items, SAME order.
    Return (mean(a)-mean(b), lo, hi) with scipy.stats.bootstrap(paired=True, method="percentile",
    rng=numpy.random.default_rng(rng)). If a == b everywhere return (0.0, 0.0, 0.0)."""
    if len(a) != len(b) or not a:
        raise ValueError("paired bootstrap requires two non-empty sequences of equal length")
    if n_resamples <= 0 or not 0.0 < confidence < 1.0:
        raise ValueError("invalid bootstrap parameters")
    import numpy as np
    from scipy.stats import bootstrap

    left = np.asarray(a, dtype=float)
    right = np.asarray(b, dtype=float)
    observed = float(np.mean(left) - np.mean(right))
    if np.array_equal(left, right):
        return 0.0, 0.0, 0.0

    def statistic(x, y, axis=0):
        return np.mean(x, axis=axis) - np.mean(y, axis=axis)

    result = bootstrap(
        (left, right), statistic, paired=True, n_resamples=n_resamples,
        confidence_level=confidence, method="percentile",
        rng=np.random.default_rng(rng), vectorized=True,
    )
    return observed, float(result.confidence_interval.low), float(result.confidence_interval.high)


def pass_at_k(n: int, c: int, k: int) -> float:
    """Probability that AT LEAST ONE of k trials drawn from n (c of them passing) passes.
    Unbiased estimator (Chen et al. 2021): 1 - C(n-c, k) / C(n, k). Raise ValueError if k > n."""
    # TODO M6
    raise NotImplementedError


def pass_hat_k(n: int, c: int, k: int) -> float:
    """pass^k (tau-bench, Yao et al. 2024): probability that ALL k trials drawn from n pass.
    Unbiased estimator: C(c, k) / C(n, k). Raise ValueError if k > n.
    pass^k <= pass@1 <= pass@k; a reliable agent keeps pass^k close to pass@1."""
    # TODO M6
    raise NotImplementedError
