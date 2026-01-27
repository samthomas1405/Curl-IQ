'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/lib/auth';
import { useRouter } from 'next/navigation';
import { userApi } from '@/lib/api';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Navigation } from '@/components/Navigation';
import { LocationInput } from '@/components/LocationInput';
import { X } from 'lucide-react';

const CURL_PATTERNS = [
  { value: '2A', label: '2A - Wavy (Loose)' },
  { value: '2B', label: '2B - Wavy (Defined)' },
  { value: '2C', label: '2C - Wavy (Tight)' },
  { value: '3A', label: '3A - Curly (Loose)' },
  { value: '3B', label: '3B - Curly (Defined)' },
  { value: '3C', label: '3C - Curly (Tight)' },
  { value: '4A', label: '4A - Coily (Loose)' },
  { value: '4B', label: '4B - Coily (Zigzag)' },
  { value: '4C', label: '4C - Coily (Tight)' },
];

const POROSITY_OPTIONS = [
  { value: 'low', label: 'Low Porosity' },
  { value: 'medium', label: 'Medium Porosity' },
  { value: 'high', label: 'High Porosity' },
];

const DENSITY_OPTIONS = [
  { value: 'low', label: 'Low Density' },
  { value: 'medium', label: 'Medium Density' },
  { value: 'high', label: 'High Density' },
];

const THICKNESS_OPTIONS = [
  { value: 'fine', label: 'Fine' },
  { value: 'medium', label: 'Medium' },
  { value: 'coarse', label: 'Coarse' },
];

const SCALP_OPTIONS = [
  { value: 'dry', label: 'Dry Scalp' },
  { value: 'oily', label: 'Oily Scalp' },
  { value: 'sensitive', label: 'Sensitive Scalp' },
  { value: 'normal', label: 'Normal Scalp' },
];

export default function ProfilePage() {
  const { isAuthenticated, loading: authLoading, user, refreshUser } = useAuth();
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [isEditing, setIsEditing] = useState(false);

  const [formData, setFormData] = useState({
    curl_pattern: '',
    porosity: '',
    density: '',
    thickness: '',
    scalp_type: '',
    location: '',
  });

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, authLoading, router]);

  useEffect(() => {
    if (user) {
      setFormData({
        curl_pattern: user.curl_pattern || '',
        porosity: user.porosity || '',
        density: user.density || '',
        thickness: user.thickness || '',
        scalp_type: user.scalp_type || '',
        location: user.location || '',
      });
      setLoading(false);
    }
  }, [user]);

  const handleSave = async () => {
    setSaving(true);
    setError(null);
    setSuccess(false);

    try {
      // Validate required fields
      if (!formData.curl_pattern || !formData.porosity) {
        setError('Curl pattern and porosity are required');
        setSaving(false);
        return;
      }

      await userApi.updateProfile(formData);
      setSuccess(true);
      setIsEditing(false);
      
      // Refresh user data in auth context
      await refreshUser();
      
      setTimeout(() => setSuccess(false), 3000);
    } catch (err: any) {
      console.error('Failed to update profile:', err);
      setError(
        err.response?.data?.detail || 
        err.message || 
        'Failed to update profile. Please try again.'
      );
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    if (user) {
      setFormData({
        curl_pattern: user.curl_pattern || '',
        porosity: user.porosity || '',
        density: user.density || '',
        thickness: user.thickness || '',
        scalp_type: user.scalp_type || '',
        location: user.location || '',
      });
    }
    setIsEditing(false);
    setError(null);
    setSuccess(false);
  };

  if (authLoading || loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#E6E6FA]">
      <Navigation />

      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold">Profile</h2>
          <p className="text-gray-600 mt-2">Manage your account and hair profile</p>
        </div>

        {/* Account Information */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Account Information</CardTitle>
            <CardDescription>Your account details</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <Label>Email</Label>
                <Input
                  type="email"
                  value={user?.email || ''}
                  disabled
                  className="mt-1 bg-white"
                />
                <p className="mt-1 text-sm text-gray-500">
                  Email cannot be changed
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Hair Profile */}
        <Card>
          <CardHeader>
            <div className="flex justify-between items-center">
              <div>
                <CardTitle>Hair Profile</CardTitle>
                <CardDescription>Your hair characteristics and preferences</CardDescription>
              </div>
              {!isEditing && (
                <Button onClick={() => setIsEditing(true)} variant="outline">
                  Edit Profile
                </Button>
              )}
            </div>
          </CardHeader>
          <CardContent>
            {error && (
              <div className="mb-4 rounded-md bg-red-50 p-3 text-sm text-red-800">
                {error}
              </div>
            )}
            {success && (
              <div className="mb-4 rounded-md bg-green-50 p-3 text-sm text-green-800">
                Profile updated successfully!
              </div>
            )}

            {isEditing ? (
              <div className="space-y-6">
                {/* Curl Pattern */}
                <div>
                  <Label htmlFor="curl_pattern">
                    Curl Pattern <span className="text-red-500">*</span>
                  </Label>
                  <Select
                    value={formData.curl_pattern}
                    onValueChange={(value) =>
                      setFormData((prev) => ({ ...prev, curl_pattern: value }))
                    }
                  >
                    <SelectTrigger id="curl_pattern" className="mt-2">
                      <SelectValue placeholder="Select curl pattern" />
                    </SelectTrigger>
                    <SelectContent>
                      {CURL_PATTERNS.map((pattern) => (
                        <SelectItem key={pattern.value} value={pattern.value}>
                          {pattern.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Porosity */}
                <div>
                  <Label htmlFor="porosity">
                    Porosity <span className="text-red-500">*</span>
                  </Label>
                  <Select
                    value={formData.porosity}
                    onValueChange={(value) =>
                      setFormData((prev) => ({ ...prev, porosity: value }))
                    }
                  >
                    <SelectTrigger id="porosity" className="mt-2">
                      <SelectValue placeholder="Select porosity" />
                    </SelectTrigger>
                    <SelectContent>
                      {POROSITY_OPTIONS.map((option) => (
                        <SelectItem key={option.value} value={option.value}>
                          {option.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Density */}
                <div>
                  <Label htmlFor="density">Density (optional)</Label>
                  <div className="flex gap-2 mt-2">
                    <Select
                      value={formData.density || undefined}
                      onValueChange={(value) =>
                        setFormData((prev) => ({ ...prev, density: value }))
                      }
                    >
                      <SelectTrigger id="density" className="flex-1">
                        <SelectValue placeholder="Select density" />
                      </SelectTrigger>
                      <SelectContent>
                        {DENSITY_OPTIONS.map((option) => (
                          <SelectItem key={option.value} value={option.value}>
                            {option.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    {formData.density && (
                      <Button
                        type="button"
                        variant="outline"
                        size="icon"
                        onClick={() => setFormData((prev) => ({ ...prev, density: '' }))}
                      >
                        <X className="h-4 w-4" />
                      </Button>
                    )}
                  </div>
                </div>

                {/* Thickness */}
                <div>
                  <Label htmlFor="thickness">Thickness (optional)</Label>
                  <div className="flex gap-2 mt-2">
                    <Select
                      value={formData.thickness || undefined}
                      onValueChange={(value) =>
                        setFormData((prev) => ({ ...prev, thickness: value }))
                      }
                    >
                      <SelectTrigger id="thickness" className="flex-1">
                        <SelectValue placeholder="Select thickness" />
                      </SelectTrigger>
                      <SelectContent>
                        {THICKNESS_OPTIONS.map((option) => (
                          <SelectItem key={option.value} value={option.value}>
                            {option.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    {formData.thickness && (
                      <Button
                        type="button"
                        variant="outline"
                        size="icon"
                        onClick={() => setFormData((prev) => ({ ...prev, thickness: '' }))}
                      >
                        <X className="h-4 w-4" />
                      </Button>
                    )}
                  </div>
                </div>

                {/* Scalp Type */}
                <div>
                  <Label htmlFor="scalp_type">Scalp Type (optional)</Label>
                  <div className="flex gap-2 mt-2">
                    <Select
                      value={formData.scalp_type || undefined}
                      onValueChange={(value) =>
                        setFormData((prev) => ({ ...prev, scalp_type: value }))
                      }
                    >
                      <SelectTrigger id="scalp_type" className="flex-1">
                        <SelectValue placeholder="Select scalp type" />
                      </SelectTrigger>
                      <SelectContent>
                        {SCALP_OPTIONS.map((option) => (
                          <SelectItem key={option.value} value={option.value}>
                            {option.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    {formData.scalp_type && (
                      <Button
                        type="button"
                        variant="outline"
                        size="icon"
                        onClick={() => setFormData((prev) => ({ ...prev, scalp_type: '' }))}
                      >
                        <X className="h-4 w-4" />
                      </Button>
                    )}
                  </div>
                </div>

                {/* Location */}
                <div>
                  <Label htmlFor="location">Location (optional)</Label>
                  <div className="mt-2">
                    <LocationInput
                      id="location"
                      value={formData.location}
                      onChange={(value) =>
                        setFormData((prev) => ({ ...prev, location: value }))
                      }
                      placeholder="e.g., New York, NY, USA"
                    />
                  </div>
                  <p className="mt-1 text-sm text-gray-500">
                    Used for weather tracking. Start typing to see suggestions.
                  </p>
                </div>

                <div className="flex gap-2 pt-4">
                  <Button onClick={handleSave} disabled={saving}>
                    {saving ? 'Saving...' : 'Save Changes'}
                  </Button>
                  <Button onClick={handleCancel} variant="outline" disabled={saving}>
                    Cancel
                  </Button>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label className="text-gray-500">Curl Pattern</Label>
                    <p className="mt-1 font-medium">
                      {user?.curl_pattern
                        ? CURL_PATTERNS.find((p) => p.value === user.curl_pattern)?.label ||
                          user.curl_pattern
                        : 'Not set'}
                    </p>
                  </div>
                  <div>
                    <Label className="text-gray-500">Porosity</Label>
                    <p className="mt-1 font-medium">
                      {user?.porosity
                        ? POROSITY_OPTIONS.find((p) => p.value === user.porosity)?.label ||
                          user.porosity
                        : 'Not set'}
                    </p>
                  </div>
                  <div>
                    <Label className="text-gray-500">Density</Label>
                    <p className="mt-1 font-medium">
                      {user?.density
                        ? DENSITY_OPTIONS.find((d) => d.value === user.density)?.label ||
                          user.density
                        : 'Not set'}
                    </p>
                  </div>
                  <div>
                    <Label className="text-gray-500">Thickness</Label>
                    <p className="mt-1 font-medium">
                      {user?.thickness
                        ? THICKNESS_OPTIONS.find((t) => t.value === user.thickness)?.label ||
                          user.thickness
                        : 'Not set'}
                    </p>
                  </div>
                  <div>
                    <Label className="text-gray-500">Scalp Type</Label>
                    <p className="mt-1 font-medium">
                      {user?.scalp_type
                        ? SCALP_OPTIONS.find((s) => s.value === user.scalp_type)?.label ||
                          user.scalp_type
                        : 'Not set'}
                    </p>
                  </div>
                  <div>
                    <Label className="text-gray-500">Location</Label>
                    <p className="mt-1 font-medium">
                      {user?.location || 'Not set'}
                    </p>
                  </div>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      </main>
    </div>
  );
}
