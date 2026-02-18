"""
Script to populate the database with prepopulated shampoo products
These will be community products (user_id=None) available to all users
"""
import sys
from pathlib import Path

# Add the backend directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import SessionLocal
from app.models.product import Product

# Shampoo data - comprehensive list with duplicates removed
SHAMPOOS = [
    # Head & Shoulders
    {"brand": "Head & Shoulders", "name": "Classic Clean Dandruff Defense Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Head & Shoulders", "name": "Smooth & Silky Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Head & Shoulders", "name": "Clinical Strength Dandruff Defense Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Head & Shoulders", "name": "Itchy Scalp Care Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Head & Shoulders", "name": "Apple Fresh Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Head & Shoulders", "name": "Tea Tree Oil Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Head & Shoulders", "name": "Deep Moisture Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Head & Shoulders", "name": "Old Spice Pure Sport 2-in-1 Shampoo", "type": "shampoo", "ingredients": None},
    
    # Pantene
    {"brand": "Pantene", "name": "Pro-V Daily Moisture Renewal Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Pantene", "name": "Pro-V Curl Perfection Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Pantene", "name": "Pro-V Smooth & Sleek Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Pantene", "name": "Pro-V Repair & Protect Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Pantene", "name": "Pro-V Sheer Volume Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Pantene", "name": "Pro-V Nutrient Blends Rose Water Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Pantene", "name": "Pro-V Miracle Rescue Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Pantene", "name": "Pro-V Gold Series Moisture Boost Shampoo", "type": "shampoo", "ingredients": None},
    
    # TRESemmé
    {"brand": "TRESemmé", "name": "Moisture Rich Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "TRESemmé", "name": "Keratin Smooth Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "TRESemmé", "name": "Curl Hydrate Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "TRESemmé", "name": "Deep Cleanse Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "TRESemmé", "name": "Color Revitalize Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "TRESemmé", "name": "Rich Moisture Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "TRESemmé", "name": "Pro Pure Micellar Moisture Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "TRESemmé", "name": "Pro Collection Repair & Protect 7 Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Tresemmé Botanique", "name": "Coconut Nourish Shampoo", "type": "shampoo", "ingredients": None},
    
    # As I Am
    {"brand": "As I Am", "name": "Curl Clarity Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "As I Am", "name": "Dry & Itchy Scalp Care Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "As I Am", "name": "Long & Luxe Strengthening Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "As I Am", "name": "Jamaican Black Castor Oil Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "As I Am", "name": "Olive & Tea Tree Oil Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "As I Am", "name": "Coconut CoWash Cleansing Conditioner", "type": "shampoo", "ingredients": None},
    
    # Not Your Mother's
    {"brand": "Not Your Mother's", "name": "Curl Talk Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Not Your Mother's", "name": "Tahitian Gardenia Flower & Mango Butter Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Not Your Mother's", "name": "Blue Sea Kale & Pure Coconut Water Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Not Your Mother's", "name": "Matcha Green Tea & Wild Apple Blossom Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Not Your Mother's", "name": "Plump For Joy Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Not Your Mother's", "name": "Way To Grow Long & Strong Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Not Your Mother's", "name": "Naturals Royal Honey & Kalahari Desert Melon Shampoo", "type": "shampoo", "ingredients": None},
    
    # Rizos Curls
    {"brand": "Rizos Curls", "name": "Hydrating Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Rizos Curls", "name": "Deep Clean Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Rizos Curls", "name": "Scalp Relief Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Rizos Curls", "name": "Nourish & Shine Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Rizos Curls", "name": "Strengthening Shampoo", "type": "shampoo", "ingredients": None},
    
    # Curlsmith
    {"brand": "Curlsmith", "name": "Core Strength Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Curlsmith", "name": "Vivid Tones Vibrancy Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Curlsmith", "name": "Essential Moisture Cleanser", "type": "shampoo", "ingredients": None},
    {"brand": "Curlsmith", "name": "Shine Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Curlsmith", "name": "Wash & Scrub Detox Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Curlsmith", "name": "Frizz Control Cleanser", "type": "shampoo", "ingredients": None},
    
    # Mielle
    {"brand": "Mielle", "name": "Pomegranate & Honey Moisturizing and Detangling Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Mielle", "name": "Rosemary Mint Strengthening Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Mielle", "name": "Babassu Conditioning Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Mielle", "name": "Sea Moss Anti-Shedding Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Mielle", "name": "Mongongo Oil Exfoliating Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Mielle", "name": "White Peony Leave-In Conditioner Cleanser Shampoo", "type": "shampoo", "ingredients": None},
    
    # SheaMoisture
    {"brand": "SheaMoisture", "name": "Coconut & Hibiscus Curl & Shine Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "SheaMoisture", "name": "Jamaican Black Castor Oil Strengthen & Restore Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "SheaMoisture", "name": "Manuka Honey & Mafura Oil Intensive Hydration Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "SheaMoisture", "name": "African Black Soap Deep Cleansing Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "SheaMoisture", "name": "Low Porosity Protein-Free Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "SheaMoisture", "name": "Raw Shea Butter Moisture Retention Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "SheaMoisture", "name": "Green Coconut & Activated Charcoal Purifying Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "SheaMoisture", "name": "Sugarcane Extract & Meadowfoam Seed Silicone Free Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "SheaMoisture", "name": "Red Palm Oil & Cocoa Butter Shampoo", "type": "shampoo", "ingredients": None},
    
    # Redken
    {"brand": "Redken", "name": "All Soft Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Redken", "name": "Extreme Length Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Redken", "name": "Color Extend Magnetics Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Redken", "name": "Acidic Bonding Concentrate Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Redken", "name": "Volume Injection Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Redken", "name": "Frizz Dismiss Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Redken", "name": "Curvaceous High Foam Shampoo", "type": "shampoo", "ingredients": None},
    
    # OGX
    {"brand": "OGX", "name": "Coconut Milk Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "OGX", "name": "Argan Oil of Morocco Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "OGX", "name": "Tea Tree Mint Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "OGX", "name": "Biotin & Collagen Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "OGX", "name": "Hydrate & Repair Argan Oil Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "OGX", "name": "Shea Soft & Smooth Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "OGX", "name": "Apple Cider Vinegar Shampoo", "type": "shampoo", "ingredients": None},
    
    # Aussie
    {"brand": "Aussie", "name": "Miracle Curls Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Aussie", "name": "Total Miracle Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Aussie", "name": "Volume Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Aussie", "name": "Repair Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Aussie", "name": "Moist Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Aussie", "name": "Head Strong Volume Shampoo", "type": "shampoo", "ingredients": None},
    
    # Cantu
    {"brand": "Cantu", "name": "Sulfate-Free Cleansing Cream Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Cantu", "name": "Shea Butter for Natural Hair Cleansing Cream Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Cantu", "name": "Shea Butter Cleansing Cream Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Cantu", "name": "Guava & Ginger Anti-Dandruff Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Cantu", "name": "TXTR Apple Cider Vinegar Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Cantu", "name": "Hydrating Cream Shampoo", "type": "shampoo", "ingredients": None},
    
    # Briogeo
    {"brand": "Briogeo", "name": "Don't Despair Repair Super Moisture Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Briogeo", "name": "Curl Charisma Rice Amino & Avocado Hydrating Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Briogeo", "name": "Scalp Revival Charcoal + Coconut Oil Micro-Exfoliating Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Briogeo", "name": "Superfoods Mango + Cherry Balancing Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Briogeo", "name": "Be Gentle Be Kind Aloe + Oat Milk Shampoo", "type": "shampoo", "ingredients": None},
    
    # Camille Rose
    {"brand": "Camille Rose", "name": "Sweet Ginger Cleansing Rinse", "type": "shampoo", "ingredients": None},
    {"brand": "Camille Rose", "name": "Coconut Water Curl Cleanse", "type": "shampoo", "ingredients": None},
    {"brand": "Camille Rose", "name": "Herbal Tea Seal & Soften Shampoo", "type": "shampoo", "ingredients": None},
    
    # Amika
    {"brand": "Amika", "name": "Normcore Signature Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Amika", "name": "The Kure Bond Repair Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Amika", "name": "Bust Your Brass Cool Blonde Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Amika", "name": "Hydro Rush Intense Moisture Shampoo", "type": "shampoo", "ingredients": None},
    
    # Oribe
    {"brand": "Oribe", "name": "Gold Lust Repair & Restore Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Oribe", "name": "Signature Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Oribe", "name": "Shampoo for Moisture & Control", "type": "shampoo", "ingredients": None},
    {"brand": "Oribe", "name": "Serene Scalp Anti-Dandruff Shampoo", "type": "shampoo", "ingredients": None},
    
    # Bumble and Bumble
    {"brand": "Bumble and Bumble", "name": "Hairdresser's Invisible Oil Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Bumble and Bumble", "name": "Curl Moisturizing Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Bumble and Bumble", "name": "Sunday Clarifying Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Bumble and Bumble", "name": "Thickening Volume Shampoo", "type": "shampoo", "ingredients": None},
    
    # Verb
    {"brand": "Verb", "name": "Ghost Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Verb", "name": "Curl Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Verb", "name": "Hydrating Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Verb", "name": "Reset Clarifying Shampoo", "type": "shampoo", "ingredients": None},
    
    # Kristin Ess
    {"brand": "Kristin Ess", "name": "The One Signature Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Kristin Ess", "name": "Extra Gentle Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Kristin Ess", "name": "Deep Clean Clarifying Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Kristin Ess", "name": "Curl Shampoo", "type": "shampoo", "ingredients": None},
    
    # Function of Beauty
    {"brand": "Function of Beauty", "name": "Custom Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Function of Beauty", "name": "Pro Custom Recovery Shampoo", "type": "shampoo", "ingredients": None},
    
    # Monday Haircare
    {"brand": "Monday Haircare", "name": "Moisture Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Monday Haircare", "name": "Smooth Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Monday Haircare", "name": "Volume Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Monday Haircare", "name": "Repair Shampoo", "type": "shampoo", "ingredients": None},
    
    # Native
    {"brand": "Native", "name": "Moisturizing Shampoo Coconut & Vanilla", "type": "shampoo", "ingredients": None},
    {"brand": "Native", "name": "Almond & Shea Butter Strengthening Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Native", "name": "Cucumber & Mint Volumizing Shampoo", "type": "shampoo", "ingredients": None},
    
    # The Mane Choice
    {"brand": "The Mane Choice", "name": "Easy On The Curls Detangling Hydration Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "The Mane Choice", "name": "Peach Black Tea Vitamin Fusion Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "The Mane Choice", "name": "Ancient Egyptian Anti-Breakage Shampoo", "type": "shampoo", "ingredients": None},
    
    # Kinky-Curly
    {"brand": "Kinky-Curly", "name": "Come Clean Natural Moisturizing Shampoo", "type": "shampoo", "ingredients": None},
    
    # Aunt Jackie's
    {"brand": "Aunt Jackie's", "name": "Oh So Clean Moisturizing & Softening Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Aunt Jackie's", "name": "Power Wash Intense Moisture Clarifying Shampoo", "type": "shampoo", "ingredients": None},
    
    # Eden BodyWorks
    {"brand": "Eden BodyWorks", "name": "Peppermint Tea Tree Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Eden BodyWorks", "name": "Coconut Shea Cleansing CoWash", "type": "shampoo", "ingredients": None},
    
    # Jane Carter Solution
    {"brand": "Jane Carter Solution", "name": "Moisture Nourishing Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Jane Carter Solution", "name": "Dandruff Control Shampoo", "type": "shampoo", "ingredients": None},
    
    # Alikay Naturals
    {"brand": "Alikay Naturals", "name": "Moist Black Soap Revitalizing Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Alikay Naturals", "name": "Essential 17 Hair Growth Shampoo", "type": "shampoo", "ingredients": None},
    
    # Innersense
    {"brand": "Innersense", "name": "Pure Harmony Hairbath", "type": "shampoo", "ingredients": None},
    {"brand": "Innersense", "name": "Hydrating Cream Hairbath", "type": "shampoo", "ingredients": None},
    {"brand": "Innersense", "name": "Color Awakening Hairbath", "type": "shampoo", "ingredients": None},
    
    # R+Co
    {"brand": "R+Co", "name": "Atlantis Moisturizing Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "R+Co", "name": "Dallas Thickening Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "R+Co", "name": "Oblivion Clarifying Shampoo", "type": "shampoo", "ingredients": None},
    
    # IGK
    {"brand": "IGK", "name": "Good Behavior Spirulina Protein Smoothing Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "IGK", "name": "Extra Love Volume & Thickening Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "IGK", "name": "Legendary Dream Hair Shampoo", "type": "shampoo", "ingredients": None},
    
    # Maui Moisture
    {"brand": "Maui Moisture", "name": "Heal & Hydrate Shea Butter Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Maui Moisture", "name": "Curl Quench + Coconut Oil Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Maui Moisture", "name": "Thicken & Restore Bamboo Fibers Shampoo", "type": "shampoo", "ingredients": None},
    
    # Pacifica
    {"brand": "Pacifica", "name": "Pineapple Curls Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Pacifica", "name": "Coconut Power Strong & Long Shampoo", "type": "shampoo", "ingredients": None},
    
    # Acure
    {"brand": "Acure", "name": "Curiously Clarifying Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Acure", "name": "Vivacious Volume Shampoo", "type": "shampoo", "ingredients": None},
    
    # Giovanni
    {"brand": "Giovanni", "name": "Smooth As Silk Deep Moisture Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Giovanni", "name": "Tea Tree Triple Treat Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Giovanni", "name": "2chic Ultra-Moist Shampoo", "type": "shampoo", "ingredients": None},
    
    # Herbal Essences
    {"brand": "Herbal Essences", "name": "Hello Hydration Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Herbal Essences", "name": "Bio:Renew Argan Oil of Morocco Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Herbal Essences", "name": "Curl Define Shampoo", "type": "shampoo", "ingredients": None},
    
    # Suave
    {"brand": "Suave", "name": "Professionals Almond & Shea Butter Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Suave", "name": "Daily Clarifying Shampoo", "type": "shampoo", "ingredients": None},
    
    # Nexxus
    {"brand": "Nexxus", "name": "Humectress Ultimate Moisture Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Nexxus", "name": "Therappe Ultimate Moisture Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Nexxus", "name": "Keraphix Damage Healing Shampoo", "type": "shampoo", "ingredients": None},
    
    # Dove
    {"brand": "Dove", "name": "Intensive Repair Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Dove", "name": "Amplified Textures Hydrating Cleanse Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Dove", "name": "Daily Moisture Shampoo", "type": "shampoo", "ingredients": None},
    
    # Biolage
    {"brand": "Biolage", "name": "HydraSource Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Biolage", "name": "VolumeBloom Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Biolage", "name": "Strength Recovery Shampoo", "type": "shampoo", "ingredients": None},
    
    # Kenra
    {"brand": "Kenra", "name": "Moisturizing Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Kenra", "name": "Clarifying Shampoo", "type": "shampoo", "ingredients": None},
    
    # Sexy Hair
    {"brand": "Sexy Hair", "name": "Healthy Sexy Hair Moisturizing Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Sexy Hair", "name": "Curly Sexy Hair Shampoo", "type": "shampoo", "ingredients": None},
    
    # Ouai
    {"brand": "Ouai", "name": "Fine Hair Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Ouai", "name": "Thick Hair Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Ouai", "name": "Detox Shampoo", "type": "shampoo", "ingredients": None},
    
    # Shu Uemura
    {"brand": "Shu Uemura", "name": "Ultimate Reset Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Shu Uemura", "name": "Urban Moisture Shampoo", "type": "shampoo", "ingredients": None},
    
    # Philip Kingsley
    {"brand": "Philip Kingsley", "name": "Elasticizer Booster Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Philip Kingsley", "name": "Moisture Balancing Shampoo", "type": "shampoo", "ingredients": None},
    
    # Drunk Elephant
    {"brand": "Drunk Elephant", "name": "Cocomino Glossing Shampoo", "type": "shampoo", "ingredients": None},
    
    # Ceremonia
    {"brand": "Ceremonia", "name": "Guava Hydrating Shampoo", "type": "shampoo", "ingredients": None},
    
    # Bondi Boost
    {"brand": "Bondi Boost", "name": "HG Shampoo for Hair Growth", "type": "shampoo", "ingredients": None},
    
    # K18
    {"brand": "K18", "name": "Peptide Prep pH Maintenance Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "K18", "name": "Peptide Prep Detox Shampoo", "type": "shampoo", "ingredients": None},
    
    # Act+Acre
    {"brand": "Act+Acre", "name": "Cold Processed Hair Cleanse", "type": "shampoo", "ingredients": None},
    
    # DevaCurl
    {"brand": "DevaCurl", "name": "No-Poo Original Cleanser", "type": "shampoo", "ingredients": None},
    {"brand": "DevaCurl", "name": "Low-Poo Delight Cleanser", "type": "shampoo", "ingredients": None},
    {"brand": "DevaCurl", "name": "Low-Poo Original Cleanser", "type": "shampoo", "ingredients": None},
    {"brand": "DevaCurl", "name": "Buildup Buster Micellar Water Cleansing Serum", "type": "shampoo", "ingredients": None},
    
    # Ouidad
    {"brand": "Ouidad", "name": "Advanced Climate Control Defrizzing Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Ouidad", "name": "Curl Quencher Moisturizing Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Ouidad", "name": "Water Works Clarifying Shampoo", "type": "shampoo", "ingredients": None},
    
    # Olaplex
    {"brand": "Olaplex", "name": "No. 4 Bond Maintenance Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Olaplex", "name": "No. 4C Bond Maintenance Clarifying Shampoo", "type": "shampoo", "ingredients": None},
    
    # Kérastase
    {"brand": "Kérastase", "name": "Bain Satin Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Kérastase", "name": "Curl Manifesto Bain Hydratation Douceur Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Kérastase", "name": "Bain Lumiere Blond Absolu Shampoo", "type": "shampoo", "ingredients": None},
    
    # Pureology
    {"brand": "Pureology", "name": "Hydrate Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Pureology", "name": "Strength Cure Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Pureology", "name": "Nanoworks Gold Shampoo", "type": "shampoo", "ingredients": None},
    
    # Living Proof
    {"brand": "Living Proof", "name": "Perfect Hair Day Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Living Proof", "name": "Curl Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Living Proof", "name": "Restore Shampoo", "type": "shampoo", "ingredients": None},
    
    # Matrix
    {"brand": "Matrix", "name": "A Curl Can Dream Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Matrix", "name": "Total Results Mega Sleek Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Matrix", "name": "Total Results So Silver Shampoo", "type": "shampoo", "ingredients": None},
    
    # Moroccanoil
    {"brand": "Moroccanoil", "name": "Hydrating Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Moroccanoil", "name": "Curl Enhancing Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Moroccanoil", "name": "Clarifying Shampoo", "type": "shampoo", "ingredients": None},
    
    # Carol's Daughter
    {"brand": "Carol's Daughter", "name": "Wash Day Delight Water-to-Foam Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Carol's Daughter", "name": "Black Vanilla Moisture & Shine Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Carol's Daughter", "name": "Goddess Strength Fortifying Shampoo", "type": "shampoo", "ingredients": None},
    
    # Pattern
    {"brand": "Pattern", "name": "Hydration Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Pattern", "name": "Clarifying Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Pattern", "name": "Palo Santo Leave-In Conditioner Cleanser Shampoo", "type": "shampoo", "ingredients": None},
    
    # Design Essentials
    {"brand": "Design Essentials", "name": "Oat Protein & Henna Deep Cleansing Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Design Essentials", "name": "Almond & Avocado Moisturizing & Detangling Shampoo", "type": "shampoo", "ingredients": None},
    
    # L'Oréal
    {"brand": "L'Oréal EverPure", "name": "Moisture Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "L'Oréal EverPure", "name": "Bond Strengthening Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "L'Oréal Elvive", "name": "Total Repair 5 Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "L'Oréal Elvive", "name": "Dream Lengths Shampoo", "type": "shampoo", "ingredients": None},
    
    # Garnier Fructis
    {"brand": "Garnier Fructis", "name": "Curl Nourish Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Garnier Fructis", "name": "Damage Repairing Treat Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Garnier Fructis", "name": "Pure Clean Shampoo", "type": "shampoo", "ingredients": None},
    
    # Aveda
    {"brand": "Aveda", "name": "Be Curly Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Aveda", "name": "Nutriplenish Light Moisture Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Aveda", "name": "Shampure Nurturing Shampoo", "type": "shampoo", "ingredients": None},
    
    # Paul Mitchell
    {"brand": "Paul Mitchell", "name": "Tea Tree Special Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Paul Mitchell", "name": "Awapuhi Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Paul Mitchell", "name": "Extra-Body Shampoo", "type": "shampoo", "ingredients": None},
    
    # CHI
    {"brand": "CHI", "name": "Infra Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "CHI", "name": "Keratin Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "CHI", "name": "Aloe Vera Curl Enhancing Shampoo", "type": "shampoo", "ingredients": None},
    
    # Joico
    {"brand": "Joico", "name": "Moisture Recovery Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Joico", "name": "K-PAK Reconstructing Shampoo", "type": "shampoo", "ingredients": None},
    {"brand": "Joico", "name": "Curls Like Us Shampoo", "type": "shampoo", "ingredients": None},
]


def populate_shampoos():
    """Populate the database with prepopulated shampoo products"""
    db = SessionLocal()
    
    try:
        added_count = 0
        skipped_count = 0
        
        for shampoo_data in SHAMPOOS:
            # Check if product already exists (case-insensitive)
            existing = db.query(Product).filter(
                Product.brand.ilike(shampoo_data["brand"].strip()),
                Product.name.ilike(shampoo_data["name"].strip()),
                Product.type == shampoo_data["type"]
            ).first()
            
            if existing:
                print(f"⏭️  Skipped (already exists): {shampoo_data['brand']} - {shampoo_data['name']}")
                skipped_count += 1
                continue
            
            # Create new product as community product (user_id=None)
            product = Product(
                brand=shampoo_data["brand"].strip(),
                name=shampoo_data["name"].strip(),
                type=shampoo_data["type"],
                ingredients=shampoo_data["ingredients"],
                user_id=None,  # Community product available to all users
                usage_count=0,
                success_rate=0.0,
                is_starred=False
            )
            
            db.add(product)
            added_count += 1
            print(f"✅ Added: {shampoo_data['brand']} - {shampoo_data['name']}")
        
        db.commit()
        
        print(f"\n📊 Summary:")
        print(f"   ✅ Added: {added_count} products")
        print(f"   ⏭️  Skipped: {skipped_count} products (already exist)")
        print(f"   📦 Total: {len(SHAMPOOS)} products")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Starting shampoo population...\n")
    populate_shampoos()
    print("\n✨ Done!")
