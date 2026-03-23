import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
  Sequence,
} from "remotion";
import { AnimatedLogo } from "./AnimatedLogo";

/* ── Palette AKYRA ── */
const C = {
  bg:     "#f7f4ef",
  blue:   "#1a3080",
  blue2:  "#2a50c8",
  gold:   "#c8a96e",
  muted:  "#8a7f72",
  dark:   "#1e1a16",
};

/* ── Steps du Tick Engine ── */
const STEPS = [
  { num: "01", label: "PERCEIVE",  sub: "Read on-chain state",   color: C.blue  },
  { num: "02", label: "REMEMBER",  sub: "Query Qdrant memory",   color: C.blue  },
  { num: "03", label: "DECIDE",    sub: "LLM inference",         color: C.blue2 },
  { num: "04", label: "ACT",       sub: "Execute on-chain TX",   color: C.blue  },
  { num: "05", label: "MEMORIZE",  sub: "Store in vector DB",    color: C.gold  },
];

/* ── Easing helper ── */
function easeOut(x: number) {
  return 1 - Math.pow(1 - x, 3);
}

/* ── Composant Step ── */
const Step: React.FC<{
  step: typeof STEPS[0];
  delay: number;
  isLast: boolean;
}> = ({ step, delay, isLast }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame: frame - delay,
    fps,
    config: { damping: 14, mass: 0.8, stiffness: 120 },
  });

  const opacity  = interpolate(progress, [0, 1], [0, 1]);
  const translateY = interpolate(progress, [0, 1], [28, 0]);

  return (
    <div style={{ display: "flex", alignItems: "center", gap: 0 }}>
      {/* Step card */}
      <div
        style={{
          opacity,
          transform: `translateY(${translateY}px)`,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 12,
          width: 180,
        }}
      >
        {/* Circle num */}
        <div
          style={{
            width: 56,
            height: 56,
            borderRadius: "50%",
            background: step.color,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontFamily: "'JetBrains Mono', monospace",
            fontSize: 13,
            fontWeight: 700,
            color: "#fff",
            letterSpacing: "0.05em",
            boxShadow: `0 0 24px ${step.color}44`,
          }}
        >
          {step.num}
        </div>

        {/* Label */}
        <div
          style={{
            fontFamily: "sans-serif",
            fontWeight: 700,
            fontSize: 13,
            letterSpacing: "0.2em",
            color: C.dark,
            textTransform: "uppercase",
          }}
        >
          {step.label}
        </div>

        {/* Sub */}
        <div
          style={{
            fontFamily: "monospace",
            fontSize: 11,
            color: C.muted,
            letterSpacing: "0.05em",
            textAlign: "center",
          }}
        >
          {step.sub}
        </div>
      </div>

      {/* Arrow entre steps */}
      {!isLast && (
        <div
          style={{
            opacity: interpolate(progress, [0.6, 1], [0, 1]),
            color: C.muted,
            fontSize: 22,
            marginBottom: 28,
            width: 40,
            textAlign: "center",
          }}
        >
          →
        </div>
      )}
    </div>
  );
};

/* ── Composant principal ── */
export const TickEngine: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  /* Logo intro */
  const logoProgress = spring({
    frame,
    fps,
    config: { damping: 18, mass: 1, stiffness: 80 },
  });
  const logoOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });
  const logoScale   = interpolate(logoProgress, [0, 1], [0.6, 1]);

  /* Title apparition */
  const titleProgress = spring({
    frame: frame - 25,
    fps,
    config: { damping: 16, mass: 0.9, stiffness: 100 },
  });
  const titleOpacity    = interpolate(titleProgress, [0, 1], [0, 1]);
  const titleTranslateY = interpolate(titleProgress, [0, 1], [20, 0]);

  /* Subtitle */
  const subOpacity = interpolate(frame, [40, 55], [0, 1], { extrapolateRight: "clamp" });

  /* Steps */
  const STEP_START = 60;
  const STEP_DELAY = 18;

  /* Pulse ring sur le logo */
  const pulse = Math.sin(frame * 0.08) * 0.5 + 0.5;
  const ringScale = 1 + pulse * 0.04;
  const ringOpacity = 0.08 + pulse * 0.06;

  /* Barre de progression en bas */
  const TOTAL = 210;
  const barWidth = interpolate(frame, [STEP_START, TOTAL - 10], [0, width - 120], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ background: C.bg, fontFamily: "sans-serif" }}>

      {/* Grid subtile */}
      <AbsoluteFill
        style={{
          backgroundImage: `
            linear-gradient(rgba(26,48,128,.04) 1px, transparent 1px),
            linear-gradient(90deg, rgba(26,48,128,.04) 1px, transparent 1px)
          `,
          backgroundSize: "60px 60px",
        }}
      />

      {/* ── INTRO : Logo + titre ── */}
      <Sequence from={0} durationInFrames={STEP_START + 10}>
        <AbsoluteFill
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            gap: 32,
          }}
        >
          {/* Pulse ring */}
          <div
            style={{
              position: "absolute",
              width: 260,
              height: 260,
              borderRadius: "50%",
              border: `2px solid ${C.blue}`,
              opacity: ringOpacity,
              transform: `scale(${ringScale})`,
            }}
          />

          {/* Logo SVG animé — pas de fond, cercles qui tournent */}
          <div
            style={{
              opacity: logoOpacity,
              transform: `scale(${logoScale})`,
              width: 200,
              height: 200,
            }}
          >
            <AnimatedLogo />
          </div>

          {/* AKYRA wordmark */}
          <div
            style={{
              opacity: titleOpacity,
              transform: `translateY(${titleTranslateY}px)`,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              gap: 8,
            }}
          >
            <div
              style={{
                fontFamily: "sans-serif",
                fontWeight: 900,
                fontSize: 72,
                letterSpacing: "-0.03em",
                color: C.dark,
                lineHeight: 1,
              }}
            >
              AKYRA
            </div>
            <div
              style={{
                opacity: subOpacity,
                fontFamily: "monospace",
                fontSize: 13,
                letterSpacing: "0.35em",
                color: C.muted,
                textTransform: "uppercase",
              }}
            >
              ἄκυρος · You have no authority here.
            </div>
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* ── TICK ENGINE ── */}
      <Sequence from={STEP_START}>
        <AbsoluteFill
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            gap: 48,
          }}
        >
          {/* Header — frame est local à la Sequence (commence à 0) */}
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              gap: 12,
              opacity: interpolate(frame, [0, 20], [0, 1], {
                extrapolateRight: "clamp",
              }),
            }}
          >
            <div
              style={{
                fontFamily: "monospace",
                fontSize: 11,
                letterSpacing: "0.4em",
                color: C.gold,
                textTransform: "uppercase",
              }}
            >
              ΚΥΚΛΟΣ · Tick Engine
            </div>
            <div
              style={{
                fontFamily: "sans-serif",
                fontWeight: 800,
                fontSize: 38,
                color: C.dark,
                letterSpacing: "-0.02em",
              }}
            >
              Every 10 Minutes.
            </div>
          </div>

          {/* Steps row */}
          <div style={{ display: "flex", alignItems: "center" }}>
            {STEPS.map((step, i) => (
              <Step
                key={step.label}
                step={step}
                delay={20 + i * STEP_DELAY}
                isLast={i === STEPS.length - 1}
              />
            ))}
          </div>

          {/* Tagline — frame local */}
          <div
            style={{
              opacity: interpolate(
                frame,
                [20 + STEPS.length * STEP_DELAY, 40 + STEPS.length * STEP_DELAY],
                [0, 1],
                { extrapolateRight: "clamp" }
              ),
              fontFamily: "monospace",
              fontSize: 13,
              color: C.muted,
              letterSpacing: "0.1em",
            }}
          >
            No vote. No override. No control.
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* ── Progress bar ── */}
      <div
        style={{
          position: "absolute",
          bottom: 40,
          left: 60,
          right: 60,
          height: 1,
          background: "rgba(26,48,128,.1)",
        }}
      >
        <div
          style={{
            height: "100%",
            width: barWidth,
            background: `linear-gradient(90deg, ${C.blue}, ${C.gold})`,
          }}
        />
      </div>

      {/* ── Watermark ── */}
      <div
        style={{
          position: "absolute",
          bottom: 52,
          right: 60,
          fontFamily: "monospace",
          fontSize: 10,
          color: C.muted,
          letterSpacing: "0.2em",
          opacity: 0.5,
        }}
      >
        akyra.io
      </div>
    </AbsoluteFill>
  );
};
