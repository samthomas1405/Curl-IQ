'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/lib/auth';
import { useRouter } from 'next/navigation';
import { aiApi, productsApi, routinesApi } from '@/lib/api';
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
import { Sparkles, TrendingUp, Lightbulb, Search, Brain, Zap } from 'lucide-react';

const DRYING_METHODS = ['air-dry', 'diffuser', 'hooded-dryer', 'other'];

type TabType = 'predict' | 'recommendations' | 'insights' | 'patterns';

export default function AIPage() {
  const { isAuthenticated, loading: authLoading } = useAuth();
  const router = useRouter();
  const [activeTab, setActiveTab] = useState<TabType>('predict');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Prediction state
  const [predictionData, setPredictionData] = useState({
    routine_id: '',
    products: [] as number[],
    drying_method: 'air-dry',
    date: new Date().toISOString().split('T')[0],
  });
  const [predictionResult, setPredictionResult] = useState<any>(null);

  // Recommendations state
  const [productRecommendations, setProductRecommendations] = useState<any[]>([]);
  const [routineRecommendations, setRoutineRecommendations] = useState<any[]>([]);
  const [recommendationsLoading, setRecommendationsLoading] = useState(false);

  // Insights state
  const [insights, setInsights] = useState<any[]>([]);
  const [insightsLoading, setInsightsLoading] = useState(false);

  // Patterns state
  const [patterns, setPatterns] = useState<any[]>([]);
  const [patternsLoading, setPatternsLoading] = useState(false);

  // Data for forms
  const [products, setProducts] = useState<any[]>([]);
  const [routines, setRoutines] = useState<any[]>([]);

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, authLoading, router]);

  useEffect(() => {
    if (isAuthenticated) {
      fetchData();
    }
  }, [isAuthenticated]);

  const fetchData = async () => {
    try {
      const [productsRes, routinesRes] = await Promise.all([
        productsApi.getAll(),
        routinesApi.getAll(),
      ]);
      setProducts(productsRes.data);
      setRoutines(routinesRes.data);
    } catch (err) {
      console.error('Failed to fetch data:', err);
    }
  };

  const handlePredict = async () => {
    setLoading(true);
    setError(null);
    setPredictionResult(null);

    try {
      const response = await aiApi.predictOutcome({
        routine_id: predictionData.routine_id || null,
        products: predictionData.products,
        drying_method: predictionData.drying_method,
        date: predictionData.date,
      });
      setPredictionResult(response.data);
    } catch (err: any) {
      console.error('Prediction failed:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to generate prediction');
    } finally {
      setLoading(false);
    }
  };

  const handleGetRecommendations = async () => {
    setRecommendationsLoading(true);
    setError(null);

    try {
      const [productsRes, routinesRes] = await Promise.all([
        aiApi.getProductRecommendations(5),
        aiApi.getRoutineRecommendations(3),
      ]);
      setProductRecommendations(productsRes.data.recommendations || []);
      setRoutineRecommendations(routinesRes.data.recommendations || []);
    } catch (err: any) {
      console.error('Recommendations failed:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to get recommendations');
    } finally {
      setRecommendationsLoading(false);
    }
  };

  const handleGetInsights = async () => {
    setInsightsLoading(true);
    setError(null);

    try {
      const response = await aiApi.getAIInsights();
      setInsights(response.data.insights || []);
    } catch (err: any) {
      console.error('Insights failed:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to get insights');
    } finally {
      setInsightsLoading(false);
    }
  };

  const handleDetectPatterns = async () => {
    setPatternsLoading(true);
    setError(null);

    try {
      const response = await aiApi.detectPatterns();
      setPatterns(response.data.patterns || []);
      if (response.data.message) {
        setError(response.data.message);
      }
    } catch (err: any) {
      console.error('Pattern detection failed:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to detect patterns');
    } finally {
      setPatternsLoading(false);
    }
  };

  const handleTrainModel = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await aiApi.trainModel();
      alert(`Model trained successfully!\n\nMetrics:\n${JSON.stringify(response.data.metrics, null, 2)}`);
    } catch (err: any) {
      console.error('Training failed:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to train model');
    } finally {
      setLoading(false);
    }
  };

  const toggleProductSelection = (productId: number) => {
    setPredictionData((prev) => ({
      ...prev,
      products: prev.products.includes(productId)
        ? prev.products.filter((id) => id !== productId)
        : [...prev.products, productId],
    }));
  };

  if (authLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div>Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#FAF5F0]">
      <Navigation />
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">AI Features</h1>
          <p className="text-muted-foreground">
            Leverage machine learning and AI to optimize your curly hair routine
          </p>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-6 border-b">
          <Button
            variant={activeTab === 'predict' ? 'default' : 'ghost'}
            onClick={() => setActiveTab('predict')}
            className="rounded-b-none"
          >
            <Zap className="mr-2 h-4 w-4" />
            Predict Outcome
          </Button>
          <Button
            variant={activeTab === 'recommendations' ? 'default' : 'ghost'}
            onClick={() => setActiveTab('recommendations')}
            className="rounded-b-none"
          >
            <Sparkles className="mr-2 h-4 w-4" />
            Recommendations
          </Button>
          <Button
            variant={activeTab === 'insights' ? 'default' : 'ghost'}
            onClick={() => setActiveTab('insights')}
            className="rounded-b-none"
          >
            <Lightbulb className="mr-2 h-4 w-4" />
            AI Insights
          </Button>
          <Button
            variant={activeTab === 'patterns' ? 'default' : 'ghost'}
            onClick={() => setActiveTab('patterns')}
            className="rounded-b-none"
          >
            <Search className="mr-2 h-4 w-4" />
            Pattern Detection
          </Button>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-800">
            {error}
          </div>
        )}

        {/* Prediction Tab */}
        {activeTab === 'predict' && (
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Predict Routine Outcome</CardTitle>
                <CardDescription>
                  Get a prediction of how well your routine will work before you try it
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label>Routine (Optional)</Label>
                  <Select
                    value={predictionData.routine_id || undefined}
                    onValueChange={(value) =>
                      setPredictionData((prev) => ({ ...prev, routine_id: value === 'none' ? '' : value }))
                    }
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select a routine template" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="none">None</SelectItem>
                      {routines.map((routine) => (
                        <SelectItem key={routine.id} value={routine.id.toString()}>
                          {routine.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label>Products to Use</Label>
                  <div className="mt-2 space-y-2 max-h-48 overflow-y-auto border rounded-lg p-4">
                    {products.length === 0 ? (
                      <p className="text-sm text-muted-foreground">No products available</p>
                    ) : (
                      products.map((product) => (
                        <label
                          key={product.id}
                          className="flex items-center space-x-2 cursor-pointer hover:bg-gray-50 p-2 rounded"
                        >
                          <input
                            type="checkbox"
                            checked={predictionData.products.includes(product.id)}
                            onChange={() => toggleProductSelection(product.id)}
                            className="rounded"
                          />
                          <span className="text-sm">
                            {product.brand} - {product.name}
                          </span>
                        </label>
                      ))
                    )}
                  </div>
                </div>

                <div>
                  <Label>Drying Method</Label>
                  <Select
                    value={predictionData.drying_method}
                    onValueChange={(value) =>
                      setPredictionData((prev) => ({ ...prev, drying_method: value }))
                    }
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {DRYING_METHODS.map((method) => (
                        <SelectItem key={method} value={method}>
                          {method.replace('-', ' ')}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label>Date</Label>
                  <Input
                    type="date"
                    value={predictionData.date}
                    onChange={(e) =>
                      setPredictionData((prev) => ({ ...prev, date: e.target.value }))
                    }
                  />
                </div>

                <Button onClick={handlePredict} disabled={loading} className="w-full">
                  {loading ? 'Predicting...' : 'Get Prediction'}
                </Button>
              </CardContent>
            </Card>

            {predictionResult && (
              <Card>
                <CardHeader>
                  <CardTitle>Prediction Result</CardTitle>
                </CardHeader>
                <CardContent>
                  {predictionResult.prediction?.error ? (
                    <div className="space-y-4">
                      <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                        <p className="font-semibold text-yellow-800">
                          {predictionResult.prediction.error}
                        </p>
                        <p className="text-sm text-yellow-700 mt-2">
                          {predictionResult.prediction.message}
                        </p>
                        <Button
                          onClick={handleTrainModel}
                          disabled={loading}
                          className="mt-4"
                          variant="outline"
                        >
                          {loading ? 'Training...' : 'Train Model Now'}
                        </Button>
                      </div>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      <div>
                        <div className="text-2xl font-bold text-primary mb-2">
                          Predicted Score: {predictionResult.prediction?.predicted_score?.toFixed(1) || 'N/A'}
                          / 10
                        </div>
                        {predictionResult.prediction?.confidence && (
                          <p className="text-sm text-muted-foreground">
                            Confidence: {(predictionResult.prediction.confidence * 100).toFixed(0)}%
                          </p>
                        )}
                      </div>
                      {predictionResult.weather && (
                        <div className="border-t pt-4">
                          <h4 className="font-semibold mb-2">Weather Conditions</h4>
                          <div className="grid grid-cols-3 gap-4 text-sm">
                            <div>
                              <span className="text-muted-foreground">Temperature:</span>{' '}
                              {predictionResult.weather.temperature}°F
                            </div>
                            <div>
                              <span className="text-muted-foreground">Humidity:</span>{' '}
                              {predictionResult.weather.humidity}%
                            </div>
                            <div>
                              <span className="text-muted-foreground">Dew Point:</span>{' '}
                              {predictionResult.weather.dew_point}°F
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </CardContent>
              </Card>
            )}
          </div>
        )}

        {/* Recommendations Tab */}
        {activeTab === 'recommendations' && (
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Smart Recommendations</CardTitle>
                <CardDescription>
                  Get AI-powered product and routine recommendations based on your hair profile and
                  history
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button
                  onClick={handleGetRecommendations}
                  disabled={recommendationsLoading}
                  className="w-full mb-6"
                >
                  {recommendationsLoading ? 'Loading...' : 'Get Recommendations'}
                </Button>

                {productRecommendations.length > 0 && (
                  <div className="mb-6">
                    <h3 className="text-lg font-semibold mb-4">Recommended Products</h3>
                    <div className="space-y-3">
                      {productRecommendations.map((rec: any, index: number) => (
                        <Card key={index} className="bg-white">
                          <CardContent className="pt-4">
                            <div className="flex justify-between items-start">
                              <div>
                                <h4 className="font-semibold">
                                  {rec.product?.brand} - {rec.product?.name}
                                </h4>
                                <p className="text-sm text-muted-foreground">
                                  {rec.product?.type}
                                </p>
                                {rec.reason && (
                                  <p className="text-sm mt-2 text-muted-foreground">
                                    {rec.reason}
                                  </p>
                                )}
                              </div>
                              {rec.score && (
                                <div className="text-right">
                                  <div className="text-lg font-bold text-primary">
                                    {rec.score.toFixed(2)}
                                  </div>
                                  <div className="text-xs text-muted-foreground">match score</div>
                                </div>
                              )}
                            </div>
                          </CardContent>
                        </Card>
                      ))}
                    </div>
                  </div>
                )}

                {routineRecommendations.length > 0 && (
                  <div>
                    <h3 className="text-lg font-semibold mb-4">Recommended Routines</h3>
                    <div className="space-y-3">
                      {routineRecommendations.map((rec: any, index: number) => (
                        <Card key={index} className="bg-white">
                          <CardContent className="pt-4">
                            <div className="flex justify-between items-start">
                              <div>
                                <h4 className="font-semibold">{rec.routine?.name}</h4>
                                {rec.reason && (
                                  <p className="text-sm mt-2 text-muted-foreground">
                                    {rec.reason}
                                  </p>
                                )}
                              </div>
                              {rec.score && (
                                <div className="text-right">
                                  <div className="text-lg font-bold text-primary">
                                    {rec.score.toFixed(2)}
                                  </div>
                                  <div className="text-xs text-muted-foreground">match score</div>
                                </div>
                              )}
                            </div>
                          </CardContent>
                        </Card>
                      ))}
                    </div>
                  </div>
                )}

                {productRecommendations.length === 0 &&
                  routineRecommendations.length === 0 &&
                  !recommendationsLoading && (
                    <p className="text-center text-muted-foreground py-8">
                      Click "Get Recommendations" to see personalized suggestions
                    </p>
                  )}
              </CardContent>
            </Card>
          </div>
        )}

        {/* Insights Tab */}
        {activeTab === 'insights' && (
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>AI-Powered Insights</CardTitle>
                <CardDescription>
                  Get natural language explanations of patterns in your hair routine data
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button
                  onClick={handleGetInsights}
                  disabled={insightsLoading}
                  className="w-full mb-6"
                >
                  {insightsLoading ? 'Generating Insights...' : 'Get AI Insights'}
                </Button>

                {insights.length > 0 && (
                  <div className="space-y-4">
                    {insights.map((insight: any, index: number) => (
                      <Card key={index} className="bg-white">
                        <CardContent className="pt-4">
                          <div className="space-y-2">
                            <h4 className="font-semibold">{insight.title || 'Insight'}</h4>
                            {insight.ai_explanation ? (
                              <p className="text-sm text-muted-foreground">
                                {insight.ai_explanation}
                              </p>
                            ) : (
                              <p className="text-sm text-muted-foreground">
                                {insight.message || insight.description}
                              </p>
                            )}
                            {insight.confidence && (
                              <p className="text-xs text-muted-foreground">
                                Confidence: {insight.confidence}
                              </p>
                            )}
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                )}

                {insights.length === 0 && !insightsLoading && (
                  <p className="text-center text-muted-foreground py-8">
                    Click "Get AI Insights" to generate personalized insights
                  </p>
                )}
              </CardContent>
            </Card>
          </div>
        )}

        {/* Patterns Tab */}
        {activeTab === 'patterns' && (
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Pattern Detection</CardTitle>
                <CardDescription>
                  Discover statistical patterns in your routine data
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex gap-4 mb-6">
                  <Button
                    onClick={handleDetectPatterns}
                    disabled={patternsLoading}
                    className="flex-1"
                  >
                    {patternsLoading ? 'Detecting...' : 'Detect Patterns'}
                  </Button>
                  <Button
                    onClick={handleTrainModel}
                    disabled={loading}
                    variant="outline"
                    className="flex-1"
                  >
                    {loading ? 'Training...' : 'Train Model'}
                  </Button>
                </div>

                {patterns.length > 0 && (
                  <div className="space-y-4">
                    {patterns.map((pattern: any, index: number) => (
                      <Card key={index} className="bg-white">
                        <CardContent className="pt-4">
                          <div className="space-y-2">
                            <div className="flex items-center justify-between">
                              <h4 className="font-semibold capitalize">{pattern.type}</h4>
                              {pattern.confidence && (
                                <span
                                  className={`text-xs px-2 py-1 rounded ${
                                    pattern.confidence === 'high'
                                      ? 'bg-green-100 text-green-800'
                                      : pattern.confidence === 'medium'
                                        ? 'bg-yellow-100 text-yellow-800'
                                        : 'bg-gray-100 text-gray-800'
                                  }`}
                                >
                                  {pattern.confidence} confidence
                                </span>
                              )}
                            </div>
                            <p className="text-sm text-muted-foreground">{pattern.message}</p>
                            {pattern.trend && (
                              <div className="flex items-center gap-2 text-sm">
                                <TrendingUp className="h-4 w-4" />
                                <span className="capitalize">{pattern.trend}</span>
                              </div>
                            )}
                            {pattern.sample_size && (
                              <p className="text-xs text-muted-foreground">
                                Based on {pattern.sample_size} samples
                              </p>
                            )}
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                )}

                {patterns.length === 0 && !patternsLoading && (
                  <p className="text-center text-muted-foreground py-8">
                    Click "Detect Patterns" to analyze your routine data
                  </p>
                )}
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
}
