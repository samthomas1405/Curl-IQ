'use client';

interface CurlPatternStepProps {
  value?: string;
  onChange: (value: string) => void;
}

const CURL_PATTERNS = [
  { value: '2A', label: '2A - Wavy (Loose)', description: 'Loose S-shaped waves' },
  { value: '2B', label: '2B - Wavy (Defined)', description: 'More defined S-waves' },
  { value: '2C', label: '2C - Wavy (Tight)', description: 'Tight S-waves with some spirals' },
  { value: '3A', label: '3A - Curly (Loose)', description: 'Large, loose curls' },
  { value: '3B', label: '3B - Curly (Defined)', description: 'Medium, springy curls' },
  { value: '3C', label: '3C - Curly (Tight)', description: 'Tight, corkscrew curls' },
  { value: '4A', label: '4A - Coily (Loose)', description: 'Loose, S-shaped coils' },
  { value: '4B', label: '4B - Coily (Zigzag)', description: 'Z-shaped coils' },
  { value: '4C', label: '4C - Coily (Tight)', description: 'Tight, densely packed coils' },
];

export default function CurlPatternStep({ value, onChange }: CurlPatternStepProps) {
  return (
    <div>
      <h2 className="text-2xl font-bold mb-2">What's your curl pattern?</h2>
      <p className="text-gray-600 mb-6">
        Select the pattern that best matches your hair. This helps us personalize your recommendations.
      </p>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {CURL_PATTERNS.map((pattern) => (
          <button
            key={pattern.value}
            type="button"
            onClick={() => onChange(pattern.value)}
            className={`
              p-4 rounded-lg border-2 text-left transition-all
              ${value === pattern.value
                ? 'border-blue-600 bg-blue-50 shadow-md'
                : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
              }
            `}
          >
            <div className="font-semibold text-lg mb-1">{pattern.label}</div>
            <div className="text-sm text-gray-600">{pattern.description}</div>
          </button>
        ))}
      </div>
      
      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <p className="text-sm text-gray-600">
          <strong>Not sure?</strong> Look at your hair when it's wet and air-dried. 
          The pattern refers to the shape of your curls - waves (2), curls (3), or coils (4).
        </p>
      </div>
    </div>
  );
}
