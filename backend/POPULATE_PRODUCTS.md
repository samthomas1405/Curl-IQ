# Populate Prepopulated Products

These scripts populate the database with community products (available to all users).

## Usage

### Shampoos
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python populate_shampoos.py
```

### Conditioners
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python populate_conditioners.py
```

## What it does

- Adds products to the database as community products (`user_id=None`)
- Skips products that already exist (case-insensitive matching)
- All users will see these products in their product list

## Available Scripts

- `populate_shampoos.py` - ~250+ shampoo products from 70+ brands
- `populate_conditioners.py` - ~120+ conditioner products from 40+ brands

## Adding more product types

To add leave-ins, creams, gels, etc., create similar scripts:
- `populate_leave_ins.py`
- `populate_creams.py`
- etc.

Or extend existing scripts to handle multiple product types.

## Notes

- Products are marked as community products (`user_id=None`)
- They appear in all users' product lists
- Users can still create their own products
- The deduplication system will prevent duplicates
