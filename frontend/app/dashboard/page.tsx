'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/lib/auth';
import { useRouter } from 'next/navigation';
import { dashboardApi } from '@/lib/api';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Navigation } from '@/components/Navigation';
import Link from 'next/link';

export default function DashboardPage() {
  const { isAuthenticated, loading: authLoading, logout } = useAuth();
  const router = useRouter();
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, authLoading, router]);

  useEffect(() => {
    if (isAuthenticated) {
      fetchStats();
    }
  }, [isAuthenticated]);

  const fetchStats = async () => {
    try {
      const response = await dashboardApi.getStats();
      setStats(response.data);
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (authLoading || loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div>Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold">Dashboard</h2>
          <p className="text-gray-600 mt-2">Your curly hair routine insights</p>
        </div>

        {stats ? (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            <Card>
              <CardHeader>
                <CardTitle>Total Logs</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">{stats.total_logs}</div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Total Outcomes</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">{stats.total_outcomes}</div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Average Overall Score</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">
                  {stats.average_scores?.overall?.toFixed(1) || 'N/A'}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Best Routine</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-lg font-semibold">
                  {stats.best_routine?.name || 'N/A'}
                </div>
                {stats.best_routine && (
                  <div className="text-sm text-gray-600">
                    Score: {stats.best_routine.average_score.toFixed(1)}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        ) : (
          <Card>
            <CardHeader>
              <CardTitle>Welcome!</CardTitle>
              <CardDescription>
                Start by creating a product or routine, then log your first routine.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex gap-4">
                <Link href="/products">
                  <Button>Add Products</Button>
                </Link>
                <Link href="/routines">
                  <Button>Create Routine</Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        )}
      </main>
    </div>
  );
}
