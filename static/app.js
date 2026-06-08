/**
 * TravelX AI - Enhanced JavaScript
 * Modern interactions and animations
 */

// ==================== INITIALIZATION ====================
document.addEventListener('DOMContentLoaded', function() {
    initMobileMenu();
    initScrollEffects();
    initFormEnhancements();
    initAnimations();
    initParallax();
    initTooltips();
});

// ==================== MOBILE MENU ====================
function initMobileMenu() {
    const mobileBtn = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    
    if (mobileBtn && mobileMenu) {
        mobileBtn.addEventListener('click', () => {
            mobileBtn.classList.toggle('active');
            mobileMenu.classList.toggle('active');
            document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
        });

        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!mobileBtn.contains(e.target) && !mobileMenu.contains(e.target)) {
                mobileBtn.classList.remove('active');
                mobileMenu.classList.remove('active');
                document.body.style.overflow = '';
            }
        });

        // Close menu on link click
        const mobileLinks = mobileMenu.querySelectorAll('a');
        mobileLinks.forEach(link => {
            link.addEventListener('click', () => {
                mobileBtn.classList.remove('active');
                mobileMenu.classList.remove('active');
                document.body.style.overflow = '';
            });
        });
    }
}

// ==================== SCROLL EFFECTS ====================
function initScrollEffects() {
    const navbar = document.querySelector('.navbar');
    let lastScroll = 0;

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;

        // Add shadow on scroll
        if (currentScroll > 50) {
            navbar?.classList.add('scrolled');
        } else {
            navbar?.classList.remove('scrolled');
        }

        // Reveal animations
        revealOnScroll();

        lastScroll = currentScroll;
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#' && href !== '') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
}

// ==================== REVEAL ON SCROLL ====================
function revealOnScroll() {
    const reveals = document.querySelectorAll('.fade-in, .destination-card, .feature-card');
    
    reveals.forEach(element => {
        const windowHeight = window.innerHeight;
        const elementTop = element.getBoundingClientRect().top;
        const elementVisible = 150;

        if (elementTop < windowHeight - elementVisible) {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }
    });
}

// ==================== FORM ENHANCEMENTS ====================
function initFormEnhancements() {
    const form = document.getElementById('tripForm');
    
    if (form) {
        // Add floating label effect
        const inputs = form.querySelectorAll('.form-input, .form-select');
        inputs.forEach(input => {
            // Add focus effects
            input.addEventListener('focus', function() {
                this.parentElement.classList.add('focused');
            });

            input.addEventListener('blur', function() {
                if (!this.value) {
                    this.parentElement.classList.remove('focused');
                }
            });

            // Validate on change
            input.addEventListener('change', function() {
                validateField(this);
            });
        });

        // Form submission with loading state
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('.submit-btn');
            if (submitBtn && !form.dataset.submitting) {
                form.dataset.submitting = 'true';
                submitBtn.innerHTML = `
                    <div class="btn-content">
                        <svg class="btn-icon spinning" width="24" height="24" viewBox="0 0 24 24" fill="none">
                            <circle cx="12" cy="12" r="10" stroke="white" stroke-width="3" stroke-dasharray="60" stroke-dashoffset="20"/>
                        </svg>
                        Generating Your Perfect Trip...
                    </div>
                    <div class="btn-subtext">This may take a few seconds</div>
                `;
                submitBtn.disabled = true;
            }
        });

        // Date validation
        const startDate = form.querySelector('input[name="date"]');
        const endDate = form.querySelector('input[name="return"]');
        
        if (startDate && endDate) {
            const today = new Date().toISOString().split('T')[0];
            startDate.setAttribute('min', today);
            
            startDate.addEventListener('change', function() {
                endDate.setAttribute('min', this.value);
                if (endDate.value && endDate.value < this.value) {
                    endDate.value = this.value;
                }
            });
        }
    }
}

// ==================== FIELD VALIDATION ====================
function validateField(field) {
    const value = field.value.trim();
    const fieldContainer = field.closest('.form-field');
    
    // Remove previous validation
    fieldContainer?.classList.remove('error', 'success');
    
    if (field.hasAttribute('required') && !value) {
        fieldContainer?.classList.add('error');
        return false;
    }
    
    if (value) {
        fieldContainer?.classList.add('success');
    }
    
    return true;
}

// ==================== ANIMATIONS ====================
function initAnimations() {
    // Animate stats on scroll
    const stats = document.querySelectorAll('.stat-number');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateNumber(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    stats.forEach(stat => observer.observe(stat));

    // Stagger animation for cards
    const cards = document.querySelectorAll('.destination-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
}

// ==================== NUMBER ANIMATION ====================
function animateNumber(element) {
    const text = element.textContent;
    const number = parseFloat(text.replace(/[^0-9.]/g, ''));
    
    if (isNaN(number)) return;
    
    const suffix = text.replace(/[0-9.]/g, '');
    const duration = 2000;
    const steps = 60;
    const increment = number / steps;
    let current = 0;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= number) {
            element.textContent = number + suffix;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current) + suffix;
        }
    }, duration / steps);
}

// ==================== PARALLAX EFFECT ====================
function initParallax() {
    const parallaxElements = document.querySelectorAll('.hero-graphic, .floating-card');
    
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        
        parallaxElements.forEach(element => {
            const speed = element.dataset.speed || 0.5;
            const yPos = -(scrolled * speed);
            element.style.transform = `translateY(${yPos}px)`;
        });
    });
}

// ==================== TOOLTIPS ====================
function initTooltips() {
    const tooltipTriggers = document.querySelectorAll('[data-tooltip]');
    
    tooltipTriggers.forEach(trigger => {
        trigger.addEventListener('mouseenter', function(e) {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.dataset.tooltip;
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
            
            setTimeout(() => tooltip.classList.add('show'), 10);
            
            this.addEventListener('mouseleave', function() {
                tooltip.classList.remove('show');
                setTimeout(() => tooltip.remove(), 300);
            }, { once: true });
        });
    });
}

// ==================== FLASH MESSAGES ====================
function initFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash');
    
    flashMessages.forEach(flash => {
        setTimeout(() => {
            flash.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(() => flash.remove(), 300);
        }, 5000);
        
        flash.addEventListener('click', function() {
            this.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(() => this.remove(), 300);
        });
    });
}

// Initialize flash messages
initFlashMessages();

// ==================== SCROLL TO TOP ====================
const scrollTopBtn = document.getElementById('scrollTopBtn');
if (scrollTopBtn) {
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            scrollTopBtn.classList.add('visible');
        } else {
            scrollTopBtn.classList.remove('visible');
        }
    });

    scrollTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// ==================== LOADING ANIMATION ====================
window.addEventListener('load', () => {
    document.body.classList.add('loaded');
});

// ==================== UTILITY FUNCTIONS ====================
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

// Export for use in other scripts
window.TravelXAI = {
    animateNumber,
    validateField,
    debounce
};
