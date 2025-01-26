'use client'

export function mapP(
    from: number,
    to: number,
    progress: number,
) {
    return from + (to - from) * progress;
}

export function rangeP(
    from: number,
    to: number,
    progress: number,
) {
    if (progress >= to) return 1;
    if (progress <= from) return 0;
    const alpha = 1 / (to - from);
    const result = alpha * (progress - from);
    return Math.max(0, Math.min(result, 1));
}
