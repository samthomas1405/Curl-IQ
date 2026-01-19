'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/lib/auth';
import { useRouter } from 'next/navigation';
import { routinesApi, productsApi } from '@/lib/api';
import { Navigation } from '@/components/Navigation';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

const STEP_TYPES = ['cleanse', 'condition', 'deep-condition', 'leave-in', 'style', 'oil', 'other'];
const DRYING_METHODS = ['air-dry', 'diffuser', 'hooded-dryer', 'other'];
const METHOD_TAGS = ['wash-and-go', 'twist-out', 'braid-out', 'silk-press-prep', 'other'];
const PRODUCT_TYPES = [
  'shampoo',
  'conditioner',
  'leave-in',
  'cream',
  'gel',
  'mousse',
  'oil',
];

interface RoutineStep {
  step_type: string;
  product_id: number | null;
  order: number;
  notes: string;
}

export default function RoutinesPage() {
  const { isAuthenticated, loading: authLoading } = useAuth();
  const router = useRouter();
  const [routines, setRoutines] = useState<any[]>([]);
  const [products, setProducts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingRoutine, setEditingRoutine] = useState<any | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showAddProductDialog, setShowAddProductDialog] = useState(false);
  const [newProductData, setNewProductData] = useState({
    brand: '',
    name: '',
    type: '',
    ingredients: '',
    notes: '',
  });

  const [formData, setFormData] = useState({
    name: '',
    is_template: true,
    is_public: false,
    steps: [] as RoutineStep[],
    method_tags: [] as string[],
    drying_method: '',
  });

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
      const [routinesRes, productsRes] = await Promise.all([
        routinesApi.getAll(),
        productsApi.getAll(),
      ]);
      setRoutines(routinesRes.data);
      setProducts(productsRes.data);
    } catch (error) {
      console.error('Failed to fetch data:', error);
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      is_template: true,
      is_public: false,
      steps: [],
      method_tags: [],
      drying_method: '',
    });
    setEditingRoutine(null);
    setError(null);
  };

  const handleOpenDialog = (routine?: any) => {
    if (routine) {
      setEditingRoutine(routine);
      setFormData({
        name: routine.name,
        is_template: routine.is_template,
        is_public: routine.is_public,
        steps: routine.steps || [],
        method_tags: routine.method_tags || [],
        drying_method: routine.drying_method || '',
      });
    } else {
      resetForm();
    }
    setDialogOpen(true);
  };

  const addStep = () => {
    setFormData((prev) => ({
      ...prev,
      steps: [
        ...prev.steps,
        {
          step_type: 'cleanse',
          product_id: null,
          order: prev.steps.length + 1,
          notes: '',
        },
      ],
    }));
  };

  const updateStep = (index: number, field: keyof RoutineStep, value: any) => {
    setFormData((prev) => ({
      ...prev,
      steps: prev.steps.map((step, i) =>
        i === index ? { ...step, [field]: value } : step
      ),
    }));
  };

  const removeStep = (index: number) => {
    setFormData((prev) => ({
      ...prev,
      steps: prev.steps
        .filter((_, i) => i !== index)
        .map((step, i) => ({ ...step, order: i + 1 })),
    }));
  };

  const toggleMethodTag = (tag: string) => {
    setFormData((prev) => ({
      ...prev,
      method_tags: prev.method_tags.includes(tag)
        ? prev.method_tags.filter((t) => t !== tag)
        : [...prev.method_tags, tag],
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);

    // Validation
    if (!formData.name.trim()) {
      setError('Please enter a routine name');
      setSubmitting(false);
      return;
    }

    if (formData.steps.length === 0) {
      setError('Please add at least one step to the routine');
      setSubmitting(false);
      return;
    }

    try {
      const routineData = {
        name: formData.name.trim(),
        is_template: formData.is_template,
        is_public: formData.is_public,
        steps: formData.steps.map((step) => ({
          ...step,
          product_id: step.product_id || undefined,
          notes: step.notes?.trim() || undefined,
        })),
        method_tags: formData.method_tags.length > 0 ? formData.method_tags : undefined,
        drying_method: formData.drying_method || undefined,
      };

      if (editingRoutine) {
        await routinesApi.update(editingRoutine.id, routineData);
      } else {
        await routinesApi.create(routineData);
      }

      resetForm();
      setDialogOpen(false);
      await fetchData();
    } catch (err: any) {
      console.error('Failed to save routine:', err);
      setError(
        err.response?.data?.detail ||
          err.message ||
          'Failed to save routine. Please try again.'
      );
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (routineId: number) => {
    if (!confirm('Are you sure you want to delete this routine?')) {
      return;
    }

    try {
      await routinesApi.delete(routineId);
      await fetchData();
    } catch (err: any) {
      console.error('Failed to delete routine:', err);
      alert('Failed to delete routine. Please try again.');
    }
  };

  const handleAddProduct = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!newProductData.brand.trim() || !newProductData.name.trim() || !newProductData.type) {
      setError('Please fill in all required fields (Brand, Name, Type)');
      return;
    }

    try {
      const ingredients = newProductData.ingredients
        .split(',')
        .map((ing) => ing.trim())
        .filter((ing) => ing.length > 0);

      const productData = {
        brand: newProductData.brand.trim(),
        name: newProductData.name.trim(),
        type: newProductData.type,
        ingredients: ingredients.length > 0 ? ingredients : undefined,
        notes: newProductData.notes.trim() || undefined,
      };

      const response = await productsApi.create(productData);
      await fetchData(); // Refresh products list
      
      // Reset form and close dialog
      setNewProductData({
        brand: '',
        name: '',
        type: '',
        ingredients: '',
        notes: '',
      });
      setShowAddProductDialog(false);
      
      // Optionally select the newly created product
      return response.data.id;
    } catch (err: any) {
      console.error('Failed to create product:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to create product');
      throw err;
    }
  };

  if (authLoading || loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navigation />
        <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center">
          <div>Loading...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8 flex justify-between items-center">
          <div>
            <h2 className="text-3xl font-bold">Routines</h2>
            <p className="text-gray-600 mt-2">Create and manage your hair care routine templates</p>
          </div>
          <Dialog open={dialogOpen} onOpenChange={(open) => {
            setDialogOpen(open);
            if (!open) resetForm();
          }}>
            <DialogTrigger asChild>
              <Button onClick={() => handleOpenDialog()}>Create Routine</Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[700px] max-h-[90vh] overflow-y-auto">
              <DialogHeader>
                <DialogTitle>
                  {editingRoutine ? 'Edit Routine' : 'Create New Routine'}
                </DialogTitle>
                <DialogDescription>
                  Build a reusable routine template with steps and products
                </DialogDescription>
              </DialogHeader>
              <form onSubmit={handleSubmit}>
                <div className="grid gap-4 py-4">
                  <div className="grid gap-2">
                    <Label htmlFor="name">
                      Routine Name <span className="text-red-500">*</span>
                    </Label>
                    <Input
                      id="name"
                      value={formData.name}
                      onChange={(e) =>
                        setFormData((prev) => ({ ...prev, name: e.target.value }))
                      }
                      placeholder="e.g., Wash Day Routine"
                      required
                    />
                  </div>

                  <div className="grid gap-2">
                    <Label>Steps <span className="text-red-500">*</span></Label>
                    {formData.steps.length === 0 ? (
                      <p className="text-sm text-gray-500">No steps added yet. Click "Add Step" to get started.</p>
                    ) : (
                      <div className="space-y-3">
                        {formData.steps.map((step, index) => (
                          <Card key={index} className="p-4">
                            <div className="flex justify-between items-start mb-3">
                              <span className="font-medium text-sm">Step {step.order}</span>
                              <Button
                                type="button"
                                variant="ghost"
                                size="sm"
                                onClick={() => removeStep(index)}
                              >
                                Remove
                              </Button>
                            </div>
                            <div className="grid gap-3">
                              <div className="grid gap-2">
                                <Label className="text-xs">Step Type</Label>
                                <Select
                                  value={step.step_type}
                                  onValueChange={(value) =>
                                    updateStep(index, 'step_type', value)
                                  }
                                >
                                  <SelectTrigger>
                                    <SelectValue />
                                  </SelectTrigger>
                                  <SelectContent>
                                    {STEP_TYPES.map((type) => (
                                      <SelectItem key={type} value={type}>
                                        {type.charAt(0).toUpperCase() + type.slice(1).replace('-', ' ')}
                                      </SelectItem>
                                    ))}
                                  </SelectContent>
                                </Select>
                              </div>
                              <div className="grid gap-2">
                                <Label className="text-xs">Product (optional)</Label>
                                <Select
                                  value={step.product_id?.toString() || undefined}
                                  onValueChange={(value) =>
                                    updateStep(index, 'product_id', value ? parseInt(value) : null)
                                  }
                                >
                                  <SelectTrigger>
                                    <SelectValue placeholder="Select a product (optional)" />
                                  </SelectTrigger>
                                  <SelectContent>
                                    {products.map((product) => (
                                      <SelectItem key={product.id} value={product.id.toString()}>
                                        {product.brand} - {product.name} ({product.type})
                                      </SelectItem>
                                    ))}
                                    <div className="border-t pt-1 mt-1">
                                      <Button
                                        type="button"
                                        variant="ghost"
                                        size="sm"
                                        className="w-full justify-start"
                                        onClick={(e) => {
                                          e.preventDefault();
                                          setShowAddProductDialog(true);
                                        }}
                                      >
                                        + Add New Product
                                      </Button>
                                    </div>
                                  </SelectContent>
                                </Select>
                                {step.product_id && (
                                  <Button
                                    type="button"
                                    variant="ghost"
                                    size="sm"
                                    onClick={() => updateStep(index, 'product_id', null)}
                                    className="text-xs h-6"
                                  >
                                    Clear selection
                                  </Button>
                                )}
                              </div>
                              <div className="grid gap-2">
                                <Label className="text-xs">Notes (optional)</Label>
                                <Input
                                  value={step.notes}
                                  onChange={(e) => updateStep(index, 'notes', e.target.value)}
                                  placeholder="Any notes for this step..."
                                />
                              </div>
                            </div>
                          </Card>
                        ))}
                      </div>
                    )}
                    <Button
                      type="button"
                      variant="outline"
                      onClick={addStep}
                    >
                      Add Step
                    </Button>
                  </div>

                  <div className="grid gap-2">
                    <Label>Method Tags (optional)</Label>
                    <div className="flex flex-wrap gap-2">
                      {METHOD_TAGS.map((tag) => (
                        <Button
                          key={tag}
                          type="button"
                          variant={formData.method_tags.includes(tag) ? 'default' : 'outline'}
                          size="sm"
                          onClick={() => toggleMethodTag(tag)}
                        >
                          {tag.replace('-', ' ')}
                        </Button>
                      ))}
                    </div>
                  </div>

                  <div className="grid gap-2">
                    <Label htmlFor="drying_method">Drying Method (optional)</Label>
                    <div className="flex gap-2">
                      <Select
                        value={formData.drying_method || undefined}
                        onValueChange={(value) =>
                          setFormData((prev) => ({ ...prev, drying_method: value }))
                        }
                      >
                        <SelectTrigger id="drying_method" className="flex-1">
                          <SelectValue placeholder="Select drying method" />
                        </SelectTrigger>
                        <SelectContent>
                          {DRYING_METHODS.map((method) => (
                            <SelectItem key={method} value={method}>
                              {method.charAt(0).toUpperCase() + method.slice(1).replace('-', ' ')}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                      {formData.drying_method && (
                        <Button
                          type="button"
                          variant="outline"
                          onClick={() => setFormData((prev) => ({ ...prev, drying_method: '' }))}
                        >
                          Clear
                        </Button>
                      )}
                    </div>
                  </div>

                  <div className="flex items-center gap-4">
                    <label className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        checked={formData.is_template}
                        onChange={(e) =>
                          setFormData((prev) => ({ ...prev, is_template: e.target.checked }))
                        }
                      />
                      <span className="text-sm">Template</span>
                    </label>
                    <label className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        checked={formData.is_public}
                        onChange={(e) =>
                          setFormData((prev) => ({ ...prev, is_public: e.target.checked }))
                        }
                      />
                      <span className="text-sm">Public (share with community)</span>
                    </label>
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
                    onClick={() => {
                      setDialogOpen(false);
                      resetForm();
                    }}
                    disabled={submitting}
                  >
                    Cancel
                  </Button>
                  <Button type="submit" disabled={submitting}>
                    {submitting
                      ? 'Saving...'
                      : editingRoutine
                      ? 'Update Routine'
                      : 'Create Routine'}
                  </Button>
                </DialogFooter>
              </form>
            </DialogContent>
          </Dialog>
        </div>

        {routines.length > 0 ? (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {routines.map((routine) => (
              <Card key={routine.id}>
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <div>
                      <CardTitle>{routine.name}</CardTitle>
                      <CardDescription>
                        {routine.steps?.length || 0} steps
                        {routine.method_tags && routine.method_tags.length > 0 && (
                          <span className="ml-2">
                            • {routine.method_tags.join(', ')}
                          </span>
                        )}
                      </CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2 mb-4">
                    {routine.steps && routine.steps.length > 0 ? (
                      <div className="text-sm">
                        <div className="font-medium mb-1">Steps:</div>
                        <ol className="list-decimal list-inside space-y-1 text-gray-600">
                          {routine.steps.map((step: any, idx: number) => (
                            <li key={idx}>
                              {step.step_type}
                              {step.notes && ` (${step.notes})`}
                            </li>
                          ))}
                        </ol>
                      </div>
                    ) : (
                      <p className="text-sm text-gray-500">No steps defined</p>
                    )}
                    {routine.drying_method && (
                      <div className="text-sm text-gray-600">
                        Drying: {routine.drying_method.replace('-', ' ')}
                      </div>
                    )}
                  </div>
                  <div className="flex gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleOpenDialog(routine)}
                    >
                      Edit
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleDelete(routine.id)}
                    >
                      Delete
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <Card>
            <CardHeader>
              <CardTitle>No routines yet</CardTitle>
              <CardDescription>
                Create your first routine template to get started
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button onClick={() => handleOpenDialog()}>Create Routine</Button>
            </CardContent>
          </Card>
        )}
      </main>

      {/* Add Product Dialog */}
      <Dialog open={showAddProductDialog} onOpenChange={setShowAddProductDialog}>
        <DialogContent className="sm:max-w-[500px]">
          <DialogHeader>
            <DialogTitle>Add New Product</DialogTitle>
            <DialogDescription>
              Add a new product to your library
            </DialogDescription>
          </DialogHeader>
          <form onSubmit={handleAddProduct}>
            <div className="grid gap-4 py-4">
              <div className="grid gap-2">
                <Label htmlFor="new_brand">
                  Brand <span className="text-red-500">*</span>
                </Label>
                <Input
                  id="new_brand"
                  value={newProductData.brand}
                  onChange={(e) =>
                    setNewProductData((prev) => ({ ...prev, brand: e.target.value }))
                  }
                  placeholder="e.g., Shea Moisture"
                  required
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="new_name">
                  Product Name <span className="text-red-500">*</span>
                </Label>
                <Input
                  id="new_name"
                  value={newProductData.name}
                  onChange={(e) =>
                    setNewProductData((prev) => ({ ...prev, name: e.target.value }))
                  }
                  placeholder="e.g., Coconut & Hibiscus Curl & Shine Shampoo"
                  required
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="new_type">
                  Type <span className="text-red-500">*</span>
                </Label>
                <Select
                  value={newProductData.type}
                  onValueChange={(value) =>
                    setNewProductData((prev) => ({ ...prev, type: value }))
                  }
                  required
                >
                  <SelectTrigger id="new_type">
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
                <Label htmlFor="new_ingredients">Ingredients (optional)</Label>
                <Input
                  id="new_ingredients"
                  value={newProductData.ingredients}
                  onChange={(e) =>
                    setNewProductData((prev) => ({ ...prev, ingredients: e.target.value }))
                  }
                  placeholder="Comma-separated list"
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="new_notes">Notes (optional)</Label>
                <Textarea
                  id="new_notes"
                  value={newProductData.notes}
                  onChange={(e) =>
                    setNewProductData((prev) => ({ ...prev, notes: e.target.value }))
                  }
                  placeholder="Any additional notes..."
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
                onClick={() => {
                  setShowAddProductDialog(false);
                  setNewProductData({
                    brand: '',
                    name: '',
                    type: '',
                    ingredients: '',
                    notes: '',
                  });
                  setError(null);
                }}
              >
                Cancel
              </Button>
              <Button type="submit">Add Product</Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
}
