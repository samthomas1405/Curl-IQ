# Product Deduplication System

## Overview

The product deduplication system prevents duplicate products from being created when users add products with similar names or slight spelling differences.

## How It Works

### 1. **Duplicate Detection**
When a user tries to create a product, the system:
- First checks for **exact matches** (case-insensitive)
- Then checks for **similar products** using fuzzy string matching
- Compares both brand and product name
- Uses a similarity threshold of 85%+

### 2. **Similarity Scoring**
- **Brand similarity**: 30% weight
- **Product name similarity**: 70% weight (more important)
- Uses Python's `difflib.SequenceMatcher` for fuzzy matching

### 3. **Actions Based on Similarity**

#### **≥95% Similarity** (Very Similar - Likely Duplicate)
- **Action**: Automatically returns the existing product
- **User Experience**: Product is linked to user, no duplicate created
- **Example**: "As I Am Classic Leave-In" vs "As I Am Classic Leave In"

#### **85-95% Similarity** (Somewhat Similar - Warning)
- **Action**: Returns 409 Conflict with suggestion
- **User Experience**: Frontend can show a warning dialog asking user to confirm
- **Example**: "As I Am Classic Leave-In" vs "As I Am Classic Leave-In Conditioner"

#### **<85% Similarity** (Different Products)
- **Action**: Creates new product normally
- **User Experience**: No interruption

## API Endpoints

### Create Product (with deduplication)
```http
POST /api/v1/products
```

**Query Parameters:**
- `force_create=true` - Force creation even if duplicate found (85-95% similarity)

**Response Codes:**
- `201 Created` - Product created or existing product returned
- `409 Conflict` - Similar product found (85-95% similarity), includes suggestion

**409 Response Example:**
```json
{
  "detail": {
    "message": "Similar product exists: As I Am - Classic Leave-In (90% similar). Continue anyway?",
    "similar_product": {
      "id": 1,
      "brand": "As I Am",
      "name": "Classic Leave-In",
      "type": "leave-in"
    },
    "similarity": 0.9
  }
}
```

### Check for Duplicates (Before Creating)
```http
GET /api/v1/products/check-duplicate?brand=As%20I%20Am&name=Classic%20Leave-In&product_type=leave-in
```

**Response:**
```json
{
  "exists": true,
  "similar_product": {
    "id": 1,
    "brand": "As I Am",
    "name": "Classic Leave-In",
    "type": "leave-in",
    "success_rate": 85.5,
    "usage_count": 12
  },
  "similarity": 0.95,
  "message": "Similar product found: As I Am - Classic Leave-In",
  "action": "suggest_existing"
}
```

## Frontend Integration

### Option 1: Check Before Creating
```javascript
// Check for duplicates before showing create form
const checkDuplicate = async (brand, name, type) => {
  const response = await api.get('/api/v1/products/check-duplicate', {
    params: { brand, name, product_type: type }
  });
  
  if (response.data.exists) {
    if (response.data.similarity >= 0.95) {
      // Show: "This product already exists. Use existing?"
      return { action: 'use_existing', product: response.data.similar_product };
    } else {
      // Show: "Similar product found. Create anyway?"
      return { action: 'warn', product: response.data.similar_product };
    }
  }
  return { action: 'create_new' };
};
```

### Option 2: Handle 409 Conflict
```javascript
try {
  await productsApi.create(productData);
} catch (error) {
  if (error.response?.status === 409) {
    const { similar_product, message } = error.response.data.detail;
    // Show dialog: "Similar product found. Use existing or create new?"
    const useExisting = await showDuplicateDialog(message, similar_product);
    if (useExisting) {
      return similar_product;
    } else {
      // Force create with ?force_create=true
      await productsApi.create(productData, { params: { force_create: true } });
    }
  }
}
```

## Benefits

1. **Prevents Duplicates**: Automatically handles exact and near-exact matches
2. **User-Friendly**: Shows suggestions instead of silently creating duplicates
3. **Flexible**: Allows legitimate similar products (e.g., different sizes)
4. **Community Products**: Can link existing community products to users
5. **Data Quality**: Maintains cleaner database with fewer duplicates

## Configuration

### Adjust Similarity Thresholds

Edit `backend/app/services/product_deduplication.py`:

```python
# In find_similar_product function
threshold: float = 0.85  # Default threshold

# In check_and_suggest_duplicate function
if similarity >= 0.95:  # Auto-return existing
if similarity >= 0.85:  # Warn user
```

### Normalization

The system normalizes text by:
- Converting to lowercase
- Trimming whitespace
- Case-insensitive comparison

## Future Enhancements

1. **Fuzzy Search Library**: Could use `fuzzywuzzy` or `rapidfuzz` for better matching
2. **Brand Normalization**: Handle brand variations (e.g., "As I Am" vs "AsIAm")
3. **Product Merging**: Admin tool to merge confirmed duplicates
4. **Community Product Pool**: Shared product database that all users can access
5. **Ingredient Matching**: Use ingredients to detect duplicates even with different names
