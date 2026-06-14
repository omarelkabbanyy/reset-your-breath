/* ============================================
   RESET YOUR BREATH — Interactive Script
   Ambient canvas, mouse tracking, parallax,
   reveal animations, counter, language toggle
   ============================================ */

(function () {
    'use strict';

    // === AMBIENT CANVAS BACKGROUND ===
    const canvas = document.getElementById('ambient-canvas');
    const ctx = canvas.getContext('2d');
    let canvasW, canvasH;
    let animFrame;

    function resizeCanvas() {
        canvasW = canvas.width = window.innerWidth;
        canvasH = canvas.height = window.innerHeight;
    }
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Soft gradient orbs that slowly move
    const orbs = [];
    for (let i = 0; i < 5; i++) {
        orbs.push({
            x: Math.random() * canvasW,
            y: Math.random() * canvasH,
            r: 150 + Math.random() * 250,
            dx: (Math.random() - 0.5) * 0.3,
            dy: (Math.random() - 0.5) * 0.3,
            hue: i % 2 === 0 ? '91,184,154' : '224,122,95',
            alpha: 0.03 + Math.random() * 0.03,
        });
    }

    function drawAmbient() {
        ctx.clearRect(0, 0, canvasW, canvasH);
        orbs.forEach((o) => {
            o.x += o.dx;
            o.y += o.dy;
            if (o.x < -o.r) o.x = canvasW + o.r;
            if (o.x > canvasW + o.r) o.x = -o.r;
            if (o.y < -o.r) o.y = canvasH + o.r;
            if (o.y > canvasH + o.r) o.y = -o.r;

            const grad = ctx.createRadialGradient(o.x, o.y, 0, o.x, o.y, o.r);
            grad.addColorStop(0, `rgba(${o.hue},${o.alpha})`);
            grad.addColorStop(1, 'rgba(0,0,0,0)');
            ctx.fillStyle = grad;
            ctx.fillRect(o.x - o.r, o.y - o.r, o.r * 2, o.r * 2);
        });
        animFrame = requestAnimationFrame(drawAmbient);
    }
    drawAmbient();

    // === FLOATING PARTICLES ===
    const particlesContainer = document.getElementById('particles-container');
    function createParticle() {
        const p = document.createElement('div');
        p.classList.add('particle');
        const size = 2 + Math.random() * 4;
        p.style.width = size + 'px';
        p.style.height = size + 'px';
        p.style.left = Math.random() * 100 + '%';
        p.style.animationDuration = 10 + Math.random() * 15 + 's';
        p.style.animationDelay = Math.random() * 10 + 's';
        p.style.background = Math.random() > 0.7 ? '#e07a5f' : '#5bb89a';
        particlesContainer.appendChild(p);

        // Clean up after animation
        setTimeout(() => {
            p.remove();
            createParticle();
        }, (10 + 15) * 1000 + 10000);
    }
    for (let i = 0; i < 20; i++) {
        setTimeout(createParticle, i * 800);
    }

    // === MOUSE GLOW FOLLOWER ===
    const mouseGlow = document.getElementById('mouse-glow');
    let mouseX = 0, mouseY = 0;
    let glowX = 0, glowY = 0;

    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    function updateGlow() {
        glowX += (mouseX - glowX) * 0.08;
        glowY += (mouseY - glowY) * 0.08;
        mouseGlow.style.left = glowX + 'px';
        mouseGlow.style.top = glowY + 'px';
        requestAnimationFrame(updateGlow);
    }
    updateGlow();

    // === HEADER SCROLL EFFECT ===
    const header = document.getElementById('main-header');
    let lastScroll = 0;

    function onScroll() {
        const scrollY = window.scrollY;
        if (scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
        lastScroll = scrollY;
    }
    window.addEventListener('scroll', onScroll, { passive: true });

    // === MOBILE NAV ===
    const mobileBtn = document.getElementById('mobile-menu-btn');
    const mobileOverlay = document.getElementById('mobile-nav-overlay');
    const mobileLinks = document.querySelectorAll('.mobile-nav-link');

    if (mobileBtn) {
        mobileBtn.addEventListener('click', () => {
            mobileBtn.classList.toggle('open');
            mobileOverlay.classList.toggle('open');
            document.body.style.overflow = mobileOverlay.classList.contains('open') ? 'hidden' : '';
        });

        mobileLinks.forEach((link) => {
            link.addEventListener('click', () => {
                mobileBtn.classList.remove('open');
                mobileOverlay.classList.remove('open');
                document.body.style.overflow = '';
            });
        });
    }

    

    // === SCROLL REVEAL ANIMATIONS ===
    const revealElements = document.querySelectorAll('.reveal-up, .reveal-left, .reveal-right');

    const revealObserver = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('in-view');
                }
            });
        },
        { threshold: 0.15, rootMargin: '0px 0px -60px 0px' }
    );

    revealElements.forEach((el) => revealObserver.observe(el));

    // === TIMELINE ITEMS ===
    const timelineItems = document.querySelectorAll('.timeline-item');
    const timelineObserver = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('in-view');
                }
            });
        },
        { threshold: 0.3 }
    );
    timelineItems.forEach((el) => timelineObserver.observe(el));

    // Timeline progress - support both old and new timeline IDs
    const timelineLine = document.querySelector('.timeline-progress');
    const timeline = document.getElementById('recovery-timeline') || document.getElementById('timeline');

    function updateTimelineProgress() {
        if (!timeline || !timelineLine) return;
        const rect = timeline.getBoundingClientRect();
        const windowH = window.innerHeight;
        const progress = Math.max(0, Math.min(1, (windowH - rect.top) / (rect.height + windowH * 0.5)));
        timelineLine.style.height = (progress * 100) + '%';
    }
    window.addEventListener('scroll', updateTimelineProgress, { passive: true });

    // === COUNTING ANIMATION ===
    function animateCounters(container) {
        const counters = container.querySelectorAll('.count');
        counters.forEach((counter) => {
            const target = parseInt(counter.getAttribute('data-target'));
            const duration = 2000;
            const start = performance.now();

            function animate(now) {
                const elapsed = now - start;
                const progress = Math.min(elapsed / duration, 1);
                const ease = 1 - Math.pow(1 - progress, 3);
                counter.textContent = Math.round(ease * target);
                if (progress < 1) requestAnimationFrame(animate);
            }
            requestAnimationFrame(animate);
        });
    }

    // Observer for any stats container
    const counterObserver = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting && !entry.target.dataset.counted) {
                    entry.target.dataset.counted = 'true';
                    animateCounters(entry.target);
                }
            });
        },
        { threshold: 0.3 }
    );

    // Observe both hero stats and big stats
    const heroStats = document.getElementById('hero-stats');
    const bigStats = document.getElementById('big-stats');
    if (heroStats) counterObserver.observe(heroStats);
    if (bigStats) counterObserver.observe(bigStats);


    // === TILT EFFECT ON FEATURE CARDS ===
    const tiltCards = document.querySelectorAll('[data-tilt]');

    tiltCards.forEach((card) => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const rotateX = ((y - centerY) / centerY) * -6;
            const rotateY = ((x - centerX) / centerX) * 6;

            card.style.transform = `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(800px) rotateX(0deg) rotateY(0deg) translateY(0)';
        });
    });

    // === PARALLAX ON HERO ORBS ===
    const heroOrbs = document.querySelectorAll('.hero-orb');

    function parallaxOrbs() {
        const scrollY = window.scrollY;
        heroOrbs.forEach((orb, i) => {
            const speed = 0.1 + i * 0.05;
            orb.style.transform = `translateY(${scrollY * speed}px)`;
        });
    }
    window.addEventListener('scroll', parallaxOrbs, { passive: true });

    // === LANGUAGE TOGGLE ===
    const langToggle = document.getElementById('lang-toggle');
    const langBtns = langToggle ? langToggle.querySelectorAll('.lang-btn') : [];
    let currentLang = 'en';

    function switchLanguage(lang) {
        currentLang = lang;
        const isAr = lang === 'ar';

        // Toggle body direction
        document.body.classList.toggle('rtl', isAr);
        document.documentElement.setAttribute('lang', lang);
        document.documentElement.setAttribute('dir', isAr ? 'rtl' : 'ltr');

        // Update active btn
        langBtns.forEach((btn) => {
            btn.classList.toggle('active', btn.getAttribute('data-lang') === lang);
        });

        // Update all translatable elements
        document.querySelectorAll('[data-en][data-ar]').forEach((el) => {
            const text = el.getAttribute(`data-${lang}`);
            if (text) el.textContent = text;
        });
    }

    langBtns.forEach((btn) => {
        btn.addEventListener('click', () => {
            switchLanguage(btn.getAttribute('data-lang'));
        });
    });

    // === SMOOTH SCROLL FOR ANCHOR LINKS ===
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
        anchor.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = anchor.getAttribute('href').slice(1);
            const targetEl = document.getElementById(targetId);
            if (targetEl) {
                const top = targetEl.offsetTop - 80;
                window.scrollTo({ top, behavior: 'smooth' });
            }
        });
    });

    // === BREATHING ANIMATION ON LOGO ===
    const logoIcon = document.querySelector('.logo-icon');
    if (logoIcon) {
        logoIcon.addEventListener('mouseenter', () => {
            logoIcon.style.animation = 'gentlePulse 1.5s ease-in-out';
            setTimeout(() => {
                logoIcon.style.animation = '';
            }, 1500);
        });
    }

    // === INITIAL LOAD ANIMATION ===
    window.addEventListener('load', () => {
        document.body.style.opacity = '0';
        document.body.style.transition = 'opacity 0.6s ease';
        requestAnimationFrame(() => {
            document.body.style.opacity = '1';
        });

        // Trigger hero reveals
        setTimeout(() => {
            document.querySelectorAll('.hero-section .reveal-up').forEach((el) => {
                el.classList.add('in-view');
            });
        }, 200);
    });

    // === KEYBOARD ACCESSIBILITY ===
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            mobileBtn.classList.remove('open');
            mobileOverlay.classList.remove('open');
            document.body.style.overflow = '';
        }
    });


    // === SPA ROUTER ===
    const pageSections = document.querySelectorAll('.page-section');
    const navLinksList = document.querySelectorAll('.nav-link, .mobile-nav-link, .scroll-to, .cta-btn[data-page]');
    
    document.querySelectorAll('[data-page]').forEach((btn) => {
        btn.addEventListener('click', (e) => {
            const targetId = btn.getAttribute('data-page');
            const targetPage = document.getElementById('page-' + targetId);
            
            if (targetPage) {
                e.preventDefault();
                // Switch active page section
                pageSections.forEach(page => {
                    page.classList.remove('active');
                    setTimeout(() => {
                        if (!page.classList.contains('active')) {
                            page.style.display = 'none';
                        }
                    }, 400); 
                });
                
                targetPage.style.display = 'block';
                setTimeout(() => {
                    targetPage.classList.add('active');
                    // Retrigger animations
                    targetPage.querySelectorAll('.reveal-up, .reveal-left, .reveal-right').forEach(el => el.classList.remove('in-view'));
                    setTimeout(() => {
                        targetPage.querySelectorAll('.reveal-up, .reveal-left, .reveal-right').forEach(el => el.classList.add('in-view'));
                    }, 50);
                }, 10);
                
                // Update nav link active states
                document.querySelectorAll('.nav-link, .mobile-nav-link').forEach(link => {
                    if (link.getAttribute('data-page') === targetId) {
                        link.classList.add('active');
                    } else {
                        link.classList.remove('active');
                    }
                });

                window.scrollTo({ top: 0, behavior: 'smooth' });
                
                // Close mobile nav if open
                if (document.getElementById('mobile-menu-btn')) {
                    document.getElementById('mobile-menu-btn').classList.remove('open');
                    document.getElementById('mobile-nav-overlay').classList.remove('open');
                    document.body.style.overflow = '';
                }
            }
        });
    });

    // === TREATMENT TABS ===
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanels = document.querySelectorAll('.tab-panel');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabPanels.forEach(p => p.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById(btn.getAttribute('data-target')).classList.add('active');
        });
    });

    // === COMMUNITY VIDEO PLAYER ===
    const vlistItems = document.querySelectorAll('.vlist-item');
    const mainVideo = document.getElementById('main-video-player');
    const mainTitle = document.getElementById('main-video-title');
    
    vlistItems.forEach(item => {
        item.addEventListener('click', () => {
            vlistItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');
            mainVideo.src = "https://www.youtube.com/embed/" + item.getAttribute('data-vid') + "?autoplay=1";
            mainTitle.textContent = item.getAttribute('data-title');
        });
    });

    // === COST CALCULATOR LOGIC ===
    const calcCigs = document.getElementById('calc-cigs');
    const calcPrice = document.getElementById('calc-price');
    const calcDaily = document.getElementById('calc-daily');
    const calcMonthly = document.getElementById('calc-monthly');
    const calcYearly = document.getElementById('calc-yearly');
    const calcFiveYears = document.getElementById('calc-fiveyears');
    const calcCigsYearly = document.getElementById('calc-cigs-yearly');
    
    function updateCalculator() {
        if (!calcCigs || !calcPrice) return;
        const cigsPerDay = parseInt(calcCigs.value) || 0;
        const pricePerPack = parseFloat(calcPrice.value) || 0;
        
        // 20 cigarettes in a pack
        const pricePerCig = pricePerPack / 20;
        const dailyCost = cigsPerDay * pricePerCig;
        
        calcDaily.textContent = dailyCost.toLocaleString() + ' EGP';
        calcMonthly.textContent = (dailyCost * 30).toLocaleString() + ' EGP';
        calcYearly.textContent = (dailyCost * 365).toLocaleString() + ' EGP';
        calcFiveYears.textContent = (dailyCost * 365 * 5).toLocaleString() + ' EGP';
        if (calcCigsYearly) calcCigsYearly.textContent = (cigsPerDay * 365).toLocaleString();
        
        localStorage.setItem('reset_daily_cost', dailyCost);
    }
    
    if (calcCigs && calcPrice) {
        calcCigs.addEventListener('input', updateCalculator);
        calcPrice.addEventListener('input', updateCalculator);
        updateCalculator();
    }

    // === TRACKER LOGIC ===
    const trackerForm = document.getElementById('tracker-form');
    const trackerSignup = document.getElementById('tracker-signup');
    const trackerDashboard = document.getElementById('tracker-dashboard');
    const trackDays = document.getElementById('track-days');
    const trackMoney = document.getElementById('track-money');
    const quitDateInput = document.getElementById('quit-date');
    const resetTrackerBtn = document.getElementById('reset-tracker');

    function initTracker() {
        if (!trackerForm) return;
        const savedQuitDate = localStorage.getItem('reset_quit_date');
        const dailyCost = parseFloat(localStorage.getItem('reset_daily_cost')) || 100;
        
        if (savedQuitDate) {
            trackerSignup.style.display = 'none';
            trackerDashboard.style.display = 'block';
            
            const qDate = new Date(savedQuitDate);
            const today = new Date();
            const diffTime = Math.abs(today - qDate);
            const diffDays = Math.max(0, Math.ceil(diffTime / (1000 * 60 * 60 * 24)) - 1);
            
            trackDays.textContent = diffDays;
            trackMoney.textContent = (diffDays * dailyCost).toLocaleString() + ' EGP';
        } else {
            trackerSignup.style.display = 'block';
            trackerDashboard.style.display = 'none';
        }
    }
    
    if (trackerForm) {
        trackerForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const date = quitDateInput.value;
            if (date) {
                localStorage.setItem('reset_quit_date', date);
                initTracker();
            }
        });
        
        resetTrackerBtn.addEventListener('click', () => {
            localStorage.removeItem('reset_quit_date');
            initTracker();
        });
        
        initTracker();
    }

})();
