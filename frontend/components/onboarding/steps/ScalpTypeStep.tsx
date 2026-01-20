'use client';

interface ScalpTypeStepProps {
  value?: string;
  onChange: (value: string) => void;
}

const SCALP_OPTIONS = [
  {
    value: 'dry',
    label: 'Dry Scalp',
    description: 'Your scalp feels tight, may have flakes, and doesn\'t produce much oil',
  },
  {
    value: 'oily',
    label: 'Oily Scalp',
    description: 'Your scalp produces excess oil and may feel greasy quickly after washing',
  },
  {
    value: 'sensitive',
    label: 'Sensitive Scalp',
    description: 'Your scalp is easily irritated, may be itchy or react to certain products',
  },
  {
    value: 'normal',
    label: 'Normal Scalp',
    description: 'Your scalp is balanced - not too dry or too oily',
  },
];

export default function ScalpTypeStep({ value, onChange }: ScalpTypeStepProps) {
  return (
    <div>
      <h2 className="text-2xl font-bold mb-2">What's your scalp type?</h2>
      <p className="text-gray-600 mb-6">
        Understanding your scalp type helps us recommend the right products and washing frequency. This is optional.
      </p>
      
      <div className="space-y-4">
        {SCALP_OPTIONS.map((option) => (
          <button
            key={option.value}
            type="button"
            onClick={() => onChange(option.value)}
            className={`
              w-full p-5 rounded-lg border-2 text-left transition-all
              ${value === option.value
                ? 'border-blue-600 bg-blue-50 shadow-md'
                : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
              }
            `}
          >
            <div className="font-semibold text-lg mb-2">{option.label}</div>
            <div className="text-sm text-gray-600">{option.description}</div>
          </button>
        ))}
      </div>
    </div>
  );
}
