
# Agricultural Export E-Commerce Platform

A bilingual (English/Indonesian) e-commerce platform built with Flask for selling premium agricultural products, specifically designed for international banana leaf exports and other agricultural commodities.

## Features

### Customer Features
- **Bilingual Support**: Automatic language detection with manual switching between English and Indonesian
- **Multi-Currency**: Support for USD and IDR with automatic currency conversion
- **Product Catalog**: Browse products by categories with search functionality
- **Shopping Cart**: Add, update, and remove products with quantity management
- **Checkout Process**: Simple customer registration and order placement
- **Responsive Design**: Mobile-friendly interface using Bootstrap 5

### Admin Features
- **Dashboard**: Overview of orders, products, and revenue statistics
- **Product Management**: Add, edit, delete, and manage product inventory
- **Order Management**: View, update order status, and manage customer orders
- **Shipping Tracking**: Track shipments with multiple carriers (JNE, TIKI, DHL, FedEx, etc.)
- **Company Settings**: Manage company information and contact details
- **Multi-language Content**: Manage content in both English and Indonesian

## Technology Stack

### Backend
- **Flask**: Python web framework
- **SQLAlchemy**: Database ORM with Flask-SQLAlchemy integration
- **Flask-Login**: User authentication and session management
- **Werkzeug**: Password hashing and security utilities
- **SQLite**: Default database (configurable to PostgreSQL)

### Frontend
- **Bootstrap 5**: Responsive CSS framework
- **Font Awesome 6**: Icon library
- **Jinja2**: Template engine with bilingual support
- **Vanilla JavaScript**: Client-side interactivity

## Installation & Setup

### Prerequisites
- Python 3.11+
- Git

### Quick Start on Replit
1. Fork this repository on Replit
2. The application will auto-install dependencies
3. Click the "Run" button to start the server
4. Access the application at the provided URL

### Local Development
```bash
# Clone the repository
git clone <repository-url>
cd banana-export-website

# Install dependencies
pip install -r requirements.txt

# Initialize the database
python init_new_db.py

# Run the application
python main.py
```

## Configuration

### Environment Variables
- `DATABASE_URL`: Database connection string (default: SQLite)
- `SESSION_SECRET`: Secret key for session management

### Default Admin Credentials
- **Username**: `admin`
- **Password**: `admin123`

## Database Schema

### Core Models
- **Admin**: Administrative user accounts
- **Category**: Product categories with bilingual names
- **Product**: Products with multi-currency pricing and bilingual descriptions
- **Order**: Customer orders with shipping tracking
- **OrderItem**: Individual items within orders
- **CompanySettings**: Configurable company information

### Key Features
- Bilingual content storage (English/Indonesian)
- Multi-currency support (USD/IDR)
- Comprehensive shipping tracking
- Automatic timestamp management

## API Endpoints

### Customer Routes
- `GET /` - Homepage with featured products
- `GET /products` - Product catalog with filtering
- `GET /product/<id>` - Product detail page
- `POST /add_to_cart` - Add product to shopping cart
- `GET /cart` - Shopping cart management
- `GET /checkout` - Checkout process
- `POST /place_order` - Submit order

### Admin Routes
- `GET /admin` - Admin dashboard
- `GET /admin/login` - Admin login
- `GET /admin/products` - Product management
- `GET /admin/orders` - Order management
- `GET /admin/shipping` - Shipping tracking
- `GET /admin/settings` - Company settings

## Shipping Integration

### Supported Carriers
- **Domestic (Indonesia)**: JNE, TIKI, POS Indonesia
- **International**: DHL, FedEx, UPS

### Tracking Features
- Real-time status updates
- Estimated delivery dates
- Shipping cost calculation
- International vs domestic handling

## Internationalization

### Language Support
- **English**: Default for international customers
- **Indonesian**: Automatic detection for Indonesian users

### Auto-Detection Features
- Browser language preferences
- User-Agent analysis
- Geographic IP detection
- Manual language switching

## Deployment on Replit

### Automatic Features
- Environment detection and setup
- Database initialization
- Static file serving
- Port forwarding (5000 → 80/443)

### Production Considerations
- ProxyFix middleware for reverse proxy compatibility
- Session security with environment-based secrets
- Database connection pooling
- Error logging and monitoring

## File Structure

```
├── admin_routes.py      # Admin panel routes and logic
├── app.py              # Flask application configuration
├── main.py             # Application entry point
├── models.py           # Database models and schema
├── routes.py           # Customer-facing routes
├── init_new_db.py      # Database initialization script
├── static/
│   ├── css/style.css   # Custom stylesheets
│   └── js/main.js      # JavaScript functionality
└── templates/          # Jinja2 templates
    ├── admin/          # Admin panel templates
    ├── base.html       # Base template
    └── *.html          # Customer page templates
```

## Contributing

### Development Guidelines
1. Follow Flask best practices
2. Maintain bilingual content support
3. Test both currency modes (USD/IDR)
4. Ensure mobile responsiveness
5. Maintain admin/customer separation

### Adding New Features
1. Update database models if needed
2. Add routes to appropriate blueprint
3. Create bilingual templates
4. Test with different language/currency combinations
5. Update admin panel if applicable

## License

This project is proprietary software for agricultural export businesses.

## Support

For technical support or business inquiries:
- **Email**: Contact admin through the application
- **WhatsApp**: Available in company settings
- **Phone**: Listed in company contact information

---

**Note**: This application is optimized for Replit deployment and agricultural export businesses focusing on Indonesian products for international markets.
