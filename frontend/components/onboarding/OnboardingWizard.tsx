'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { userApi } from '@/lib/api';
import OnboardingStep from './OnboardingStep';
import CurlPatternStep from './steps/CurlPatternStep';
import PorosityStep from './steps/PorosityStep';
import DensityStep from './steps/DensityStep';
import ThicknessStep from './steps/ThicknessStep';
import ScalpTypeStep from './steps/ScalpTypeStep';
import LocationStep from './steps/LocationStep';

interface OnboardingData {
  curl_pattern?: string;
  porosity?: string;
  density?: string;
  thickness?: string;
  scalp_type?: string;
  location?: string;
}

const TOTAL_STEPS = 6;

export default function OnboardingWizard() {
  const router = useRouter();
  const [currentStep, setCurrentStep] = useState(0);
  const [formData, setFormData] = useState<OnboardingData>({});
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const updateFormData = (field: keyof OnboardingData, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    setError(null);
  };

  const handleNext = () => {
    // Validate required fields on step 0 and 1
    if (currentStep === 0 && !formData.curl_pattern) {
      setError('Please select your curl pattern');
      return;
    }
    if (currentStep === 1 && !formData.porosity) {
      setError('Please select your hair porosity');
      return;
    }

    if (currentStep < TOTAL_STEPS - 1) {
      setCurrentStep((prev) => prev + 1);
      setError(null);
    }
  };

  const handleBack = () => {
    if (currentStep > 0) {
      setCurrentStep((prev) => prev - 1);
      setError(null);
    }
  };

  const handleSkip = () => {
    if (currentStep < TOTAL_STEPS - 1) {
      setCurrentStep((prev) => prev + 1);
      setError(null);
    }
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    setError(null);

    try {
      // Validate required fields
      if (!formData.curl_pattern || !formData.porosity) {
        setError('Please complete all required fields');
        setSubmitting(false);
        return;
      }

      // Submit profile data
      await userApi.updateProfile(formData);
      
      // Redirect to dashboard
      router.push('/dashboard');
    } catch (err: any) {
      console.error('Failed to save profile:', err);
      setError(
        err.response?.data?.detail || 
        err.message || 
        'Failed to save profile. Please try again.'
      );
      setSubmitting(false);
    }
  };

  const canProceed = () => {
    if (currentStep === 0) return !!formData.curl_pattern;
    if (currentStep === 1) return !!formData.porosity;
    return true; // Optional steps can always proceed
  };

  const isLastStep = currentStep === TOTAL_STEPS - 1;

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-2xl">
        {/* Welcome Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold mb-2">Welcome to CurlLabs!</h1>
          <p className="text-gray-600">
            Let's set up your hair profile to get personalized recommendations
          </p>
        </div>

        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700">
              Step {currentStep + 1} of {TOTAL_STEPS}
            </span>
            <span className="text-sm text-gray-500">
              {Math.round(((currentStep + 1) / TOTAL_STEPS) * 100)}% Complete
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${((currentStep + 1) / TOTAL_STEPS) * 100}%` }}
            />
          </div>
        </div>

        {/* Step Content */}
        <OnboardingStep
          currentStep={currentStep}
          totalSteps={TOTAL_STEPS}
          onNext={handleNext}
          onBack={handleBack}
          onSkip={handleSkip}
          onSubmit={handleSubmit}
          canProceed={canProceed()}
          isLastStep={isLastStep}
          submitting={submitting}
          error={error}
        >
          {currentStep === 0 && (
            <CurlPatternStep
              value={formData.curl_pattern}
              onChange={(value) => updateFormData('curl_pattern', value)}
            />
          )}
          {currentStep === 1 && (
            <PorosityStep
              value={formData.porosity}
              onChange={(value) => updateFormData('porosity', value)}
            />
          )}
          {currentStep === 2 && (
            <DensityStep
              value={formData.density}
              onChange={(value) => updateFormData('density', value)}
            />
          )}
          {currentStep === 3 && (
            <ThicknessStep
              value={formData.thickness}
              onChange={(value) => updateFormData('thickness', value)}
            />
          )}
          {currentStep === 4 && (
            <ScalpTypeStep
              value={formData.scalp_type}
              onChange={(value) => updateFormData('scalp_type', value)}
            />
          )}
          {currentStep === 5 && (
            <LocationStep
              value={formData.location}
              onChange={(value) => updateFormData('location', value)}
            />
          )}
        </OnboardingStep>
      </div>
    </div>
  );
}
