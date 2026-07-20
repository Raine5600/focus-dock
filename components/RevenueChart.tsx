import type { DailyPoint } from "@/lib/analytics";
import { formatAmount } from "@/lib/purchases";

const W = 720;
const H = 210;
const PAD_L = 46;
const PAD_R = 8;
const PAD_T = 16;
const PAD_B = 30;

/**
 * Last-N-days revenue — server-rendered SVG, single teal series.
 * Native <title> tooltips per bar; value label only on the peak day;
 * recessive grid; text in ink tokens (never the series color).
 */
export function RevenueChart({ daily }: { daily: DailyPoint[] }) {
  const plotW = W - PAD_L - PAD_R;
  const plotH = H - PAD_T - PAD_B;
  const max = Math.max(...daily.map((d) => d.revenue), 2700); // ≥ one sale so the scale never lies
  const step = plotW / daily.length;
  const barW = Math.min(26, step * 0.55);
  const peak = daily.reduce((m, d, i) => (d.revenue > daily[m].revenue ? i : m), 0);
  const hasSales = daily.some((d) => d.revenue > 0);

  const y = (v: number) => PAD_T + plotH * (1 - v / max);

  const gridVals = [max, max / 2];

  return (
    <svg
      viewBox={`0 0 ${W} ${H}`}
      role="img"
      aria-label={`Daily revenue, last ${daily.length} days`}
      className="w-full"
    >
      {/* recessive grid + y labels */}
      {gridVals.map((v) => (
        <g key={v}>
          <line
            x1={PAD_L}
            x2={W - PAD_R}
            y1={y(v)}
            y2={y(v)}
            stroke="var(--border)"
            strokeWidth="1"
            strokeDasharray="2 4"
          />
          <text
            x={PAD_L - 8}
            y={y(v) + 3.5}
            textAnchor="end"
            fontSize="10"
            fill="var(--ink-lt)"
          >
            {formatAmount(v, "usd").replace(".00", "")}
          </text>
        </g>
      ))}
      {/* baseline */}
      <line
        x1={PAD_L}
        x2={W - PAD_R}
        y1={PAD_T + plotH}
        y2={PAD_T + plotH}
        stroke="var(--border)"
        strokeWidth="1"
      />

      {daily.map((d, i) => {
        const x = PAD_L + i * step + (step - barW) / 2;
        const h = d.revenue > 0 ? Math.max(4, (d.revenue / max) * plotH) : 0;
        const showLabel = i % 2 === 0 || daily.length <= 8;
        return (
          <g key={d.date}>
            {d.revenue > 0 ? (
              <rect
                x={x}
                y={PAD_T + plotH - h}
                width={barW}
                height={h}
                rx="3"
                fill="#2a9d8f"
              >
                <title>{`${d.label}: ${formatAmount(d.revenue, "usd")} · ${d.sales} sale${d.sales === 1 ? "" : "s"}`}</title>
              </rect>
            ) : (
              <rect
                x={x}
                y={PAD_T + plotH - 2}
                width={barW}
                height={2}
                fill="var(--border)"
              >
                <title>{`${d.label}: no sales`}</title>
              </rect>
            )}
            {i === peak && d.revenue > 0 ? (
              <text
                x={x + barW / 2}
                y={y(d.revenue) - 6}
                textAnchor="middle"
                fontSize="10.5"
                fontWeight="700"
                fill="var(--ink)"
              >
                {formatAmount(d.revenue, "usd").replace(".00", "")}
              </text>
            ) : null}
            {showLabel ? (
              <text
                x={x + barW / 2}
                y={H - 10}
                textAnchor="middle"
                fontSize="9.5"
                fill="var(--ink-lt)"
              >
                {d.label}
              </text>
            ) : null}
          </g>
        );
      })}

      {!hasSales ? (
        <text
          x={PAD_L + plotW / 2}
          y={PAD_T + plotH / 2}
          textAnchor="middle"
          fontSize="12"
          fill="var(--ink-lt)"
        >
          No sales in this window yet — bars appear as purchases come in.
        </text>
      ) : null}
    </svg>
  );
}
