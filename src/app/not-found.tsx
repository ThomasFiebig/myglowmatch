import Home from "./page";

// Alle alten Deep-Links (/demo, /analyse, /desiree, /konzept/...)
// landen auf der Coming-Soon-Seite statt auf einer 404-Meldung.
export default function NotFound() {
  return <Home />;
}
