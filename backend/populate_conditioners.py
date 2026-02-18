"""
Script to populate the database with prepopulated conditioner products
These will be community products (user_id=None) available to all users
"""
import sys
from pathlib import Path

# Add the backend directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import SessionLocal
from app.models.product import Product

# Conditioner data - comprehensive list with duplicates removed
CONDITIONERS = [
    # Redken
    {"brand": "Redken", "name": "All Soft Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Redken", "name": "Extreme Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Redken", "name": "Extreme Length Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Redken", "name": "Color Extend Magnetics Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Redken", "name": "Acidic Bonding Concentrate Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Redken", "name": "Frizz Dismiss Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Redken", "name": "Volume Injection Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Redken", "name": "Curvaceous Conditioner", "type": "conditioner", "ingredients": None},
    
    # Olaplex
    {"brand": "Olaplex", "name": "No. 5 Bond Maintenance Conditioner", "type": "conditioner", "ingredients": None},
    
    # Pureology
    {"brand": "Pureology", "name": "Hydrate Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Pureology", "name": "Strength Cure Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Pureology", "name": "Nanoworks Gold Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Pureology", "name": "Color Fanatic Conditioner", "type": "conditioner", "ingredients": None},
    
    # Kérastase
    {"brand": "Kérastase", "name": "Fondant Fluidealiste Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Kérastase", "name": "Curl Manifesto Fondant Hydratation Essentielle Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Kérastase", "name": "Fondant Renforcateur Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Kérastase", "name": "Fondant Cica Chroma Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Kérastase", "name": "Fondant Extentioniste Conditioner", "type": "conditioner", "ingredients": None},
    
    # Matrix
    {"brand": "Matrix", "name": "A Curl Can Dream Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Matrix", "name": "Total Results Mega Sleek Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Matrix", "name": "Total Results So Silver Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Matrix", "name": "HydraSource Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Matrix", "name": "Instacure Conditioner", "type": "conditioner", "ingredients": None},
    
    # Paul Mitchell
    {"brand": "Paul Mitchell", "name": "The Detangler Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Paul Mitchell", "name": "Super Skinny Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Paul Mitchell", "name": "Tea Tree Special Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Paul Mitchell", "name": "Extra-Body Conditioner", "type": "conditioner", "ingredients": None},
    
    # Joico
    {"brand": "Joico", "name": "Moisture Recovery Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Joico", "name": "K-PAK Reconstructing Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Joico", "name": "Curls Like Us Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Joico", "name": "Blonde Life Conditioner", "type": "conditioner", "ingredients": None},
    
    # Biolage
    {"brand": "Biolage", "name": "HydraSource Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Biolage", "name": "VolumeBloom Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Biolage", "name": "Strength Recovery Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Biolage", "name": "ColorLast Conditioner", "type": "conditioner", "ingredients": None},
    
    # Living Proof
    {"brand": "Living Proof", "name": "Perfect Hair Day Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Living Proof", "name": "Restore Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Living Proof", "name": "Curl Conditioner", "type": "conditioner", "ingredients": None},
    
    # Bumble and Bumble
    {"brand": "Bumble and Bumble", "name": "Hairdresser's Invisible Oil Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Bumble and Bumble", "name": "Curl Moisturizing Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Bumble and Bumble", "name": "Thickening Volume Conditioner", "type": "conditioner", "ingredients": None},
    
    # Oribe
    {"brand": "Oribe", "name": "Gold Lust Repair & Restore Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Oribe", "name": "Signature Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Oribe", "name": "Conditioner for Moisture & Control", "type": "conditioner", "ingredients": None},
    
    # Amika
    {"brand": "Amika", "name": "Normcore Signature Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Amika", "name": "The Kure Bond Repair Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Amika", "name": "Hydro Rush Intense Moisture Conditioner", "type": "conditioner", "ingredients": None},
    
    # Ouai
    {"brand": "Ouai", "name": "Fine Hair Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Ouai", "name": "Thick Hair Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Ouai", "name": "Medium Hair Conditioner", "type": "conditioner", "ingredients": None},
    
    # Verb
    {"brand": "Verb", "name": "Ghost Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Verb", "name": "Curl Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Verb", "name": "Hydrating Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Verb", "name": "Volume Conditioner", "type": "conditioner", "ingredients": None},
    
    # IGK
    {"brand": "IGK", "name": "Good Behavior Spirulina Protein Smoothing Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "IGK", "name": "Extra Love Volume & Thickening Conditioner", "type": "conditioner", "ingredients": None},
    
    # R+Co
    {"brand": "R+Co", "name": "Atlantis Moisturizing Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "R+Co", "name": "Dallas Thickening Conditioner", "type": "conditioner", "ingredients": None},
    
    # Nexxus
    {"brand": "Nexxus", "name": "Humectress Ultimate Moisture Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Nexxus", "name": "Therappe Ultimate Moisture Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Nexxus", "name": "Keraphix Damage Healing Conditioner", "type": "conditioner", "ingredients": None},
    
    # SheaMoisture
    {"brand": "SheaMoisture", "name": "Coconut & Hibiscus Curl & Shine Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "SheaMoisture", "name": "Jamaican Black Castor Oil Strengthen & Restore Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "SheaMoisture", "name": "Manuka Honey & Mafura Oil Intensive Hydration Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "SheaMoisture", "name": "Raw Shea Butter Moisture Retention Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "SheaMoisture", "name": "Low Porosity Protein-Free Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "SheaMoisture", "name": "Red Palm Oil & Cocoa Butter Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "SheaMoisture", "name": "Sugarcane Extract & Meadowfoam Seed Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "SheaMoisture", "name": "African Black Soap Balancing Conditioner", "type": "conditioner", "ingredients": None},
    
    # Mielle
    {"brand": "Mielle", "name": "Pomegranate & Honey Moisturizing Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Mielle", "name": "Rosemary Mint Strengthening Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Mielle", "name": "Babassu Oil & Mint Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Mielle", "name": "White Peony Leave-In Conditioner Rinse Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Mielle", "name": "Mongongo Oil Protein-Free Conditioner", "type": "conditioner", "ingredients": None},
    
    # Curlsmith
    {"brand": "Curlsmith", "name": "Glow Perfecting Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Curlsmith", "name": "Multi-Tasking Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Curlsmith", "name": "Essential Moisture Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Curlsmith", "name": "Frizz Control Duo Conditioner", "type": "conditioner", "ingredients": None},
    
    # DevaCurl
    {"brand": "DevaCurl", "name": "One Condition Original Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "DevaCurl", "name": "One Condition Delight Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "DevaCurl", "name": "One Condition Decadence Conditioner", "type": "conditioner", "ingredients": None},
    
    # Ouidad
    {"brand": "Ouidad", "name": "Curl Quencher Moisturizing Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Ouidad", "name": "Advanced Climate Control Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Ouidad", "name": "Moisture Lock Leave-In Conditioner Rinse Conditioner", "type": "conditioner", "ingredients": None},
    
    # Pattern
    {"brand": "Pattern", "name": "Medium Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Pattern", "name": "Heavy Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Pattern", "name": "Light Conditioner", "type": "conditioner", "ingredients": None},
    
    # Camille Rose
    {"brand": "Camille Rose", "name": "Moroccan Pear Conditioning Custard", "type": "conditioner", "ingredients": None},
    {"brand": "Camille Rose", "name": "Coconut Water Conditioner", "type": "conditioner", "ingredients": None},
    
    # Kinky-Curly
    {"brand": "Kinky-Curly", "name": "Knot Today Rinse Conditioner", "type": "conditioner", "ingredients": None},
    
    # Pantene
    {"brand": "Pantene", "name": "Pro-V Daily Moisture Renewal Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Pantene", "name": "Pro-V Smooth & Sleek Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Pantene", "name": "Pro-V Repair & Protect Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Pantene", "name": "Pro-V Sheer Volume Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Pantene", "name": "Pro-V Curl Perfection Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Pantene", "name": "Pro-V Gold Series Moisture Boost Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Pantene", "name": "Pro-V Nutrient Blends Rose Water Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Pantene", "name": "Pro-V Nutrient Blends Bamboo Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Pantene", "name": "Pro-V Miracle Rescue Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Pantene", "name": "Pro-V Blends Sulfate Free Conditioner", "type": "conditioner", "ingredients": None},
    
    # TRESemmé
    {"brand": "TRESemmé", "name": "Moisture Rich Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "TRESemmé", "name": "Keratin Smooth Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "TRESemmé", "name": "Curl Hydrate Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "TRESemmé", "name": "Color Revitalize Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "TRESemmé", "name": "Rich Moisture Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "TRESemmé", "name": "Pro Pure Micellar Moisture Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "TRESemmé", "name": "Pro Collection Repair & Protect 7 Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "TRESemmé", "name": "Flawless Curls Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "TRESemmé", "name": "Climate Protection Conditioner", "type": "conditioner", "ingredients": None},
    
    # Head & Shoulders
    {"brand": "Head & Shoulders", "name": "Classic Clean Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Head & Shoulders", "name": "Smooth & Silky Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Head & Shoulders", "name": "Deep Moisture Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Head & Shoulders", "name": "Apple Fresh Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Head & Shoulders", "name": "Shea Butter Conditioner", "type": "conditioner", "ingredients": None},
    
    # Herbal Essences
    {"brand": "Herbal Essences", "name": "Hello Hydration Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Herbal Essences", "name": "Bio:Renew Argan Oil of Morocco Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Herbal Essences", "name": "Curl Define Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Herbal Essences", "name": "Bio:Renew Coconut Milk Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Herbal Essences", "name": "Smooth Collection Conditioner", "type": "conditioner", "ingredients": None},
    
    # Garnier Fructis
    {"brand": "Garnier Fructis", "name": "Curl Nourish Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Garnier Fructis", "name": "Pure Clean Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Garnier Fructis", "name": "Damage Repairing Treat Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Garnier Fructis", "name": "Grow Strong Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Garnier Fructis", "name": "Sleek & Shine Conditioner", "type": "conditioner", "ingredients": None},
    
    # L'Oréal
    {"brand": "L'Oréal Elvive", "name": "Total Repair 5 Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "L'Oréal Elvive", "name": "Dream Lengths Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "L'Oréal Elvive", "name": "Extraordinary Oil Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "L'Oréal Elvive", "name": "Color Vibrancy Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "L'Oréal Elvive", "name": "Bond Repair Conditioner", "type": "conditioner", "ingredients": None},
    
    # Dove
    {"brand": "Dove", "name": "Intensive Repair Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Dove", "name": "Daily Moisture Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Dove", "name": "Amplified Textures Moisture Lock Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Dove", "name": "Nourishing Oil Care Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Dove", "name": "Volume & Fullness Conditioner", "type": "conditioner", "ingredients": None},
    
    # Suave
    {"brand": "Suave", "name": "Professionals Almond & Shea Butter Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Suave", "name": "Daily Clarifying Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Suave", "name": "Keratin Infusion Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Suave", "name": "Avocado & Olive Oil Conditioner", "type": "conditioner", "ingredients": None},
    {"brand": "Suave", "name": "Rosemary & Mint Conditioner", "type": "conditioner", "ingredients": None},
]


def populate_conditioners():
    """Populate the database with prepopulated conditioner products"""
    db = SessionLocal()
    
    try:
        added_count = 0
        skipped_count = 0
        
        for conditioner_data in CONDITIONERS:
            # Check if product already exists (case-insensitive)
            existing = db.query(Product).filter(
                Product.brand.ilike(conditioner_data["brand"].strip()),
                Product.name.ilike(conditioner_data["name"].strip()),
                Product.type == conditioner_data["type"]
            ).first()
            
            if existing:
                print(f"⏭️  Skipped (already exists): {conditioner_data['brand']} - {conditioner_data['name']}")
                skipped_count += 1
                continue
            
            # Create new product as community product (user_id=None)
            product = Product(
                brand=conditioner_data["brand"].strip(),
                name=conditioner_data["name"].strip(),
                type=conditioner_data["type"],
                ingredients=conditioner_data["ingredients"],
                user_id=None,  # Community product available to all users
                usage_count=0,
                success_rate=0.0,
                is_starred=False
            )
            
            db.add(product)
            added_count += 1
            print(f"✅ Added: {conditioner_data['brand']} - {conditioner_data['name']}")
        
        db.commit()
        
        print(f"\n📊 Summary:")
        print(f"   ✅ Added: {added_count} products")
        print(f"   ⏭️  Skipped: {skipped_count} products (already exist)")
        print(f"   📦 Total: {len(CONDITIONERS)} products")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Starting conditioner population...\n")
    populate_conditioners()
    print("\n✨ Done!")
