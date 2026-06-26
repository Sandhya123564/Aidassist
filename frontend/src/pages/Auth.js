import React, { useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { getTranslation } from '../utils/translations';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { toast } from 'sonner';
import { Stethoscope, Loader2 } from 'lucide-react';

const Auth = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { login, signup, language } = useApp();
  const [mode, setMode] = useState(searchParams.get('mode') === 'login' ? 'login' : 'signup');
  const [loading, setLoading] = useState(false);
  
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    preferred_language: language
  });

  const t = (key) => getTranslation(key, language);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      if (mode === 'login') {
        const result = await login(formData.email, formData.password);
        if (result.success) {
          toast.success(t('success'));
          navigate('/dashboard');
        } else {
          toast.error(result.error || t('error'));
        }
      } else {
        const result = await signup(
          formData.name,
          formData.email,
          formData.password,
          formData.preferred_language
        );
        if (result.success) {
          toast.success(t('success'));
          navigate('/dashboard');
        } else {
          toast.error(result.error || t('error'));
        }
      }
    } catch (error) {
      toast.error(t('error'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-stone-50 flex items-center justify-center px-4 py-12">
      <div data-testid="auth-container" className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 mb-4">
            <Stethoscope className="h-10 w-10 text-primary" />
            <h1 className="text-3xl font-bold font-heading text-gray-900">{t('app_name')}</h1>
          </div>
          <p className="text-gray-600">{t('app_tagline')}</p>
        </div>

        {/* Auth Card */}
        <div className="bg-white border border-stone-100 rounded-2xl shadow-sm p-8">
          <h2 data-testid="auth-title" className="text-2xl font-bold font-heading text-gray-900 mb-6 text-center">
            {mode === 'login' ? t('login_title') : t('signup_title')}
          </h2>

          <form onSubmit={handleSubmit} className="space-y-4">
            {mode === 'signup' && (
              <div>
                <Label htmlFor="name">{t('name')}</Label>
                <Input
                  data-testid="name-input"
                  id="name"
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  required
                  className="h-12 rounded-lg"
                />
              </div>
            )}

            <div>
              <Label htmlFor="email">{t('email')}</Label>
              <Input
                data-testid="email-input"
                id="email"
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                required
                className="h-12 rounded-lg"
              />
            </div>

            <div>
              <Label htmlFor="password">{t('password')}</Label>
              <Input
                data-testid="password-input"
                id="password"
                type="password"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                required
                className="h-12 rounded-lg"
              />
            </div>

            {mode === 'signup' && (
              <div>
                <Label htmlFor="preferred_language">{t('preferred_language')}</Label>
                <Select
                  value={formData.preferred_language}
                  onValueChange={(value) => setFormData({ ...formData, preferred_language: value })}
                >
                  <SelectTrigger data-testid="language-select" id="preferred_language" className="h-12 rounded-lg">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="en">{t('lang_en')}</SelectItem>
                    <SelectItem value="hi">{t('lang_hi')}</SelectItem>
                    <SelectItem value="kn">{t('lang_kn')}</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            )}

            <Button
              data-testid="submit-btn"
              type="submit"
              className="w-full h-12 bg-action hover:bg-action/90 text-white rounded-full font-medium shadow-lg shadow-action/20 transition-transform active:scale-95"
              disabled={loading}
            >
              {loading ? (
                <><Loader2 className="mr-2 h-4 w-4 animate-spin" /> {t('loading')}</>
              ) : (
                mode === 'login' ? t('login_button') : t('signup_button')
              )}
            </Button>
          </form>

          {/* Toggle Mode */}
          <div className="mt-6 text-center">
            <button
              data-testid="toggle-mode-btn"
              onClick={() => setMode(mode === 'login' ? 'signup' : 'login')}
              className="text-action hover:underline"
            >
              {mode === 'login' ? t('no_account') : t('have_account')}
            </button>
          </div>
        </div>

        {/* Back to Home */}
        <div className="text-center mt-6">
          <button
            data-testid="back-to-home-btn"
            onClick={() => navigate('/')}
            className="text-gray-600 hover:text-gray-900 transition-colors"
          >
            ← {t('back')}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Auth;
