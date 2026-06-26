import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { getTranslation } from '../utils/translations';
import { Button } from '../components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { RadioGroup, RadioGroupItem } from '../components/ui/radio-group';
import { Progress } from '../components/ui/progress';
import axios from 'axios';
import { toast } from 'sonner';
import {
  Stethoscope, ArrowLeft, ArrowRight, Mic, MicOff, Loader2,
  CheckCircle, AlertTriangle, Phone, Download
} from 'lucide-react';

const TroubleshootingFlow = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { user, language, API } = useApp();
  
  const [step, setStep] = useState('triage'); // triage, classify, steps, escalation
  const [triageData, setTriageData] = useState({
    main_issue: '',
    side: '',
    device_type: '',
    power_type: '',
    exposed_to_water: false,
    additional_details: ''
  });
  
  const [sessionId, setSessionId] = useState(null);
  const [currentStep, setCurrentStep] = useState(null);
  const [stepProgress, setStepProgress] = useState(0);
  const [isListening, setIsListening] = useState(false);
  const [loading, setLoading] = useState(false);

  const t = (key) => getTranslation(key, language);

  useEffect(() => {
    const sid = searchParams.get('session');
    if (sid) {
      loadSession(sid);
    }
  }, []);

  const loadSession = async (sid) => {
    try {
      const response = await axios.get(`${API}/session/${sid}`);
      setSessionId(sid);
      setTriageData(response.data.triage_data);
      if (response.data.status === 'resolved' || response.data.status === 'escalated') {
        setStep('escalation');
      } else {
        await fetchCurrentStep(sid);
        setStep('steps');
      }
    } catch (error) {
      console.error('Failed to load session', error);
      toast.error(t('error'));
    }
  };

  const handleTriageSubmit = async () => {
    if (!triageData.main_issue || !triageData.side || !triageData.device_type || !triageData.power_type) {
      toast.error('Please fill in all required fields');
      return;
    }

    setLoading(true);
    try {
      // Submit triage
      await axios.post(`${API}/triage/submit`, {
        ...triageData,
        language
      });

      // Classify issue
      const classifyResponse = await axios.post(`${API}/classify`, {
        complaint_text: `${triageData.main_issue}. ${triageData.additional_details}`,
        triage_data: triageData,
        language
      });

      // Create session
      const sessionResponse = await axios.post(`${API}/session/create`, {
        triage_data: triageData,
        classification_result: classifyResponse.data,
        language
      });

      setSessionId(sessionResponse.data.session_id);
      await fetchCurrentStep(sessionResponse.data.session_id);
      setStep('steps');
      toast.success('Analysis complete');
    } catch (error) {
      console.error('Triage error', error);
      toast.error(t('error'));
    } finally {
      setLoading(false);
    }
  };

  const fetchCurrentStep = async (sid) => {
    try {
      const response = await axios.get(`${API}/session/${sid}/current-step`);
      setCurrentStep(response.data);
      setStepProgress(response.data.progress);
    } catch (error) {
      if (error.response?.status === 400) {
        setStep('escalation');
      } else {
        console.error('Failed to fetch step', error);
        toast.error(t('error'));
      }
    }
  };

  const handleStepAction = async (action) => {
    if (!sessionId || !currentStep) return;

    setLoading(true);
    try {
      const response = await axios.post(`${API}/session/${sessionId}/update-step`, {
        step_id: currentStep.current_step.id,
        action: action,
        outcome: action === 'FIXED' ? 'resolved' : 'continued'
      });

      if (action === 'FIXED') {
        toast.success(t('problem_fixed'));
        setStep('escalation');
      } else if (response.data.next_step_available) {
        await fetchCurrentStep(sessionId);
      } else {
        setStep('escalation');
      }
    } catch (error) {
      console.error('Step action error', error);
      toast.error(t('error'));
    } finally {
      setLoading(false);
    }
  };

  const handleGeneratePDF = async () => {
    try {
      const response = await axios.post(
        `${API}/support-summary/generate`,
        { session_id: sessionId, language },
        { responseType: 'blob' }
      );

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `aidassist_summary_${sessionId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      toast.success('PDF downloaded');
    } catch (error) {
      console.error('PDF generation error', error);
      toast.error(t('error'));
    }
  };

  const startVoiceInput = () => {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      toast.error('Speech recognition not supported');
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = language === 'hi' ? 'hi-IN' : language === 'kn' ? 'kn-IN' : 'en-US';
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () => {
      setIsListening(true);
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setTriageData({ ...triageData, additional_details: transcript });
      setIsListening(false);
    };

    recognition.onerror = () => {
      setIsListening(false);
      toast.error('Voice input failed');
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognition.start();
  };

  return (
    <div className="min-h-screen bg-stone-50">
      {/* Header */}
      <header className="bg-white border-b border-stone-200">
        <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-4">
            <Button
              data-testid="back-to-dashboard-btn"
              variant="ghost"
              onClick={() => navigate('/dashboard')}
            >
              <ArrowLeft className="h-5 w-5" />
            </Button>
            <div className="flex items-center gap-2">
              <Stethoscope className="h-8 w-8 text-primary" />
              <h1 className="text-2xl font-bold font-heading text-gray-900">{t('app_name')}</h1>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-md mx-auto px-4 py-8">
        {/* Triage Step */}
        {step === 'triage' && (
          <div data-testid="triage-form" className="animate-in">
            <h2 className="text-3xl font-bold font-heading text-gray-900 mb-8 text-center">
              {t('triage_title')}
            </h2>

            <div className="bg-white border border-stone-100 rounded-2xl p-6 space-y-6">
              <div>
                <Label>{t('main_issue')}</Label>
                <Select
                  value={triageData.main_issue}
                  onValueChange={(value) => setTriageData({ ...triageData, main_issue: value })}
                >
                  <SelectTrigger data-testid="main-issue-select" className="h-12 rounded-lg mt-2">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="No sound">{t('issue_no_sound')}</SelectItem>
                    <SelectItem value="Weak sound">{t('issue_weak_sound')}</SelectItem>
                    <SelectItem value="Whistling">{t('issue_whistling')}</SelectItem>
                    <SelectItem value="Distorted sound">{t('issue_distorted')}</SelectItem>
                    <SelectItem value="Sound cuts in/out">{t('issue_intermittent')}</SelectItem>
                    <SelectItem value="Not charging">{t('issue_not_charging')}</SelectItem>
                    <SelectItem value="Battery drains fast">{t('issue_battery_drain')}</SelectItem>
                    <SelectItem value="Bluetooth issue">{t('issue_bluetooth')}</SelectItem>
                    <SelectItem value="Discomfort">{t('issue_discomfort')}</SelectItem>
                    <SelectItem value="Too much background noise">{t('issue_background_noise')}</SelectItem>
                    <SelectItem value="Hear but don't understand">{t('issue_hear_not_understand')}</SelectItem>
                    <SelectItem value="Other">{t('issue_other')}</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label>{t('which_side')}</Label>
                <RadioGroup
                  value={triageData.side}
                  onValueChange={(value) => setTriageData({ ...triageData, side: value })}
                  className="flex gap-4 mt-2"
                >
                  <div className="flex items-center gap-2">
                    <RadioGroupItem data-testid="side-left" value="LEFT" id="left" />
                    <Label htmlFor="left">{t('side_left')}</Label>
                  </div>
                  <div className="flex items-center gap-2">
                    <RadioGroupItem data-testid="side-right" value="RIGHT" id="right" />
                    <Label htmlFor="right">{t('side_right')}</Label>
                  </div>
                  <div className="flex items-center gap-2">
                    <RadioGroupItem data-testid="side-both" value="BOTH" id="both" />
                    <Label htmlFor="both">{t('side_both')}</Label>
                  </div>
                </RadioGroup>
              </div>

              <div>
                <Label>{t('device_type')}</Label>
                <Select
                  value={triageData.device_type}
                  onValueChange={(value) => setTriageData({ ...triageData, device_type: value })}
                >
                  <SelectTrigger data-testid="device-type-select" className="h-12 rounded-lg mt-2">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="RIC">{t('device_ric')}</SelectItem>
                    <SelectItem value="BTE">{t('device_bte')}</SelectItem>
                    <SelectItem value="ITE">{t('device_ite')}</SelectItem>
                    <SelectItem value="NOT_SURE">{t('device_not_sure')}</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label>{t('power_type')}</Label>
                <Select
                  value={triageData.power_type}
                  onValueChange={(value) => setTriageData({ ...triageData, power_type: value })}
                >
                  <SelectTrigger data-testid="power-type-select" className="h-12 rounded-lg mt-2">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="BATTERY">{t('power_battery')}</SelectItem>
                    <SelectItem value="RECHARGEABLE">{t('power_rechargeable')}</SelectItem>
                    <SelectItem value="NOT_SURE">{t('power_not_sure')}</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label>{t('exposed_question')}</Label>
                <RadioGroup
                  value={triageData.exposed_to_water ? 'yes' : 'no'}
                  onValueChange={(value) => setTriageData({ ...triageData, exposed_to_water: value === 'yes' })}
                  className="flex gap-4 mt-2"
                >
                  <div className="flex items-center gap-2">
                    <RadioGroupItem data-testid="exposed-yes" value="yes" id="yes" />
                    <Label htmlFor="yes">Yes</Label>
                  </div>
                  <div className="flex items-center gap-2">
                    <RadioGroupItem data-testid="exposed-no" value="no" id="no" />
                    <Label htmlFor="no">No</Label>
                  </div>
                </RadioGroup>
              </div>

              <div>
                <div className="flex justify-between items-center mb-2">
                  <Label>{t('additional_details')}</Label>
                  <Button
                    data-testid="voice-input-btn"
                    variant="outline"
                    size="sm"
                    onClick={startVoiceInput}
                    disabled={isListening}
                  >
                    {isListening ? (
                      <><Mic className="h-4 w-4 mr-2 text-red-500 animate-pulse" /> Listening...</>
                    ) : (
                      <><MicOff className="h-4 w-4 mr-2" /> {t('voice_input')}</>
                    )}
                  </Button>
                </div>
                <Textarea
                  data-testid="additional-details-input"
                  value={triageData.additional_details}
                  onChange={(e) => setTriageData({ ...triageData, additional_details: e.target.value })}
                  className="min-h-24 rounded-lg"
                  placeholder="Describe your issue in more detail..."
                />
              </div>

              <Button
                data-testid="submit-triage-btn"
                onClick={handleTriageSubmit}
                disabled={loading}
                className="w-full h-12 bg-action hover:bg-action/90 text-white rounded-full font-medium shadow-lg shadow-action/20 transition-transform active:scale-95"
              >
                {loading ? (
                  <><Loader2 className="mr-2 h-4 w-4 animate-spin" /> {t('loading')}</>
                ) : (
                  <>{t('continue')} <ArrowRight className="ml-2 h-5 w-5" /></>
                )}
              </Button>
            </div>
          </div>
        )}

        {/* Steps */}
        {step === 'steps' && currentStep && (
          <div data-testid="troubleshooting-step" className="animate-in">
            <div className="mb-8">
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm text-gray-600">
                  {t('step_of').replace('{{current}}', currentStep.current_step_number).replace('{{total}}', currentStep.total_steps)}
                </span>
                <span className="text-sm font-medium text-primary">
                  {Math.round(stepProgress)}% {t('progress')}
                </span>
              </div>
              <Progress value={stepProgress} className="h-2" />
            </div>

            <div className="bg-white border border-stone-100 rounded-2xl p-6">
              <h2 className="text-2xl font-bold font-heading text-gray-900 mb-4">
                {currentStep.current_step.title[language] || currentStep.current_step.title.en}
              </h2>

              <div className="bg-stone-50 border border-stone-200 rounded-xl p-4 mb-6">
                <p className="text-gray-800 leading-relaxed whitespace-pre-line">
                  {currentStep.current_step.instructions[language] || currentStep.current_step.instructions.en}
                </p>
              </div>

              {currentStep.current_step.safety_notes && (
                <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 mb-6 flex gap-3">
                  <AlertTriangle className="h-5 w-5 text-amber-600 flex-shrink-0 mt-0.5" />
                  <p className="text-amber-900 text-sm">
                    {currentStep.current_step.safety_notes[language] || currentStep.current_step.safety_notes.en}
                  </p>
                </div>
              )}

              <div className="flex gap-4">
                <Button
                  data-testid="problem-fixed-btn"
                  onClick={() => handleStepAction('FIXED')}
                  disabled={loading}
                  className="flex-1 h-12 bg-green-600 hover:bg-green-700 text-white rounded-full font-medium transition-transform active:scale-95 flex items-center justify-center gap-2"
                >
                  {loading ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <><CheckCircle className="h-5 w-5" /> {t('problem_fixed')}</>
                  )}
                </Button>
                <Button
                  data-testid="next-step-btn"
                  onClick={() => handleStepAction('CONTINUE')}
                  disabled={loading}
                  className="flex-1 h-12 bg-action hover:bg-action/90 text-white rounded-full font-medium transition-transform active:scale-95 flex items-center justify-center gap-2"
                >
                  {loading ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <>{t('next_step')} <ArrowRight className="h-5 w-5" /></>
                  )}
                </Button>
              </div>
            </div>
          </div>
        )}

        {/* Escalation */}
        {step === 'escalation' && (
          <div data-testid="escalation-screen" className="animate-in">
            <div className="text-center mb-8">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-amber-100 rounded-full mb-4">
                <Phone className="h-8 w-8 text-amber-600" />
              </div>
              <h2 className="text-3xl font-bold font-heading text-gray-900 mb-4">
                {t('escalation_title')}
              </h2>
              <p className="text-lg text-gray-700 leading-relaxed">
                {t('escalation_message')}
              </p>
            </div>

            <div className="bg-white border border-stone-100 rounded-2xl p-6 space-y-4">
              <Button
                data-testid="download-pdf-btn"
                onClick={handleGeneratePDF}
                className="w-full h-12 bg-action hover:bg-action/90 text-white rounded-full font-medium shadow-lg shadow-action/20 transition-transform active:scale-95 flex items-center justify-center gap-2"
              >
                <Download className="h-5 w-5" />
                {t('download_pdf')}
              </Button>

              <Button
                data-testid="return-dashboard-btn"
                onClick={() => navigate('/dashboard')}
                variant="outline"
                className="w-full h-12 border-2 rounded-full font-medium"
              >
                Return to Dashboard
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default TroubleshootingFlow;
