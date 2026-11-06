/**
 * Wendwosen Tessema — Personal Developer Portfolio
 * Vanilla JavaScript (Minimal & Robust)
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile Menu Toggle
    const navToggle = document.getElementById('navToggle');
    const siteNav = document.getElementById('siteNav');

    if (navToggle && siteNav) {
        navToggle.addEventListener('click', () => {
            const isOpen = siteNav.classList.toggle('is-open');
            navToggle.setAttribute('aria-expanded', isOpen.toString());
        });

        // Close menu on link click
        siteNav.querySelectorAll('.nav-link, .btn-cv').forEach(link => {
            link.addEventListener('click', () => {
                siteNav.classList.remove('is-open');
                navToggle.setAttribute('aria-expanded', 'false');
            });
        });

        // Close menu on click outside
        document.addEventListener('click', (e) => {
            if (!siteNav.contains(e.target) && !navToggle.contains(e.target) && siteNav.classList.contains('is-open')) {
                siteNav.classList.remove('is-open');
                navToggle.setAttribute('aria-expanded', 'false');
            }
        });
    }

    // 2. Contact Form Asynchronous Submission (with Progressive Enhancement)
    const contactForm = document.getElementById('contactForm');
    const submitBtn = document.getElementById('submitBtn');
    const formStatus = document.getElementById('formStatus');

    if (contactForm && submitBtn && formStatus) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            // Clear previous errors
            contactForm.querySelectorAll('.form-error').forEach(el => el.remove());
            formStatus.textContent = '';
            formStatus.style.color = '';

            const originalBtnHtml = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span>Sending...</span>';

            const formData = new FormData(contactForm);

            try {
                const response = await fetch(contactForm.action, {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'Accept': 'application/json'
                    },
                    body: formData
                });

                const data = await response.json();

                if (response.ok && data.status === 'success') {
                    formStatus.style.color = '#064e3b';
                    formStatus.textContent = '✓ ' + (data.message || 'Message sent successfully!');
                    contactForm.reset();
                } else {
                    formStatus.style.color = '#b91c1c';
                    formStatus.textContent = data.message || 'Please check your input.';

                    if (data.errors) {
                        for (const [field, errors] of Object.entries(data.errors)) {
                            const inputElem = contactForm.querySelector(`[name="${field}"]`);
                            if (inputElem && inputElem.parentElement) {
                                const errSpan = document.createElement('span');
                                errSpan.className = 'form-error';
                                errSpan.textContent = errors[0];
                                inputElem.parentElement.appendChild(errSpan);
                            }
                        }
                    }
                }
            } catch (err) {
                // If network fails, submit naturally
                contactForm.submit();
                return;
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnHtml;
            }
        });
    }

    // 3. Auto-dismiss Toasts
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        setTimeout(() => {
            toast.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(10px)';
            setTimeout(() => toast.remove(), 400);
        }, 5000);
    });

    // 4. Lightbox Image Viewer for "Beyond the Code"
    const lightbox = document.getElementById('portfolioLightbox');
    const lightboxImg = document.getElementById('lightboxImg');
    const lightboxTitle = document.getElementById('lightboxTitle');
    const lightboxCaption = document.getElementById('lightboxCaption');

    if (lightbox && lightboxImg) {
        const openLightbox = (imgUrl, title, caption) => {
            if (!imgUrl) return;
            lightboxImg.src = imgUrl;
            lightboxImg.alt = caption || title || 'Full photo';
            if (lightboxTitle) lightboxTitle.textContent = title || '';
            if (lightboxCaption) lightboxCaption.textContent = caption || '';
            lightbox.classList.add('is-active');
            lightbox.setAttribute('aria-hidden', 'false');
            document.body.style.overflow = 'hidden';
        };

        const closeLightbox = () => {
            lightbox.classList.remove('is-active');
            lightbox.setAttribute('aria-hidden', 'true');
            lightboxImg.src = '';
            document.body.style.overflow = '';
        };

        // Attach triggers
        document.querySelectorAll('.js-lightbox-trigger').forEach(trigger => {
            trigger.addEventListener('click', (e) => {
                e.preventDefault();
                const fullUrl = trigger.getAttribute('data-full');
                const title = trigger.getAttribute('data-title');
                const caption = trigger.getAttribute('data-caption');
                openLightbox(fullUrl, title, caption);
            });

            // Keyboard accessibility
            trigger.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    trigger.click();
                }
            });
        });

        // Close on close button or backdrop click
        lightbox.querySelectorAll('.js-lightbox-close').forEach(btn => {
            btn.addEventListener('click', closeLightbox);
        });

        // Close on ESC
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && lightbox.classList.contains('is-active')) {
                closeLightbox();
            }
        });
    }

    // 5. Interactive Activity Boxes (Beyond the Code Hover Reveal & Mobile Tap)
    const activityBoxes = document.querySelectorAll('.js-activity-box');
    if (activityBoxes.length > 0) {
        const isHoverDevice = () => window.matchMedia('(hover: hover) and (pointer: fine)').matches;

        activityBoxes.forEach(box => {
            const detailUrl = box.getAttribute('data-href');

            // Click / Tap Handler
            box.addEventListener('click', (e) => {
                // On desktop mouse devices, clicking navigates directly to detail page
                if (isHoverDevice()) {
                    if (detailUrl && !e.target.closest('a[href]:not(.activity-box-link)')) {
                        // Natural navigation happens via .activity-box-link
                        return;
                    }
                    return;
                }

                // On touch / mobile screens:
                // If tapped directly on the dedicated "View details ↗" link, navigate
                if (e.target.closest('.js-activity-detail-link')) {
                    return;
                }

                // Prevent full-box overlay link from triggering immediate page load on touch tap
                if (e.target.closest('.activity-box-link')) {
                    e.preventDefault();
                }

                const isRevealed = box.classList.contains('is-revealed');

                // Close other opened boxes for cleaner single-focus mobile view
                activityBoxes.forEach(otherBox => {
                    if (otherBox !== box && otherBox.classList.contains('is-revealed')) {
                        otherBox.classList.remove('is-revealed');
                        otherBox.setAttribute('aria-expanded', 'false');
                    }
                });

                if (isRevealed) {
                    // Tapping again returns to text state
                    box.classList.remove('is-revealed');
                    box.setAttribute('aria-expanded', 'false');
                } else {
                    // First tap reveals photographs
                    box.classList.add('is-revealed');
                    box.setAttribute('aria-expanded', 'true');
                }
            });

            // Keyboard accessibility
            box.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    if (detailUrl) {
                        window.location.href = detailUrl;
                    }
                } else if (e.key === ' ') {
                    e.preventDefault();
                    const willReveal = !box.classList.contains('is-revealed');
                    box.classList.toggle('is-revealed');
                    box.setAttribute('aria-expanded', willReveal ? 'true' : 'false');
                }
            });
        });
    }

    // 6. Personal Moments Photo Slideshow ("Life Beyond the Screen")
    const momentsSlideshow = document.querySelector('.js-moments-slideshow');
    if (momentsSlideshow) {
        const slides = momentsSlideshow.querySelectorAll('.js-moments-slide');
        const dots = momentsSlideshow.querySelectorAll('.js-moments-dot');
        const prevBtn = momentsSlideshow.querySelector('.js-moments-prev');
        const nextBtn = momentsSlideshow.querySelector('.js-moments-next');
        const totalSlides = slides.length;

        if (totalSlides > 1) {
            let currentIndex = 0;
            let autoTimer = null;
            let isHovered = false;
            const intervalMs = parseInt(momentsSlideshow.getAttribute('data-interval') || '5000', 10);
            const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

            const goToSlide = (index) => {
                if (index < 0) {
                    currentIndex = totalSlides - 1;
                } else if (index >= totalSlides) {
                    currentIndex = 0;
                } else {
                    currentIndex = index;
                }

                slides.forEach((slide, i) => {
                    const isActive = i === currentIndex;
                    slide.classList.toggle('is-active', isActive);
                    slide.setAttribute('aria-hidden', isActive ? 'false' : 'true');
                });

                dots.forEach((dot, i) => {
                    const isActive = i === currentIndex;
                    dot.classList.toggle('is-active', isActive);
                    dot.setAttribute('aria-selected', isActive ? 'true' : 'false');
                });
            };

            const nextSlide = () => goToSlide(currentIndex + 1);
            const prevSlide = () => goToSlide(currentIndex - 1);

            const startAutoplay = () => {
                if (prefersReducedMotion || isHovered) return;
                stopAutoplay();
                autoTimer = setInterval(nextSlide, intervalMs);
            };

            const stopAutoplay = () => {
                if (autoTimer) {
                    clearInterval(autoTimer);
                    autoTimer = null;
                }
            };

            const resetAutoplay = () => {
                stopAutoplay();
                startAutoplay();
            };

            // Previous / Next button clicks
            if (prevBtn) {
                prevBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    prevSlide();
                    resetAutoplay();
                });
            }

            if (nextBtn) {
                nextBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    nextSlide();
                    resetAutoplay();
                });
            }

            // Dot indicators click
            dots.forEach(dot => {
                dot.addEventListener('click', (e) => {
                    e.preventDefault();
                    const targetIndex = parseInt(dot.getAttribute('data-slide-index'), 10);
                    if (!isNaN(targetIndex) && targetIndex !== currentIndex) {
                        goToSlide(targetIndex);
                        resetAutoplay();
                    }
                });
            });

            // Pause on hover, resume on mouse leave
            momentsSlideshow.addEventListener('mouseenter', () => {
                isHovered = true;
                stopAutoplay();
            });

            momentsSlideshow.addEventListener('mouseleave', () => {
                isHovered = false;
                startAutoplay();
            });

            // Pause when page is hidden (e.g. background tab)
            document.addEventListener('visibilitychange', () => {
                if (document.hidden) {
                    stopAutoplay();
                } else {
                    startAutoplay();
                }
            });

            // Keyboard navigation when slideshow is focused
            momentsSlideshow.addEventListener('keydown', (e) => {
                if (e.key === 'ArrowLeft') {
                    e.preventDefault();
                    prevSlide();
                    resetAutoplay();
                } else if (e.key === 'ArrowRight') {
                    e.preventDefault();
                    nextSlide();
                    resetAutoplay();
                }
            });

            // Touch swipe gesture support for mobile
            let touchStartX = 0;
            let touchStartY = 0;
            let touchEndX = 0;
            let touchEndY = 0;

            momentsSlideshow.addEventListener('touchstart', (e) => {
                if (e.touches && e.touches.length > 0) {
                    touchStartX = e.touches[0].clientX;
                    touchStartY = e.touches[0].clientY;
                }
            }, { passive: true });

            momentsSlideshow.addEventListener('touchend', (e) => {
                if (e.changedTouches && e.changedTouches.length > 0) {
                    touchEndX = e.changedTouches[0].clientX;
                    touchEndY = e.changedTouches[0].clientY;
                    handleSwipe();
                }
            }, { passive: true });

            const handleSwipe = () => {
                const diffX = touchEndX - touchStartX;
                const diffY = touchEndY - touchStartY;
                if (Math.abs(diffX) > 40 && Math.abs(diffX) > Math.abs(diffY)) {
                    if (diffX < 0) {
                        nextSlide();
                    } else {
                        prevSlide();
                    }
                    resetAutoplay();
                }
            };

            // Initialize autoplay
            startAutoplay();
        }
    }
});

