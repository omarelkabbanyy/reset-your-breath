import re

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace the active nav updating code because the original used sections, but we now use SPA
# Let's remove the scroll observer for sections
nav_update_code = """    // === ACTIVE NAV LINK ON SCROLL ===
    const navLinks = document.querySelectorAll('.nav-link[data-page]');
    const sections = document.querySelectorAll('section[id]');

    function updateActiveNav() {
        const scrollY = window.scrollY + 200;
        sections.forEach((section) => {
            const top = section.offsetTop;
            const height = section.offsetHeight;
            const id = section.getAttribute('id');
            if (scrollY >= top && scrollY < top + height) {
                navLinks.forEach((l) => l.classList.remove('active'));
                const active = document.querySelector(`.nav-link[data-page="${id}"]`);
                if (active) active.classList.add('active');
            }
        });
    }
    window.addEventListener('scroll', updateActiveNav, { passive: true });"""
    
# Remove that block completely
js = re.sub(r'// === ACTIVE NAV LINK ON SCROLL ===.*?window\.addEventListener\(\'scroll\', updateActiveNav, \{ passive: true \}\);', '', js, flags=re.DOTALL)

# Add SPA, Tabs, Video, Calc, Tracker
additional_js = """
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
"""

js = js.replace('})();', additional_js + '\n})();')

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)
