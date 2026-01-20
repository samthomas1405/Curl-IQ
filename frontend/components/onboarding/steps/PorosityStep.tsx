'use client';

interface PorosityStepProps {
  value?: string;
  onChange: (value: string) => void;
}

const POROSITY_OPTIONS = [
  {
    value: 'low',
    label: 'Low Porosity',
    description: 'Hair cuticles are tightly closed. Products tend to sit on your hair rather than absorb quickly.',
    tips: 'Your hair may take longer to get wet and products may feel heavy.',
  },
  {
    value: 'medium',
    label: 'Medium Porosity',
    description: 'Hair cuticles are moderately open. Your hair absorbs and retains moisture well.',
    tips: 'Your hair is balanced and responds well to most products.',
  },
  {
    value: 'high',
    label: 'High Porosity',
    description: 'Hair cuticles are very open. Your hair absorbs moisture quickly but may lose it just as fast.',
    tips: 'Your hair may feel dry quickly and benefit from heavier moisturizing products.',
  },
];

export default function PorosityStep({ value, onChange }: PorosityStepProps) {
  return (
    <div>
      <h2 className="text-2xl font-bold mb-2">What's your hair porosity?</h2>
      <p className="text-gray-600 mb-6">
        Porosity determines how well your hair absorbs and retains moisture. This is crucial for choosing the right products.
      </p>
      
      <div className="space-y-4">
        {POROSITY_OPTIONS.map((option) => (
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
        <p className="text-sm text-gray-600 mb-2">
          <strong>Not sure?</strong> Try the float test:
        </p>
        <ul className="text-sm text-gray-600 list-disc list-inside space-y-1">
          <li>Place a clean strand of hair in a bowl of water</li>
          <li>If it floats: Low porosity</li>
          <li>If it sinks slowly: Medium porosity</li>
          <li>If it sinks quickly: High porosity</li>
        </ul>
      </div>
    </div>
  );
}
