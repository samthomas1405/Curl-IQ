'use client';

import { useEffect, useMemo, useState } from 'react';
import { useAuth } from '@/lib/auth';
import { useRouter } from 'next/navigation';
import { productsApi } from '@/lib/api';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Star } from 'lucide-react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Navigation } from '@/components/Navigation';

const PRODUCT_TYPES = [
  'shampoo',
  'conditioner',
  'leave-in',
  'cream',
  'gel',
  'mousse',
  'oil',
];

export default function ProductsPage() {
  const { isAuthenticated, loading: authLoading } = useAuth();
  const router = useRouter();
  const [products, setProducts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [fetchError, setFetchError] = useState<string | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Form state
  const [formData, setFormData] = useState({
    brand: '',
    name: '',
    type: '',
    ingredients: '',
    notes: '',
  });

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, authLoading, router]);

  useEffect(() => {
    if (isAuthenticated) {
      fetchProducts();
    }
  }, [isAuthenticated]);

  const fetchProducts = async () => {
    setFetchError(null);
    try {
      const response = await productsApi.getAll();
      setProducts(response.data);
    } catch (err: any) {
      console.error('Failed to fetch products:', err);
      const isNetworkError = err?.code === 'ERR_NETWORK' || err?.message === 'Network Error';
      setFetchError(
        isNetworkError
          ? "Can't reach the backend. Make sure it's running (e.g. uvicorn main:app --reload --host 0.0.0.0 --port 8000)."
          : err?.response?.data?.detail || err?.message || 'Failed to load products.'
      );
      setProducts([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);

    // Validation
    if (!formData.brand.trim() || !formData.name.trim() || !formData.type) {
      setError('Please fill in all required fields (Brand, Name, Type)');
      setSubmitting(false);
      return;
    }

    try {
      // Parse ingredients (comma-separated string to array)
      const ingredients = formData.ingredients
        .split(',')
        .map((ing) => ing.trim())
        .filter((ing) => ing.length > 0);

      const productData = {
        brand: formData.brand.trim(),
        name: formData.name.trim(),
        type: formData.type,
        ingredients: ingredients.length > 0 ? ingredients : undefined,
        notes: formData.notes.trim() || undefined,
      };

      await productsApi.create(productData);
      
      // Reset form and close dialog
      setFormData({
        brand: '',
        name: '',
        type: '',
        ingredients: '',
        notes: '',
      });
      setDialogOpen(false);
      
      // Refresh products list
      await fetchProducts();
    } catch (err: any) {
      console.error('Failed to create product:', err);
      setError(
        err.response?.data?.detail || 
        err.message || 
        'Failed to create product. Please try again.'
      );
    } finally {
      setSubmitting(false);
    }
  };

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleToggleStar = async (product: { id: number; is_starred?: boolean }) => {
    try {
      await productsApi.update(product.id, { is_starred: !product.is_starred });
      await fetchProducts();
    } catch (err) {
      console.error('Failed to update star:', err);
    }
  };

  const starredProducts = useMemo(
    () => products.filter((p) => p.is_starred === true),
    [products]
  );
  const productsByType = useMemo(() => {
    const nonStarred = products.filter((p) => !p.is_starred);
    const map: Record<string, typeof products> = {};
    for (const type of PRODUCT_TYPES) {
      map[type] = nonStarred.filter((p) => p.type === type);
    }
    const other = nonStarred.filter((p) => !PRODUCT_TYPES.includes(p.type));
    if (other.length > 0) map['Other'] = other;
    return map;
  }, [products]);

  if (authLoading || loading) {
    return <div className="flex min-h-screen items-center justify-center">Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-[#FAF5F0]">
      <Navigation />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8 flex justify-between items-center">
          <div>
            <h2 className="font-bold">Products</h2>
            <p className="text-[#6B6B6B] mt-2">Manage your hair care products</p>
          </div>
          <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
            <DialogTrigger asChild>
              <Button>Add Product</Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[500px]">
              <DialogHeader>
                <DialogTitle>Add New Product</DialogTitle>
                <DialogDescription>
                  Add a new hair care product to your library
                </DialogDescription>
              </DialogHeader>
              <form onSubmit={handleSubmit}>
                <div className="grid gap-4 py-4">
                  <div className="grid gap-2">
                    <Label htmlFor="brand">
                      Brand <span className="text-red-500">*</span>
                    </Label>
                    <Input
                      id="brand"
                      name="brand"
                      value={formData.brand}
                      onChange={handleInputChange}
                      placeholder="e.g., Shea Moisture"
                      required
                    />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="name">
                      Product Name <span className="text-red-500">*</span>
                    </Label>
                    <Input
                      id="name"
                      name="name"
                      value={formData.name}
                      onChange={handleInputChange}
                      placeholder="e.g., Coconut & Hibiscus Curl & Shine Shampoo"
                      required
                    />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="type">
                      Type <span className="text-red-500">*</span>
                    </Label>
                    <Select
                      value={formData.type}
                      onValueChange={(value) =>
                        setFormData((prev) => ({ ...prev, type: value }))
                      }
                      required
                    >
                      <SelectTrigger id="type" className="w-full">
                        <SelectValue placeholder="Select product type" />
                      </SelectTrigger>
                      <SelectContent>
                        {PRODUCT_TYPES.map((type) => (
                          <SelectItem key={type} value={type}>
                            {type.charAt(0).toUpperCase() + type.slice(1)}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="ingredients">Ingredients (optional)</Label>
                    <Input
                      id="ingredients"
                      name="ingredients"
                      value={formData.ingredients}
                      onChange={handleInputChange}
                      placeholder="Comma-separated list (e.g., water, glycerin, coconut oil)"
                    />
                    <p className="text-xs text-[#6B6B6B]">
                      Separate multiple ingredients with commas
                    </p>
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="notes">Notes (optional)</Label>
                    <Textarea
                      id="notes"
                      name="notes"
                      value={formData.notes}
                      onChange={handleInputChange}
                      placeholder="Any additional notes about this product..."
                      rows={3}
                    />
                  </div>
                  {error && (
                    <div className="text-sm text-red-600 bg-red-50 p-3 rounded-md">
                      {error}
                    </div>
                  )}
                </div>
                <DialogFooter>
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => setDialogOpen(false)}
                    disabled={submitting}
                  >
                    Cancel
                  </Button>
                  <Button type="submit" disabled={submitting}>
                    {submitting ? 'Adding...' : 'Add Product'}
                  </Button>
                </DialogFooter>
              </form>
            </DialogContent>
          </Dialog>
        </div>

        {fetchError && (
          <Card className="border-amber-200 bg-amber-50/80">
            <CardHeader>
              <CardTitle className="text-amber-800">Could not load products</CardTitle>
              <CardDescription className="text-amber-700">{fetchError}</CardDescription>
            </CardHeader>
            <CardContent>
              <Button variant="outline" onClick={() => { setLoading(true); fetchProducts(); }}>
                Retry
              </Button>
            </CardContent>
          </Card>
        )}

        {!fetchError && products.length > 0 ? (
          <div className="space-y-10">
            {starredProducts.length > 0 && (
              <section>
                <h3 className="font-semibold text-[#1A1A1A] mb-4 flex items-center gap-2">
                  <Star className="h-5 w-5 fill-[#C07B5A] text-[#C07B5A]" />
                  Favorites
                </h3>
                <div className="grid gap-6 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
                  {starredProducts.map((product) => (
                    <Card key={product.id}>
                      <div className="relative">
                        <button
                          type="button"
                          onClick={() => handleToggleStar(product)}
                          className="absolute right-2 top-2 rounded p-1 text-[#C07B5A] hover:bg-[#C07B5A]/10"
                          aria-label={product.is_starred ? 'Unstar' : 'Star'}
                        >
                          <Star className="h-5 w-5 fill-[#C07B5A] text-[#C07B5A]" />
                        </button>
                        <CardHeader className="pb-1 pt-0">
                          <CardTitle className="text-base leading-tight pr-8">
                            {product.brand} — {product.name}
                          </CardTitle>
                          <CardDescription className="text-xs">{product.type}</CardDescription>
                        </CardHeader>
                        <CardContent className="pt-0 text-sm text-[#6B6B6B]">
                          Usage: {product.usage_count} times
                          {product.success_rate > 0 && (
                            <> · {product.success_rate.toFixed(1)}% success</>
                          )}
                        </CardContent>
                      </div>
                    </Card>
                  ))}
                </div>
              </section>
            )}
            {[...PRODUCT_TYPES, 'Other'].map((type) => {
              const list = productsByType[type];
              if (!list?.length) return null;
              return (
                <section key={type}>
                  <h3 className="font-semibold text-[#1A1A1A] mb-4">
                    {type.charAt(0).toUpperCase() + type.slice(1)}
                  </h3>
                  <div className="grid gap-6 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
                    {list.map((product) => (
                      <Card key={product.id}>
                        <div className="relative">
                          <button
                            type="button"
                            onClick={() => handleToggleStar(product)}
                            className="absolute right-2 top-2 rounded p-1 text-[#8B6B4F] hover:bg-[#C07B5A]/10 hover:text-[#C07B5A]"
                            aria-label={product.is_starred ? 'Unstar' : 'Star'}
                          >
                            <Star
                              className={`h-5 w-5 ${product.is_starred ? 'fill-[#C07B5A] text-[#C07B5A]' : ''}`}
                            />
                          </button>
                          <CardHeader className="pb-1 pt-0">
                            <CardTitle className="text-base leading-tight pr-8">
                              {product.brand} — {product.name}
                            </CardTitle>
                            <CardDescription className="text-xs">{product.type}</CardDescription>
                          </CardHeader>
                          <CardContent className="pt-0 text-sm text-[#6B6B6B]">
                            Usage: {product.usage_count} times
                            {product.success_rate > 0 && (
                              <> · {product.success_rate.toFixed(1)}% success</>
                            )}
                          </CardContent>
                        </div>
                      </Card>
                    ))}
                  </div>
                </section>
              );
            })}
          </div>
        ) : !fetchError ? (
          <Card>
            <CardHeader>
              <CardTitle>No products yet</CardTitle>
              <CardDescription>Add your first product to get started</CardDescription>
            </CardHeader>
            <CardContent>
              <Button onClick={() => setDialogOpen(true)}>Add Product</Button>
            </CardContent>
          </Card>
        ) : null}
      </main>
    </div>
  );
}
