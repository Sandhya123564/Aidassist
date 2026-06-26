import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { getTranslation } from '../utils/translations';
import { Button } from '../components/ui/button';
import axios from 'axios';
import { toast } from 'sonner';
import { Stethoscope, LogOut, PlayCircle, History, TrendingUp, CheckCircle } from 'lucide-react';

const Dashboard = () => {
  const navigate = useNavigate();
  const { user, logout, language, API } = useApp();
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);

  const t = (key) => getTranslation(key, language);

  useEffect(() => {
    fetchSessions();
  }, []);

  const fetchSessions = async () => {
    try {
      const response = await axios.get(`${API}/session/history`);
      setSessions(response.data.sessions);
    } catch (error) {
      console.error('Failed to fetch sessions', error);
      toast.error(t('error'));
    } finally {
      setLoading(false);
    }
  };

  const stats = {
    total: sessions.length,
    resolved: sessions.filter(s => s.status === 'resolved').length,
    successRate: sessions.length > 0
      ? Math.round((sessions.filter(s => s.status === 'resolved').length / sessions.length) * 100)
      : 0
  };

  return (
    <div className="min-h-screen bg-stone-50">
      <header className="bg-white border-b border-stone-200">
        <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <Stethoscope className="h-8 w-8 text-primary" />
            <h1 className="text-2xl font-bold font-heading text-gray-900">{t('app_name')}</h1>
          </div>
          
          <div className="flex items-center gap-4">
            <span className="text-gray-700">{user?.name}</span>
            <Button
              data-testid="logout-btn"
              variant="outline"
              onClick={logout}
              className="flex items-center gap-2"
            >
              <LogOut className="h-4 w-4" />
              Logout
            </Button>
          </div>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-4 py-12">
        <div className="mb-12">
          <h2 data-testid="dashboard-welcome" className="text-4xl font-bold font-heading text-gray-900 mb-4">
            {t('dashboard_title')}
          </h2>
          <Button
            data-testid="start-troubleshooting-btn"
            size="lg"
            onClick={() => navigate('/troubleshoot')}
            className="bg-action hover:bg-action/90 text-white px-8 py-3 rounded-full font-medium shadow-lg shadow-action/20 transition-transform active:scale-95 flex items-center gap-2"
          >
            <PlayCircle className="h-5 w-5" />
            {t('start_new_session')}
          </Button>
        </div>

        <div className="mb-12">
          <h3 className="text-2xl font-semibold font-heading text-gray-900 mb-6">
            {t('dashboard_stats')}
          </h3>
          <div data-testid="dashboard-stats" className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white border border-stone-100 rounded-2xl p-6">
              <div className="flex items-center gap-3 mb-2">
                <History className="h-6 w-6 text-primary" />
                <h4 className="text-lg font-semibold text-gray-700">{t('total_sessions')}</h4>
              </div>
              <p className="text-3xl font-bold text-gray-900">{stats.total}</p>
            </div>

            <div className="bg-white border border-stone-100 rounded-2xl p-6">
              <div className="flex items-center gap-3 mb-2">
                <CheckCircle className="h-6 w-6 text-green-600" />
                <h4 className="text-lg font-semibold text-gray-700">{t('resolved_sessions')}</h4>
              </div>
              <p className="text-3xl font-bold text-gray-900">{stats.resolved}</p>
            </div>

            <div className="bg-white border border-stone-100 rounded-2xl p-6">
              <div className="flex items-center gap-3 mb-2">
                <TrendingUp className="h-6 w-6 text-action" />
                <h4 className="text-lg font-semibold text-gray-700">{t('success_rate')}</h4>
              </div>
              <p className="text-3xl font-bold text-gray-900">{stats.successRate}%</p>
            </div>
          </div>
        </div>

        <div>
          <h3 className="text-2xl font-semibold font-heading text-gray-900 mb-6">
            {t('session_history')}
          </h3>
          {loading ? (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
              <p className="text-gray-600">{t('loading')}</p>
            </div>
          ) : sessions.length === 0 ? (
            <div data-testid="no-sessions-message" className="bg-white border border-stone-100 rounded-2xl p-12 text-center">
              <History className="h-16 w-16 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-600 mb-6">No troubleshooting sessions yet</p>
              <Button
                onClick={() => navigate('/troubleshoot')}
                className="bg-action hover:bg-action/90 text-white"
              >
                {t('start_new_session')}
              </Button>
            </div>
          ) : (
            <div data-testid="session-list" className="space-y-4">
              {sessions.map((session) => (
                <div
                  key={session.id}
                  data-testid={`session-item-${session.id}`}
                  className="bg-white border border-stone-100 rounded-2xl p-6 hover:shadow-md transition-shadow"
                >
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <h4 className="text-lg font-semibold text-gray-900 mb-1">
                        {session.classification_result?.issue_category?.replace('_', ' ') || 'Unknown Issue'}
                      </h4>
                      <p className="text-sm text-gray-600">
                        {new Date(session.created_at).toLocaleDateString()} {new Date(session.created_at).toLocaleTimeString()}
                      </p>
                    </div>
                    <span
                      className={`px-3 py-1 rounded-full text-sm font-medium ${
                        session.status === 'resolved'
                          ? 'bg-green-100 text-green-700'
                          : session.status === 'escalated'
                          ? 'bg-amber-100 text-amber-700'
                          : 'bg-blue-100 text-blue-700'
                      }`}
                    >
                      {session.status}
                    </span>
                  </div>
                  <p className="text-gray-700 mb-4">
                    {session.steps_attempted?.length || 0} steps attempted
                  </p>
                  <Button
                    data-testid={`view-session-${session.id}-btn`}
                    variant="outline"
                    size="sm"
                    onClick={() => navigate(`/troubleshoot?session=${session.id}`)}
                  >
                    {t('view_details')}
                  </Button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
