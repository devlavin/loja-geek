import { useState } from "react";
import type { FormEvent } from "react";
import { useNavigate, useLocation, Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { getApiErrorMessage } from "../api/error";

export function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError("");

    try {
      await login({ email, password });
      const redirectTo =
        (location.state as { from?: Location })?.from?.pathname ?? "/";
      navigate(redirectTo, { replace: true });
    } catch (err) {
      setError(getApiErrorMessage(err, "E-mail ou senha inválidos."));
    }
  }

  return (
    <div className="auth-page">
      <form onSubmit={handleSubmit} className="auth-form">
        <h1>Entrar</h1>

        <label>
          E-mail
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </label>

        <label>
          Senha
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>

        {error && <p className="auth-error">{error}</p>}

        <button type="submit" className="btn-primary">
          Entrar
        </button>
        <p className="auth-switch">
          Ainda não tem conta? <Link to="/register">Criar conta</Link>
        </p>
      </form>
    </div>
  );
}
