// =====================================================================
// Logo – die myglowmatch-Wortmarke als Inline-SVG.
//
// Anders als die Datei public/logo.svg (die als <img> meist auf
// Georgia zurückfällt, weil Browser externe Font-Requests blockieren),
// rendert diese Komponente das <text> direkt im Seiten-Kontext und
// nutzt deshalb die bereits geladene Fraunces.
// =====================================================================

type LogoProps = {
  /** Breite in Pixel. Höhe ergibt sich aus dem 5:1-Verhältnis. */
  width?: number;
  className?: string;
};

export default function Logo({ width = 200, className = "" }: LogoProps) {
  // viewBox 600 x 120 -> Seitenverhältnis 5:1
  const height = (width * 120) / 600;

  return (
    <svg
      viewBox="0 0 600 120"
      width={width}
      height={height}
      role="img"
      aria-label="myglowmatch"
      className={className}
    >
      <text
        x="50%"
        y="50%"
        textAnchor="middle"
        dominantBaseline="middle"
        className="font-serif"
        fontWeight={400}
        fontSize={80}
        fill="#5A4A3F"
      >
        myglowmatch
      </text>
    </svg>
  );
}
