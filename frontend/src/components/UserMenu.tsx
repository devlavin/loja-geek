import { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export function UserMenu() {
  const { user, logout } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    }

    function handleEscape(e: KeyboardEvent) {
      if (e.key === "Escape") setIsOpen(false);
    }

    document.addEventListener("mousedown", handleClickOutside);
    document.addEventListener("keydown", handleEscape);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
      document.removeEventListener("keydown", handleEscape);
    };
  }, []);

  if (!user) return null;

  function handleLogout() {
    setIsOpen(false);
    logout();
    navigate("/");
  }

  const firstName = user.name.split(" ")[0];

  return (
    <div className="user-menu" ref={menuRef}>
      <button
        className="user-menu-trigger"
        onClick={() => setIsOpen((v) => !v)}
      >
        {firstName}

        <svg
          viewBox="0 0 12 8"
          width="10"
          height="7"
          className={`chevron ${isOpen ? "open" : ""}`}
        >
          <path
            d="M1 1l5 5 5-5"
            stroke="currentColor"
            strokeWidth="1.5"
            fill="none"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </button>

      {isOpen && (
        <div className="user-menu-dropdown">
          {user.role !== "admin" && (
            <Link to="/pedidos" onClick={() => setIsOpen(false)}>
              Meus pedidos
            </Link>
          )}

          <Link to="/perfil" onClick={() => setIsOpen(false)}>
            Meus dados
          </Link>

          <div className="user-menu-divider" />

          <button onClick={handleLogout}>Sair</button>
        </div>
      )}
    </div>
  );
}