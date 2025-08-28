
from app import app, db
from models import Product

def fix_product_prices():
    """Fix existing product prices that might have been incorrectly stored"""
    with app.app_context():
        products = Product.query.all()
        
        for product in products:
            print(f"Checking product: {product.name_en}")
            print(f"  Current price_idr: {product.price_idr}")
            print(f"  Current price_usd: {product.price_usd}")
            
            # If price_idr seems too high (more than 10 million), it might be wrongly calculated
            if product.price_idr and product.price_idr > 10000000:
                print(f"  ⚠ Suspicious high price detected for {product.name_en}")
                
                # Check if price_usd looks more reasonable
                if product.price_usd and product.price_usd < 1000:
                    # Use USD price and convert to IDR
                    correct_price_idr = float(product.price_usd) * 15300
                    print(f"  → Correcting price_idr from {product.price_idr} to {correct_price_idr}")
                    product.price_idr = correct_price_idr
                else:
                    # Ask for manual correction
                    print(f"  → Please manually check and correct the price for {product.name_en}")
            
            # Ensure price_usd is correctly calculated from price_idr
            if product.price_idr:
                correct_price_usd = float(product.price_idr) / 15300
                if abs(float(product.price_usd or 0) - correct_price_usd) > 0.01:
                    print(f"  → Correcting price_usd from {product.price_usd} to {correct_price_usd}")
                    product.price_usd = correct_price_usd
        
        db.session.commit()
        print("✅ Price correction completed!")

if __name__ == '__main__':
    fix_product_prices()
