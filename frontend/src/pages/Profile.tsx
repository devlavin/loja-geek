// src/pages/Profile.tsx
import { useState } from 'react';
import type { FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { updateUser, deleteUser } from '../api/users';
import { getApiErrorMessage } from '../api/error'

type Feedback = { type: 'error' | 'success'; text: string } | null;

export function Profile() {
  const { user, setUser, logout } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState(user?.email ?? '');
  const [emailMessage, setEmailMessage] = useState<Feedback>(null);
  const [isSavingEmail, setIsSavingEmail] = useState(false);

  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [passwordMessage, setPasswordMessage] = useState<Feedback>(null);
  const [isSavingPassword, setIsSavingPassword] = useState(false);

  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  if (!user) return null;

  const userId = user.id;

  async function handleSaveEmail(e: FormEvent) {
    e.preventDefault();
    setEmailMessage(null);
    setIsSavingEmail(true);

    try {
      const updated = await updateUser(userId, { email });
      setUser(updated);
      setEmailMessage({ type: 'success', text: 'E-mail atualizado.' });
    } catch (err) {
      setEmailMessage({ type: 'error', text: getApiErrorMessage(err, 'Não foi possível atualizar o e-mail.') });
    } finally {
      setIsSavingEmail(false);
    }
  }

  async function handleSavePassword(e: FormEvent) {
    e.preventDefault();
    setPasswordMessage(null);

    if (newPassword !== confirmPassword) {
      setPasswordMessage({ type: 'error', text: 'As senhas não coincidem.' });
      return;
    }

    setIsSavingPassword(true);

    try {
      await updateUser(userId, { password: newPassword });
      setNewPassword('');
      setConfirmPassword('');
      setPasswordMessage({ type: 'success', text: 'Senha atualizada.' });
    } catch (err) {
      setPasswordMessage({ type: 'error', text: getApiErrorMessage(err, 'Não foi possível atualizar a senha.') });
    } finally {
      setIsSavingPassword(false);
    }
  }

  async function handleDeleteAccount() {
    setIsDeleting(true);
    try {
      await deleteUser(userId);
      logout();
      navigate('/');
    } catch {
      setIsDeleting(false);
    }
  }

  return (
    <div className="profile-page">
      <h1>Meus dados</h1>

      <div className="profile-field-static">
        <label>Nome</label>
        <p>{user.name}</p>
      </div>

      <form onSubmit={handleSaveEmail} className="profile-form">
        <label>E-mail</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        {emailMessage && (
          <p className={emailMessage.type === 'error' ? 'auth-error' : 'success-note'}>
            {emailMessage.text}
          </p>
        )}
        <button className="btn-primary" type="submit" disabled={isSavingEmail}>
          {isSavingEmail ? 'Salvando...' : 'Salvar e-mail'}
        </button>
      </form>

      <form onSubmit={handleSavePassword} className="profile-form">
        <label>Nova senha</label>
        <input
          type="password"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
          minLength={8}
          required
        />
        <label>Confirmar nova senha</label>
        <input
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          minLength={8}
          required
        />
        <p className="field-hint">Mínimo 8 caracteres, com maiúscula, número e caractere especial.</p>
        {passwordMessage && (
          <p className={passwordMessage.type === 'error' ? 'auth-error' : 'success-note'}>
            {passwordMessage.text}
          </p>
        )}
        <button className="btn-primary" type="submit" disabled={isSavingPassword}>
          {isSavingPassword ? 'Salvando...' : 'Alterar senha'}
        </button>
      </form>

      <div className="profile-danger">
        <h2>Excluir conta</h2>
        <p>Essa ação não pode ser desfeita.</p>

        {!showDeleteConfirm ? (
          <button className="btn-link danger" onClick={() => setShowDeleteConfirm(true)}>
            Excluir minha conta
          </button>
        ) : (
          <div className="delete-confirm">
            <p>Tem certeza? Isso vai apagar sua conta permanentemente.</p>
            <button className="btn-danger" onClick={handleDeleteAccount} disabled={isDeleting}>
              {isDeleting ? 'Excluindo...' : 'Sim, excluir'}
            </button>
            <button className="btn-link" onClick={() => setShowDeleteConfirm(false)}>
              Cancelar
            </button>
          </div>
        )}
      </div>
    </div>
  );
}