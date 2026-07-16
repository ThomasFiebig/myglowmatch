import Image from "next/image";
import Link from "next/link";

export default function Home() {
  return (
    <main className="relative flex min-h-screen flex-1 items-center justify-center px-6 py-16">
      <div className="relative mx-auto flex max-w-xl flex-col items-center text-center">
        {/* Sanft schwebende Farbwolken für dezente Tiefe */}
        <span
          aria-hidden="true"
          className="pointer-events-none absolute -top-40 left-1/2 h-72 w-72 -translate-x-1/2 rounded-full bg-rosegold/25 blur-3xl"
        />
        <span
          aria-hidden="true"
          className="pointer-events-none absolute -bottom-32 right-0 h-56 w-56 rounded-full bg-blush/60 blur-3xl"
        />

        <div className="relative animate-[fadeInUp_1.2s_ease-out_both]">
          <Image
            src="/logo.svg"
            alt="myglowmatch"
            width={260}
            height={52}
            priority
            className="mx-auto h-auto w-56 sm:w-64"
          />

          <span
            aria-hidden="true"
            className="mx-auto mt-10 block h-px w-16 bg-rosegold-dark/60"
          />

          <h1 className="mt-10 font-serif text-4xl leading-tight text-ink sm:text-5xl md:text-6xl">
            Bald wieder da.
          </h1>

          <p className="mt-6 text-lg text-ink-soft">
            Wir bauen an etwas Neuem.
          </p>

          <span
            aria-hidden="true"
            className="mx-auto mt-12 block h-px w-16 bg-rosegold-dark/60"
          />
        </div>
      </div>

      <Link
        href="/impressum"
        className="absolute bottom-6 left-1/2 -translate-x-1/2 text-xs text-ink-soft/70 underline underline-offset-4 transition-colors hover:text-ink"
      >
        Impressum
      </Link>

      <style>{`
        @keyframes fadeInUp {
          from { opacity: 0; transform: translateY(16px); }
          to   { opacity: 1; transform: translateY(0); }
        }
      `}</style>
    </main>
  );
}
