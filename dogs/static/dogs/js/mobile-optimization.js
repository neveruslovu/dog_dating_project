/**
 * Mobile Optimization JavaScript
 * Handles mobile-specific optimizations and interactions
 */

(function () {
    'use strict';

    // Configuration
    const config = {
        debug: false,
        enableLogging: false
    };

    // Utility functions
    const log = config.enableLogging ? console.log : () => { };
    const warn = config.enableLogging ? console.warn : () => { };

    /**
     * Detect if device is mobile
     */
    function isMobileDevice() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    }

    /**
     * Detect if device has touch capability
     */
    function isTouchDevice() {
        return (
            ('ontouchstart' in window) ||
            (navigator.maxTouchPoints > 0) ||
            (navigator.msMaxTouchPoints > 0)
        );
    }

    /**
     * Fix viewport height for mobile browsers
     * Handles address bar hide/show on scroll
     */
    function fixViewportHeight() {
        if (!window.visualViewport) return;

        function updateVH() {
            const vh = window.innerHeight * 0.01;
            document.documentElement.style.setProperty('--vh', vh + 'px');
        }

        window.visualViewport.addEventListener('resize', updateVH);
        updateVH();
    }

    /**
     * Prevent zoom on double-tap
     */
    function preventDoubleTapZoom() {
        let lastTouchEnd = 0;

        document.addEventListener('touchend', function (event) {
            const now = Date.now();
            if (now - lastTouchEnd <= 300) {
                event.preventDefault();
            }
            lastTouchEnd = now;
        }, false);
    }

    /**
     * Optimize form inputs for mobile
     */
    function optimizeFormInputs() {
        const inputs = document.querySelectorAll('input, textarea, select');

        inputs.forEach(input => {
            // Disable autocorrect on text fields
            input.setAttribute('autocorrect', 'off');
            input.setAttribute('autocapitalize', 'off');

            // Add proper input types for better mobile keyboard
            const type = input.type;
            if (type === 'text') {
                const name = input.name || '';
                if (name.includes('email')) {
                    input.type = 'email';
                } else if (name.includes('phone') || name.includes('tel')) {
                    input.type = 'tel';
                } else if (name.includes('url') || name.includes('website')) {
                    input.type = 'url';
                } else if (name.includes('number') || name.includes('count')) {
                    input.type = 'number';
                }
            }
        });
    }

    /**
     * Handle safe area insets for notched devices
     */
    function handleSafeAreaInsets() {
        const hasNotch = CSS.supports('padding: max(0px)');
        if (!hasNotch) return;

        const styles = `
            body {
                padding-left: max(1rem, env(safe-area-inset-left));
                padding-right: max(1rem, env(safe-area-inset-right));
                padding-top: max(0px, env(safe-area-inset-top));
                padding-bottom: max(1rem, env(safe-area-inset-bottom));
            }
            .main-header {
                padding-left: max(0.5rem, env(safe-area-inset-left));
                padding-right: max(0.5rem, env(safe-area-inset-right));
            }
            .main-footer {
                padding-bottom: max(1rem, env(safe-area-inset-bottom));
            }
        `;

        const styleElement = document.createElement('style');
        styleElement.textContent = styles;
        document.head.appendChild(styleElement);
    }

    /**
     * Smooth scroll polyfill for older browsers
     */
    function enableSmoothScroll() {
        if (!CSS.supports('scroll-behavior: smooth')) {
            const style = document.createElement('style');
            style.textContent = `
                html {
                    scroll-behavior: auto !important;
                }
            `;
            document.head.appendChild(style);
        }
    }

    /**
     * Optimize images for mobile
     */
    function optimizeImages() {
        const images = document.querySelectorAll('img');

        images.forEach(img => {
            // Add loading attribute for lazy loading
            if (!img.hasAttribute('loading')) {
                img.setAttribute('loading', 'lazy');
            }

            // Prevent long-press menu on images
            img.style.webkitTouchCallout = 'none';
            img.style.webkitUserSelect = 'none';
            img.style.userSelect = 'none';
        });
    }

    /**
     * Handle mobile menu toggle
     */
    function setupMobileMenuToggle() {
        const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
        const sidebar = document.querySelector('.sidebar');

        if (!mobileMenuToggle || !sidebar) return;

        mobileMenuToggle.addEventListener('click', function (e) {
            e.preventDefault();
            sidebar.classList.toggle('active');

            // Update aria attribute
            const isActive = sidebar.classList.contains('active');
            mobileMenuToggle.setAttribute('aria-expanded', isActive);
        });

        // Close menu only when a real navigation link (leaf item) is clicked
        // Leaf links use the 'header-nav-link' class; top-level spans without URLs
        // (e.g. "Информация", "Собаки") keep the sidebar open so their submenus
        // can be expanded and a subsection selected on mobile.
        const leafMenuLinks = sidebar.querySelectorAll('.menu-link.header-nav-link');
        leafMenuLinks.forEach(link => {
            link.addEventListener('click', function () {
                sidebar.classList.remove('active');
                mobileMenuToggle.setAttribute('aria-expanded', 'false');
            });
        });

        // Close menu when clicking outside
        document.addEventListener('click', function (e) {
            if (!sidebar.contains(e.target) && !mobileMenuToggle.contains(e.target)) {
                sidebar.classList.remove('active');
                mobileMenuToggle.setAttribute('aria-expanded', 'false');
            }
        });

        // Prevent scrolling when menu is open
        sidebar.addEventListener('touchmove', function (e) {
            if (this.classList.contains('active')) {
                // Allow scrolling within sidebar, prevent body scroll
                if (e.target === this || !this.contains(e.target)) {
                    e.preventDefault();
                }
            }
        }, { passive: false });
    }

    /**
     * Optimize tooltips for mobile
     */
    function optimizeTooltips() {
        const tooltips = document.querySelectorAll('[title]');

        tooltips.forEach(element => {
            if (isTouchDevice()) {
                // Convert title to aria-label for touch devices
                const title = element.getAttribute('title');
                element.setAttribute('aria-label', title);
                element.removeAttribute('title');
            }
        });
    }

    /**
     * Handle viewport orientation changes
     */
    function handleOrientationChange() {
        window.addEventListener('orientationchange', function () {
            // Give the browser time to update dimensions
            setTimeout(function () {
                // Trigger resize event for any listeners
                window.dispatchEvent(new Event('resize'));

                // Optionally scroll to top on orientation change
                // window.scrollTo(0, 0);

                log('Orientation changed to: ' + window.innerWidth + 'x' + window.innerHeight);
            }, 100);
        });
    }

    /**
     * Performance optimization: Debounce resize events
     */
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

    /**
     * Lazy load below-the-fold images (fallback for older browsers)
     */
    function setupIntersectionObserver() {
        if (!('IntersectionObserver' in window)) {
            // Fallback for older browsers
            const images = document.querySelectorAll('img[loading="lazy"]');
            images.forEach(img => {
                img.loading = '';
            });
            return;
        }

        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                    }
                    observer.unobserve(img);
                }
            });
        }, {
            rootMargin: '50px'
        });

        const lazyImages = document.querySelectorAll('img[data-src]');
        lazyImages.forEach(img => imageObserver.observe(img));
    }

    /**
     * Fix input zoom on focus (iOS Safari)
     */
    function fixInputZoom() {
        if (!isMobileDevice()) return;

        const inputs = document.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('focus', function () {
                // Temporarily increase font size to prevent zoom
                const originalSize = this.style.fontSize;
                this.style.fontSize = '16px';

                setTimeout(() => {
                    this.style.fontSize = originalSize;
                }, 0);
            });
        });
    }

    /**
     * Prevent body scroll when modal is open
     */
    function setupModalScrollPrevention() {
        const modals = document.querySelectorAll('.modal');

        modals.forEach(modal => {
            const observer = new MutationObserver(function (mutations) {
                mutations.forEach(function (mutation) {
                    if (mutation.attributeName === 'class') {
                        const isOpen = modal.classList.contains('show');
                        if (isOpen) {
                            document.body.style.overflow = 'hidden';
                        } else {
                            document.body.style.overflow = '';
                        }
                    }
                });
            });

            observer.observe(modal, { attributes: true, attributeFilter: ['class'] });
        });
    }

    /**
     * Initialize all mobile optimizations
     */
    function init() {
        log('Initializing mobile optimizations...');

        // Core optimizations
        fixViewportHeight();
        preventDoubleTapZoom();
        enableSmoothScroll();
        handleSafeAreaInsets();

        // UI optimizations
        optimizeFormInputs();
        optimizeImages();
        optimizeTooltips();
        setupMobileMenuToggle();

        // Event handlers
        handleOrientationChange();
        fixInputZoom();

        // Modern APIs
        if ('IntersectionObserver' in window) {
            setupIntersectionObserver();
        }

        // Check for modals
        if (document.querySelectorAll('.modal').length > 0) {
            setupModalScrollPrevention();
        }

        log('Mobile optimizations initialized successfully');
    }

    /**
     * Run initialization when DOM is ready
     */
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Export for debugging
    if (config.debug) {
        window.mobileOptimizations = {
            isMobileDevice,
            isTouchDevice,
            config
        };
    }
})();
