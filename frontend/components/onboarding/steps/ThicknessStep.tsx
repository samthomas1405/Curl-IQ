'use client';

interface ThicknessStepProps {
  value?: string;
  onChange: (value: string) => void;
}

const THICKNESS_OPTIONS = [
  {
    value: 'fine',
    label: 'Fine',
    description: 'Individual hair strands are thin and delicate',
    tips: 'May need lighter products to avoid weighing down',
  },
  {
    value: 'medium',
    label: 'Medium',
    description: 'Individual hair strands are average thickness',
    tips: 'Can handle a variety of product weights',
  },
  {
    value: 'coarse',
    label: 'Coarse',
    description: 'Individual hair strands are thick and strong',
    tips: 'Can handle heavier, richer products',
  },
];

export default function ThicknessStep({ value, onChange }: ThicknessStepProps) {
  return (
    <div>
      <h2 className="text-2xl font-bold mb-2">What's your hair strand thickness?</h2>
      <p className="text-gray-600 mb-6">
        Thickness refers to the width of individual hair strands, not how many strands you have. This is optional.
      </p>
      
      <div className="space-y-4">
        {THICKNESS_OPTIONS.map((option) => (
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
            <div className="text-sm text-gray-700 mb-2">{option.description}</div>
            <div className="text-xs text-gray-500 italic">{option.tips}</div>
          </button>
        ))}
      </div>
      
      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <p className="text-sm text-gray-600">
          <strong>Tip:</strong> Take a single strand of hair and feel it between your fingers. 
          Fine hair feels thin and silky, while coarse hair feels thick and strong.
        </p>
      </div>
    </div>
  );
}
