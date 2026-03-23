import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

const BLUE  = "#1a3080";
const GOLD  = "#c8a96e";
const BLUE2 = "#2a50c8";

/* ── Positions dots sur le ring extérieur ── */
const BLUE_DOTS = [0, 60, 120, 180, 240, 300];   // degrés
const GOLD_DOTS = [30, 90, 150, 210, 270, 330];

function polar(cx: number, cy: number, r: number, deg: number) {
  const rad = (deg - 90) * (Math.PI / 180);
  return { x: cx + r * Math.cos(rad), y: cy + r * Math.sin(rad) };
}

export const AnimatedLogo: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const cx = 100, cy = 100;
  const R1 = 82;  // outer ring
  const R2 = 62;  // gold ring
  const R3 = 42;  // inner arc

  /* ── Cercles draw-in ── */
  const sp0 = spring({ frame,      fps, config: { damping: 22, stiffness: 60, mass: 1 } });
  const sp1 = spring({ frame: frame - 6,  fps, config: { damping: 22, stiffness: 60 } });
  const sp2 = spring({ frame: frame - 12, fps, config: { damping: 22, stiffness: 60 } });

  const c1Len = 2 * Math.PI * R1;
  const c2Len = 2 * Math.PI * R2;
  const c3Len = 2 * Math.PI * R3 * 0.78; // arc 78%

  /* ── Rotation continue du ring extérieur ── */
  const rot = frame * 0.25;

  /* ── Éléments centraux ── */
  const centerSp = spring({ frame: frame - 14, fps, config: { damping: 14, stiffness: 130 } });
  const lineSp   = spring({ frame: frame - 18, fps, config: { damping: 18, stiffness: 100 } });

  /* ── Pulse central hub ── */
  const pulse = 1 + Math.sin(frame * 0.1) * 0.08;

  /* ── Opacité dots avec stagger ── */
  const dotOpacity = (i: number, delay: number) =>
    interpolate(frame - delay - i * 1.5, [0, 12], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <svg
      viewBox="0 0 200 200"
      style={{ width: "100%", height: "100%", overflow: "visible" }}
    >
      {/* ── Ring extérieur bleu ── */}
      <circle
        cx={cx} cy={cy} r={R1}
        fill="none" stroke={BLUE} strokeWidth="1.4"
        strokeDasharray={`${c1Len * sp0} ${c1Len}`}
        transform={`rotate(${rot}, ${cx}, ${cy})`}
        strokeLinecap="round"
      />

      {/* ── Ring or ── */}
      <circle
        cx={cx} cy={cy} r={R2}
        fill="none" stroke={GOLD} strokeWidth="0.9"
        strokeDasharray={`${c2Len * sp1} ${c2Len}`}
        transform={`rotate(${-rot * 0.6}, ${cx}, ${cy})`}
        strokeLinecap="round"
      />

      {/* ── Arc intérieur bleu (3/4) ── */}
      <circle
        cx={cx} cy={cy} r={R3}
        fill="none" stroke={BLUE} strokeWidth="1"
        strokeDasharray={`${c3Len * sp2} ${c1Len}`}
        transform={`rotate(${rot * 0.4 + 30}, ${cx}, ${cy})`}
        strokeLinecap="round"
        opacity={0.7}
      />

      {/* ── Dots bleus sur ring extérieur (tournent avec le ring) ── */}
      {BLUE_DOTS.map((deg, i) => {
        const { x, y } = polar(cx, cy, R1, deg + rot);
        return (
          <circle key={`bd${i}`}
            cx={x} cy={y} r={5}
            fill={BLUE}
            opacity={dotOpacity(i, 3)}
          />
        );
      })}

      {/* ── Dots or ── */}
      {GOLD_DOTS.map((deg, i) => {
        const { x, y } = polar(cx, cy, R1, deg + rot);
        return (
          <circle key={`gd${i}`}
            cx={x} cy={y} r={3.5}
            fill={GOLD}
            opacity={dotOpacity(i, 5)}
          />
        );
      })}

      {/* ── Lignes circuit (L-shape style PCB) ── */}
      {/* Grand carré bleu → hub */}
      <polyline
        points={`${73 * lineSp + (1 - lineSp) * cx},${75 * lineSp + (1 - lineSp) * cy} ${93 * lineSp + (1 - lineSp) * cx},${75 * lineSp + (1 - lineSp) * cy} ${cx},${cy}`}
        fill="none" stroke={BLUE} strokeWidth="1.3"
        opacity={lineSp}
        strokeLinecap="round" strokeLinejoin="round"
      />
      {/* Petit carré bleu → hub */}
      <polyline
        points={`${71 * lineSp + (1 - lineSp) * cx},${95 * lineSp + (1 - lineSp) * cy} ${cx},${95 * lineSp + (1 - lineSp) * cy} ${cx},${cy}`}
        fill="none" stroke={BLUE} strokeWidth="1.1"
        opacity={lineSp}
        strokeLinecap="round" strokeLinejoin="round"
      />
      {/* Carré or → hub */}
      <polyline
        points={`${112 * lineSp + (1 - lineSp) * cx},${74 * lineSp + (1 - lineSp) * cy} ${cx},${74 * lineSp + (1 - lineSp) * cy} ${cx},${cy}`}
        fill="none" stroke={GOLD} strokeWidth="1.1"
        opacity={lineSp}
        strokeLinecap="round" strokeLinejoin="round"
      />

      {/* ── Grand carré bleu (top-left) ── */}
      <rect
        x={57} y={58}
        width={34 * centerSp} height={34 * centerSp}
        rx={4 * centerSp}
        fill={BLUE}
        opacity={centerSp}
      />

      {/* ── Carré or (milieu-droite) ── */}
      <rect
        x={103} y={64}
        width={22 * centerSp} height={22 * centerSp}
        rx={3 * centerSp}
        fill={GOLD}
        opacity={centerSp}
      />

      {/* ── Petit carré bleu (bas-gauche) ── */}
      <rect
        x={60} y={85}
        width={24 * centerSp} height={24 * centerSp}
        rx={3 * centerSp}
        fill={BLUE2}
        opacity={centerSp * 0.85}
      />

      {/* ── Hub central pulsant ── */}
      {/* Halo */}
      <circle
        cx={cx} cy={cy} r={10 * pulse * centerSp}
        fill={BLUE} opacity={0.12 * centerSp}
      />
      {/* Dot central */}
      <circle
        cx={cx} cy={cy} r={7 * centerSp}
        fill={BLUE}
        opacity={centerSp}
      />
    </svg>
  );
};
