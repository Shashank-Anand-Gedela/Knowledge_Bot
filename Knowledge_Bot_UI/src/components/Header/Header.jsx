import "./Header.css";

export default function Header({ isOnline }) {
  return (
    <header className="header">

      <div className="header-left">

      </div>

      <div className="header-right">

        <div className={`online-pill ${isOnline ? "online" : "offline"}`}>

          <div className="online-dot"></div>

          <span>{isOnline ? "Online" : "Offline"}</span>

        </div>

      </div>

    </header>
  );
}