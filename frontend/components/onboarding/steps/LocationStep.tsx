'use client';

import { Label } from '@/components/ui/label';
import { LocationInput } from '@/components/LocationInput';

interface LocationStepProps {
  value?: string;
  onChange: (value: string) => void;
}

export default function LocationStep({ value, onChange }: LocationStepProps) {
  return (
    <div>
      <h2 className="text-2xl font-bold mb-2">Where are you located?</h2>
      <p className="text-gray-600 mb-6">
        We'll use your location to track weather conditions (humidity, temperature) that affect your hair. 
        This helps us provide better insights. This is optional.
      </p>
      
      <div className="space-y-4">
        <div>
          <Label htmlFor="location">City, State/Province, Country</Label>
          <div className="mt-2">
            <LocationInput
              id="location"
              value={value}
              onChange={onChange}
              placeholder="Start typing your city..."
            />
          </div>
          <p className="mt-2 text-sm text-gray-500">
            Start typing to see location suggestions
          </p>
        </div>
      </div>
      
      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <p className="text-sm text-gray-600">
          <strong>Why we ask:</strong> Weather conditions like humidity and temperature can significantly 
          affect how your hair responds to products and routines. We'll track this automatically to help 
          you understand what works best in different conditions.
        </p>
      </div>
    </div>
  );
}
