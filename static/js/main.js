// Main JavaScript file for Banana Leaf Export website

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })

    // Auto-hide flash messages
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Gallery-based landscape background system
    initializeLandscapeBackground();
});

// Initialize cart functionality
function initializeCart() {
    // Update cart badge
    updateCartBadge();

    // Add to cart animation
    const addToCartButtons = document.querySelectorAll('button[type="submit"]');
    addToCartButtons.forEach(button => {
        if (button.closest('form[action*="add_to_cart"]')) {
            button.addEventListener('click', function(e) {
                const form = this.closest('form');
                const productId = form.querySelector('input[name="product_id"]').value;
                const quantity = form.querySelector('input[name="quantity"]').value;

                // Add loading state
                this.classList.add('loading');
                this.disabled = true;

                // Submit form after a brief delay for visual feedback
                setTimeout(() => {
                    form.submit();
                }, 500);
            });
        }
    });

    // Quantity input validation
    const quantityInputs = document.querySelectorAll('input[name="quantity"]');
    quantityInputs.forEach(input => {
        input.addEventListener('input', function() {
            const min = parseInt(this.min);
            const max = parseInt(this.max);
            const value = parseInt(this.value);

            if (value < min) {
                this.value = min;
                showToast('Minimum order quantity is ' + min, 'warning');
            }

            if (max && value > max) {
                this.value = max;
                showToast('Maximum available quantity is ' + max, 'warning');
            }

            // Update total price if price display exists
            updatePriceDisplay(this);
        });
    });
}

// Update cart badge count
function updateCartBadge() {
    // This would typically be updated via AJAX
    // For now, it's handled server-side through session
}

// Update price display for quantity changes
function updatePriceDisplay(quantityInput) {
    const productCard = quantityInput.closest('.card, .product-detail');
    if (!productCard) return;

    const priceElement = productCard.querySelector('.unit-price');
    const totalElement = productCard.querySelector('.total-price');

    if (priceElement && totalElement) {
        const unitPrice = parseFloat(priceElement.dataset.price);
        const quantity = parseInt(quantityInput.value);
        const total = unitPrice * quantity;

        totalElement.textContent = '$' + total.toFixed(2);
    }
}

// Form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('form[novalidate]');

    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();

                // Focus first invalid field
                const firstInvalid = form.querySelector(':invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                    showToast('Please fill in all required fields', 'error');
                }
            }

            form.classList.add('was-validated');
        });
    });

    // Real-time validation for specific fields
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value && !isValidEmail(this.value)) {
                this.setCustomValidity('Please enter a valid email address');
                this.classList.add('is-invalid');
            } else {
                this.setCustomValidity('');
                this.classList.remove('is-invalid');
            }
        });
    });

    // Phone number validation
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function() {
            // Allow only numbers, spaces, hyphens, plus signs, and parentheses
            this.value = this.value.replace(/[^+\d\s\-()]/g, '');
        });
    });
}

// Email validation helper
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Image lazy loading
function initializeLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');

    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    observer.unobserve(img);
                }
            });
        });

        images.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback for browsers without IntersectionObserver
        images.forEach(img => {
            img.src = img.dataset.src;
            img.classList.remove('lazy');
        });
    }
}

// Smooth scrolling for anchor links
function initializeSmoothScrolling() {
    const anchors = document.querySelectorAll('a[href^="#"]');

    anchors.forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') return;

            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Admin-specific features
function initializeAdminFeatures() {
    // Auto-refresh order status
    if (window.location.pathname.includes('/admin/orders')) {
        // Check for new orders every 5 minutes
        setInterval(checkNewOrders, 300000);
    }

    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('a[href*="/delete/"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const confirmMessage = this.dataset.confirm || 'Are you sure you want to delete this item?';
            if (!confirm(confirmMessage)) {
                e.preventDefault();
            }
        });
    });

    // Auto-save form drafts
    initializeAutoSave();

    // Initialize data tables if present
    initializeDataTables();
}

// Check for new orders (admin feature)
function checkNewOrders() {
    // Placeholder for checking new orders
    console.log('Checking for new orders...');
}

// Initialize auto-save functionality
function initializeAutoSave() {
    // Placeholder for auto-save initialization
    console.log('Auto-save initialized...');
}

// Initialize data tables for admin
function initializeDataTables() {
    // Placeholder for data table initialization
    console.log('Initializing data tables...');
}


// Check for new orders (admin feature)
function checkNewOrders() {
    fetch('/admin/api/check-orders')
        .then(response => response.json())
        .then(data => {
            if (data.new_orders > 0) {
                showToast(`${data.new_orders} new order(s) received!`, 'info');
                // Update order count in navigation if present
                const orderBadge = document.querySelector('.order-count-badge');
                if (orderBadge) {
                    orderBadge.textContent = data.pending_orders;
                }
            }
        })
        .catch(error => console.log('Error checking orders:', error));
}

// Auto-save functionality
function initializeAutoSave() {
    const forms = document.querySelectorAll('form[data-autosave]');

    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('input', debounce(() => {
                saveFormDraft(form);
            }, 2000));
        });

        // Load saved draft on page load
        loadFormDraft(form);
    });
}

// Save form data to localStorage
function saveFormDraft(form) {
    const formId = form.id || form.action;
    const formData = new FormData(form);
    const data = {};

    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }

    localStorage.setItem(`draft_${formId}`, JSON.stringify(data));
}

// Load form draft from localStorage
function loadFormDraft(form) {
    const formId = form.id || form.action;
    const savedData = localStorage.getItem(`draft_${formId}`);

    if (savedData) {
        const data = JSON.parse(savedData);
        Object.keys(data).forEach(key => {
            const input = form.querySelector(`[name="${key}"]`);
            if (input && !input.value) {
                input.value = data[key];
            }
        });
    }
}

// Initialize data tables for admin
function initializeDataTables() {
    const tables = document.querySelectorAll('.data-table');

    tables.forEach(table => {
        // Add sorting functionality
        const headers = table.querySelectorAll('th[data-sort]');
        headers.forEach(header => {
            header.style.cursor = 'pointer';
            header.addEventListener('click', function() {
                sortTable(table, this.dataset.sort);
            });
        });
    });
}

// Simple table sorting
function sortTable(table, column) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));

    const sortedRows = rows.sort((a, b) => {
        const aText = a.querySelector(`td[data-${column}]`)?.textContent || '';
        const bText = b.querySelector(`td[data-${column}]`)?.textContent || '';

        return aText.localeCompare(bText);
    });

    // Clear tbody and append sorted rows
    tbody.innerHTML = '';
    sortedRows.forEach(row => tbody.appendChild(row));
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Toast notification system
function showToast(message, type = 'info') {
    // Create toast container if it doesn't exist
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '1050';
        document.body.appendChild(toastContainer);
    }

    // Create toast
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;

    toastContainer.appendChild(toast);

    // Initialize and show toast
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();

    // Remove toast element after it's hidden
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

// Initialize landscape background system
function initializeLandscapeBackground() {
    const heroSection = document.querySelector('.hero-section');
    if (!heroSection) return;

    // Get gallery images from data attribute or meta tag
    const galleryImages = getGalleryImages();
    const galleryMode = getGalleryMode();

    if (!galleryImages || galleryImages.length === 0) {
        // Fallback to default landscape for quality_care theme
        if (document.body.getAttribute('data-theme') === 'quality_care') {
            const defaultImage = 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80';
            setHeroBackground(defaultImage);
        }
        return;
    }

    if (galleryMode === 'carousel' && galleryImages.length > 1) {
        // Carousel mode - rotate through images
        let currentImageIndex = 0;
        setHeroBackground(galleryImages[0]);

        setInterval(() => {
            currentImageIndex = (currentImageIndex + 1) % galleryImages.length;
            setHeroBackground(galleryImages[currentImageIndex]);
        }, 10000); // Change every 10 seconds
    } else {
        // Static mode - use first image
        setHeroBackground(galleryImages[0]);
    }
}

// Set hero section background image
function setHeroBackground(imageUrl) {
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        const currentTheme = document.body.getAttribute('data-theme');
        let overlayGradient = 'linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5))';

        // Theme-specific overlays
        if (currentTheme === 'quality_care') {
            overlayGradient = 'linear-gradient(rgba(39, 174, 96, 0.85), rgba(34, 153, 84, 0.85))';
        } else if (currentTheme === 'theme2') {
            overlayGradient = 'linear-gradient(rgba(0, 123, 255, 0.8), rgba(108, 117, 125, 0.8))';
        }

        heroSection.style.backgroundImage = `${overlayGradient}, url('${imageUrl}')`;
        heroSection.style.backgroundSize = 'cover';
        heroSection.style.backgroundPosition = 'center center';
        heroSection.style.backgroundRepeat = 'no-repeat';
        heroSection.style.backgroundAttachment = 'fixed';
    }
}

// Get gallery images from meta tag or data attribute
function getGalleryImages() {
    // Try to get from meta tag first
    const metaGallery = document.querySelector('meta[name="gallery-images"]');
    if (metaGallery && metaGallery.content) {
        return metaGallery.content.split(',').map(url => url.trim()).filter(url => url);
    }

    // Fallback to data attribute
    const heroSection = document.querySelector('.hero-section');
    if (heroSection && heroSection.dataset.galleryImages) {
        return heroSection.dataset.galleryImages.split(',').map(url => url.trim()).filter(url => url);
    }

    return [];
}

// Get gallery mode from meta tag or data attribute
function getGalleryMode() {
    // Try to get from meta tag first
    const metaMode = document.querySelector('meta[name="gallery-mode"]');
    if (metaMode && metaMode.content) {
        return metaMode.content;
    }

    // Fallback to data attribute
    const heroSection = document.querySelector('.hero-section');
    if (heroSection && heroSection.dataset.galleryMode) {
        return heroSection.dataset.galleryMode;
    }

    return 'static'; // Default mode
}

// Export functions for global use
window.BananaExport = {
    showToast,
    updateCartBadge,
    updatePriceDisplay,
    initializeLandscapeBackground,
    setHeroBackground
};

// Handle offline/online status
window.addEventListener('online', () => {
    showToast('Connection restored', 'success');
});

window.addEventListener('offline', () => {
    showToast('No internet connection', 'warning');
});

// Performance monitoring
if ('performance' in window) {
    window.addEventListener('load', () => {
        setTimeout(() => {
            const perfData = performance.getEntriesByType('navigation')[0];
            if (perfData.loadEventEnd - perfData.loadEventStart > 3000) {
                console.log('Page load time is high:', perfData.loadEventEnd - perfData.loadEventStart);
            }
        }, 0);
    });
}

// Error handling for uncaught errors
window.addEventListener('error', (e) => {
    console.error('JavaScript error:', e.error);
    // In production, you might want to send this to a logging service
});

// Service Worker registration (for future PWA features)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // Uncomment when service worker is implemented
        // navigator.serviceWorker.register('/sw.js')
        //     .then(registration => console.log('SW registered'))
        //     .catch(error => console.log('SW registration failed'));
    });
}