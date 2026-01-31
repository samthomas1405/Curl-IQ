'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import Link from 'next/link';
import Image from 'next/image';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await login(email, password);
    } catch (err: any) {
      setError(err.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-[#FAF5F0] px-4">
      <Card className="w-full max-w-md bg-[#FFF9F5] border-[#D4A574]">
        <CardHeader className="flex flex-col items-center space-y-4">
          <Image
            src="/logo.png"
            alt="CurlLabs Logo"
            width={220}
            height={220}
            className="object-contain"
            priority
            unoptimized
          />
          <div className="text-center w-full">
            <CardTitle className="text-2xl text-[#1A1A1A]">Welcome to CurlLabs</CardTitle>
            <CardDescription className="text-[#6B6B6B]">Sign in to your account</CardDescription>
          </div>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="rounded-md bg-[#FFF9F5] border border-[#C07B5A] p-3 text-sm text-[#C07B5A]">
                {error}
              </div>
            )}
            <div className="space-y-2">
              <Label htmlFor="email" className="text-[#6B6B6B]">Email</Label>
              <Input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                placeholder="you@example.com"
                className="border-[#D4A574]"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password" className="text-[#6B6B6B]">Password</Label>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="border-[#D4A574]"
              />
            </div>
            <Button type="submit" className="w-full bg-[#C07B5A] hover:bg-[#B87C5C] text-[#FFF9F5]" disabled={loading}>
              {loading ? 'Signing in...' : 'Sign in'}
            </Button>
          </form>
          <div className="mt-4 text-center text-sm">
            <span className="text-[#6B6B6B]">Don't have an account? </span>
            <Link href="/register" className="text-[#B87C5C] hover:underline">
              Sign up
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
