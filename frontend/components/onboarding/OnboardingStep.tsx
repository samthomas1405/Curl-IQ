'use client';

import { ReactNode } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader } from '@/components/ui/card';

interface OnboardingStepProps {
  children: ReactNode;
  currentStep: number;
  totalSteps: number;
  onNext: () => void;
  onBack: () => void;
  onSkip: () => void;
  onSubmit: () => void;
  canProceed: boolean;
  isLastStep: boolean;
  submitting: boolean;
  error: string | null;
}

export default function OnboardingStep({
  children,
  currentStep,
  onNext,
  onBack,
  onSkip,
  onSubmit,
  canProceed,
  isLastStep,
  submitting,
  error,
}: OnboardingStepProps) {
  return (
    <Card>
      <CardHeader>
        {error && (
          <div className="mb-4 rounded-md bg-red-50 p-3 text-sm text-red-800">
            {error}
          </div>
        )}
      </CardHeader>
      <CardContent>
        {children}
        
        <div className="mt-8 flex justify-between">
          <div>
            {currentStep > 0 && (
              <Button
                type="button"
                variant="outline"
                onClick={onBack}
                disabled={submitting}
              >
                Back
              </Button>
            )}
          </div>
          
          <div className="flex gap-2">
            {!isLastStep && (
              <>
                {/* Show Skip button for optional steps (step 2+) */}
                {currentStep >= 2 && (
                  <Button
                    type="button"
                    variant="ghost"
                    onClick={onSkip}
                    disabled={submitting}
                  >
                    Skip
                  </Button>
                )}
                <Button
                  type="button"
                  onClick={onNext}
                  disabled={!canProceed || submitting}
                >
                  Next
                </Button>
              </>
            )}
            {isLastStep && (
              <Button
                type="button"
                onClick={onSubmit}
                disabled={!canProceed || submitting}
              >
                {submitting ? 'Saving...' : 'Complete Setup'}
              </Button>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
