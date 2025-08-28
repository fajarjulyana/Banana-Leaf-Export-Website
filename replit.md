# Overview

This is a Banana Leaf Export website built with Flask, designed to showcase and sell premium banana leaves for international markets. The application provides a bilingual (English/Indonesian) e-commerce platform with customer-facing product browsing and shopping cart functionality, plus a comprehensive admin panel for managing products, orders, and company settings.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Web Framework
- **Flask** as the core web framework with Blueprint architecture for modular route organization
- **Jinja2** templating engine for dynamic HTML generation with multilingual support
- **Flask-Login** for admin session management and authentication

## Database Layer
- **SQLAlchemy** ORM with Flask-SQLAlchemy integration
- **SQLite** as the default database (configurable via DATABASE_URL environment variable)
- Models include Admin, Category, Product, Order, OrderItem, and CompanySettings
- Automatic table creation on application startup

## Frontend Architecture
- **Bootstrap 5** for responsive UI components and styling
- **Font Awesome** for iconography
- Custom CSS for branding and enhanced user experience
- Vanilla JavaScript for interactive features (cart management, form validation, tooltips)

## Authentication & Authorization
- Hash-based password storage using Werkzeug security utilities
- Session-based admin authentication with login/logout functionality
- Protected admin routes using Flask-Login decorators

## Internationalization
- Bilingual support (English/Indonesian) with session-based language switching
- Language-specific content stored in database models (name_en/name_id, description_en/description_id)
- URL parameter and session persistence for language preferences

## Application Structure
- **Modular routing** with separate blueprints for customer and admin functionality
- **Template inheritance** using base.html for consistent layout across pages
- **Static asset organization** with dedicated CSS and JavaScript files

# External Dependencies

## Core Framework Dependencies
- Flask web framework
- Flask-SQLAlchemy for database ORM
- Flask-Login for authentication management
- Werkzeug for password hashing and WSGI utilities

## Frontend Libraries
- Bootstrap 5 (via CDN) for responsive design
- Font Awesome 6 (via CDN) for icons
- Custom CSS and JavaScript for enhanced functionality

## Database
- SQLite as default database engine
- Configurable database URL via environment variables
- Connection pooling and ping configuration for reliability

## Production Considerations
- ProxyFix middleware for deployment behind reverse proxies
- Environment-based configuration for database and session secrets
- Logging configuration for debugging and monitoring