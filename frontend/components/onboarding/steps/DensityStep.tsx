'use client';

interface DensityStepProps {
  value?: string;
  onChange: (value: string) => void;
}

const DENSITY_OPTIONS = [
  {
    value: 'low',
    label: 'Low Density',
    description: 'Your scalp is easily visible through your hair',
    visual: '👤',
  },
  {
    value: 'medium',
    label: 'Medium Density',
    description: 'Some scalp is visible, but hair covers most of it',
    visual: '👤',
  },
  {
    value: 'high',
    label: 'High Density',
    description: 'Your scalp is not visible through your hair',
    visual: '👤',
  },
];

export default function DensityStep({ value, onChange }: DensityStepProps) {
  return (
    <div>
      <h2 className="text-2xl font-bold mb-2">How dense is your hair?</h2>
      <p className="text-gray-600 mb-6">
        Density refers to how many hair strands you have on your head. This is optional but helps with styling recommendations.
      </p>
      
      <div className="space-y-4">
        {DENSITY_OPTIONS.map((option) => (
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
            <div className="flex items-center gap-3">
              <span className="text-3xl">{option.visual}</span>
              <div>
                <div className="font-semibold text-lg mb-1">{option.label}</div>
                <div className="text-sm text-gray-600">{option.description}</div>
              </div>
            </div>
          </button>
        ))}
      </div>
      
      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <p className="text-sm text-gray-600">
          <strong>Tip:</strong> Look at your hair when it's parted. Can you see your scalp easily, 
          or is it mostly covered by hair?
        </p>
      </div>
    </div>
  );
}
