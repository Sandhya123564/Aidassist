import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { getTranslation } from '../utils/translations';
import { Stethoscope, Languages, FileText, Menu } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Switch } from '../components/ui/switch';
import { Label } from '../components/ui/label';

const Landing = () => {
  const navigate = useNavigate();
  const { language, setLanguage, highContrast, setHighContrast, largeText, setLargeText } = useApp();
  const [showAccessibility, setShowAccessibility] = React.useState(false);

  const t = (key) => getTranslation(key, language);

  return (
    <div className="min-h-screen bg-stone-50">
      {/* Header */}
      <header className="bg-white border-b border-stone-200">
        <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <Stethoscope className="h-8 w-8 text-primary" />
            <h1 className="text-2xl font-bold font-heading text-gray-900">{t('app_name')}</h1>
          </div>
          
          <div className="flex items-center gap-4">
            {/* Language Selector */}
            <Select value={language} onValueChange={setLanguage}>
              <SelectTrigger data-testid="language-selector" className="w-32">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="en">{t('lang_en')}</SelectItem>
                <SelectItem value="hi">{t('lang_hi')}</SelectItem>
                <SelectItem value="kn">{t('lang_kn')}</SelectItem>
              </SelectContent>
            </Select>

            {/* Accessibility Toggle */}
            <button
              data-testid="accessibility-toggle-btn"
              onClick={() => setShowAccessibility(!showAccessibility)}
              className="p-2 hover:bg-stone-100 rounded-lg transition-colors"
            >
              <Menu className="h-5 w-5" />
            </button>
          </div>
        </div>

        {/* Accessibility Panel */}
        {showAccessibility && (
          <div data-testid="accessibility-panel" className="border-t border-stone-200 bg-white animate-in">
            <div className="max-w-6xl mx-auto px-4 py-4 flex gap-6">
              <div className="flex items-center gap-2">
                <Switch
                  data-testid="high-contrast-switch"
                  checked={highContrast}
                  onCheckedChange={setHighContrast}
                  id="high-contrast"
                />
                <Label htmlFor="high-contrast">{t('high_contrast')}</Label>
              </div>
              <div className="flex items-center gap-2">
                <Switch
                  data-testid="large-text-switch"
                  checked={largeText}
                  onCheckedChange={setLargeText}
                  id="large-text"
                />
                <Label htmlFor="large-text">{t('large_text')}</Label>
              </div>
            </div>
          </div>
        )}
      </header>

      {/* Hero Section */}
      <section className="py-20 md:py-32">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-4xl md:text-5xl font-bold font-heading text-gray-900 mb-6">
            {t('hero_title')}
          </h2>
          <p className="text-lg md:text-xl text-gray-700 mb-10 leading-relaxed">
            {t('hero_subtitle')}
          </p>
          <div className="flex gap-4 justify-center flex-wrap">
            <Button
              data-testid="get-started-btn"
              size="lg"
              className="bg-action hover:bg-action/90 text-white px-8 py-3 rounded-full text-lg font-medium shadow-lg shadow-action/20 transition-transform active:scale-95"
              onClick={() => navigate('/auth')}
            >
              {t('get_started')}
            </Button>
            <Button
              data-testid="login-btn"
              size="lg"
              variant="outline"
              className="border-2 border-stone-200 hover:border-action hover:text-action px-8 py-3 rounded-full text-lg font-medium transition-colors"
              onClick={() => navigate('/auth?mode=login')}
            >
              {t('login')}
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-6xl mx-auto px-4">
          <h3 className="text-3xl font-bold font-heading text-center text-gray-900 mb-12">
            {t('features_title')}
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div data-testid="feature-safe-guidance" className="bg-stone-50 border border-stone-100 rounded-2xl p-6 hover:shadow-md transition-shadow">
              <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mb-4">
                <Stethoscope className="h-6 w-6 text-primary" />
              </div>
              <h4 className="text-xl font-semibold font-heading text-gray-900 mb-3">
                {t('feature1_title')}
              </h4>
              <p className="text-gray-700 leading-relaxed">
                {t('feature1_desc')}
              </p>
            </div>

            {/* Feature 2 */}
            <div data-testid="feature-multilingual" className="bg-stone-50 border border-stone-100 rounded-2xl p-6 hover:shadow-md transition-shadow">
              <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mb-4">
                <Languages className="h-6 w-6 text-primary" />
              </div>
              <h4 className="text-xl font-semibold font-heading text-gray-900 mb-3">
                {t('feature2_title')}
              </h4>
              <p className="text-gray-700 leading-relaxed">
                {t('feature2_desc')}
              </p>
            </div>

            {/* Feature 3 */}
            <div data-testid="feature-expert-support" className="bg-stone-50 border border-stone-100 rounded-2xl p-6 hover:shadow-md transition-shadow">
              <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mb-4">
                <FileText className="h-6 w-6 text-primary" />
              </div>
              <h4 className="text-xl font-semibold font-heading text-gray-900 mb-3">
                {t('feature3_title')}
              </h4>
              <p className="text-gray-700 leading-relaxed">
                {t('feature3_desc')}
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Safety Notice */}
      <section className="py-16 bg-amber-50 border-t border-amber-100">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h4 className="text-2xl font-bold font-heading text-gray-900 mb-4">
            {t('safety_warning')}
          </h4>
          <p className="text-lg text-gray-700 leading-relaxed">
            {t('safety_message')}
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-white border-t border-stone-200 py-8">
        <div className="max-w-6xl mx-auto px-4 text-center text-gray-600">
          <p>© 2026 {t('app_name')}. {t('app_tagline')}</p>
        </div>
      </footer>
    </div>
  );
};

export default Landing;
