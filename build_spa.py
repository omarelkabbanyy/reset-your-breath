import re
import os

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace Nav links to use data-page and #
nav_html = """            <nav id="desktop-nav">
                <a href="#home" class="nav-link active" data-page="home">Home</a>
                <a href="#science" class="nav-link" data-page="science">Science</a>
                <a href="#community" class="nav-link" data-page="community">Community</a>
                <a href="#products" class="nav-link" data-page="products">Products</a>
                <a href="#calculator" class="nav-link" data-page="calculator">Cost</a>
                <a href="#treatment" class="nav-link" data-page="treatment">Treatment</a>
                <a href="#track" class="nav-link" data-page="track">Track</a>
            </nav>"""
html = re.sub(r'<nav id="desktop-nav">.*?</nav>', nav_html, html, flags=re.DOTALL)

mobile_nav_html = """        <div class="mobile-nav-content">
            <a href="#home" class="mobile-nav-link" data-page="home">Home</a>
            <a href="#science" class="mobile-nav-link" data-page="science">Science</a>
            <a href="#community" class="mobile-nav-link" data-page="community">Community</a>
            <a href="#products" class="mobile-nav-link" data-page="products">Products</a>
            <a href="#calculator" class="mobile-nav-link" data-page="calculator">Cost</a>
            <a href="#treatment" class="mobile-nav-link" data-page="treatment">Treatment</a>
            <a href="#track" class="mobile-nav-link" data-page="track">Track</a>
            <a href="#track" class="cta-btn mobile-cta" data-page="track">
                <span data-en="Today, I choose myself" data-ar="اليوم، أختار نفسي">Today, I choose myself</span>
            </a>
        </div>"""
html = re.sub(r'<div class="mobile-nav-content">.*?</div>\s*</div>', mobile_nav_html + '\n    </div>', html, flags=re.DOTALL)

# Wrap existing content
start_marker = '<!-- ==================== HERO SECTION ==================== -->'
end_marker = '<!-- ==================== FOOTER ==================== -->'
home_start = html.find(start_marker)
home_end = html.find(end_marker)
home_content = html[home_start:home_end]

# Modify home_content to ONLY contain Hero. Move the rest to Science!
# Actually, their original had types, psychology, damage, statistics, timeline, treatment on the main page.
# I will keep Hero on Home. Move the rest!
hero_end = home_content.find('<!-- ==================== TYPES OF SMOKING ==================== -->')
if hero_end == -1:
    hero_end = home_content.find('<section id="types"')
if hero_end == -1:
    hero_end = len(home_content)

hero_section = home_content[:hero_end]

# Extract sections for Science
types_start = home_content.find('<section id="types"')
treat_start = home_content.find('<section id="treatment"')

science_sections = home_content[types_start:treat_start] if treat_start != -1 else home_content[types_start:]

new_pages = """
    <div id="pages-container">
        <!-- ══════════════════ HOME PAGE ══════════════════ -->
        <div id="page-home" class="page-section active">
""" + hero_section + """
        </div>

        <!-- ══════════════════ SCIENCE PAGE ══════════════════ -->
        <div id="page-science" class="page-section">
            <div class="page-inner">
                <div class="page-hero reveal-up">
                    <span class="section-tag">Science & Biology</span>
                    <h2>The Science of Addiction</h2>
                    <p>Dive deep into the cardiopulmonary hazards of smoking, the psychology of addiction, and the timeline of recovery.</p>
                </div>
""" + science_sections + """
            </div>
        </div>

        <!-- ══════════════════ COMMUNITY PAGE ══════════════════ -->
        <div id="page-community" class="page-section">
            <div class="page-inner">
                <div class="page-hero reveal-up">
                    <span class="section-tag">Community</span>
                    <h2>Community Support</h2>
                    <p>Watch curated videos that support your quit journey, hear from others, and find the motivation you need.</p>
                </div>
                
                <div class="community-layout reveal-up delay-1">
                    <div class="video-main">
                        <div class="video-main-wrap">
                            <iframe id="main-video-player" src="https://www.youtube.com/embed/l5aZJBLAu1E" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>
                        </div>
                        <div class="video-title-bar" id="main-video-title">What happens when you stop smoking</div>
                    </div>
                    
                    <div class="video-list">
                        <div class="vlist-item active" data-vid="l5aZJBLAu1E" data-title="What happens when you stop smoking">
                            <div class="vlist-num">1</div>
                            <div class="vlist-label">What happens when you stop smoking</div>
                        </div>
                        <div class="vlist-item" data-vid="fDbxZTcg6tA" data-title="A helpful guide to stop smoking">
                            <div class="vlist-num">2</div>
                            <div class="vlist-label">A helpful guide to stop smoking</div>
                        </div>
                        <div class="vlist-item" data-vid="0GwyZpWw98s" data-title="How to quit all types of smoking">
                            <div class="vlist-num">3</div>
                            <div class="vlist-label">How to quit all types of smoking</div>
                        </div>
                        <div class="vlist-item" data-vid="nDZIf1a951E" data-title="Quitting smoking timeline">
                            <div class="vlist-num">4</div>
                            <div class="vlist-label">Quitting smoking timeline</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ══════════════════ PRODUCTS PAGE ══════════════════ -->
        <div id="page-products" class="page-section">
            <div class="page-inner">
                <div class="page-hero reveal-up">
                    <span class="section-tag">NRT Products</span>
                    <h2>Quit-Smoking Aids</h2>
                    <p>Explore medically approved Nicotine Replacement Therapies (NRT) and medications to double your chances of quitting.</p>
                </div>
                
                <div class="products-grid">
                    <!-- Champix -->
                    <div class="product-card reveal-up">
                        <div class="product-video-wrap">
                            <iframe src="https://www.youtube.com/embed/osVTf4Un_3c?rel=0&modestbranding=1" allow="autoplay; fullscreen" allowfullscreen></iframe>
                        </div>
                        <div class="product-body">
                            <h3>Champix (Varenicline)</h3>
                            <p class="prod-sub">Prescription medication</p>
                            <div class="buy-links mt-auto">
                                <a href="https://www.vezeeta.com/en-eg/pharmacy/champix-1-mg-28-f-c-tablet" target="_blank" class="buy-btn">Buy on Vezeeta</a>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Nicotine Gum -->
                    <div class="product-card reveal-up delay-1">
                        <div class="product-video-wrap">
                            <iframe src="https://www.youtube.com/embed/7wvBq38mues?rel=0&modestbranding=1" allow="autoplay; fullscreen" allowfullscreen></iframe>
                        </div>
                        <div class="product-body">
                            <h3>Nicotine Gum</h3>
                            <p class="prod-sub">Fast-acting craving relief</p>
                            <div class="buy-links mt-auto">
                                <a href="https://www.amazon.com/Blip-NRT-Nicotine-Gum-Replacement/dp/B0CM6V6TS9" target="_blank" class="buy-btn amazon">Buy on Amazon</a>
                            </div>
                        </div>
                    </div>

                    <!-- Lozenges -->
                    <div class="product-card reveal-up delay-2">
                        <div class="product-video-wrap">
                            <iframe src="https://www.youtube.com/embed/IzRgbANNrWE?rel=0&modestbranding=1" allow="autoplay; fullscreen" allowfullscreen></iframe>
                        </div>
                        <div class="product-body">
                            <h3>Nicotine Lozenges</h3>
                            <p class="prod-sub">Discreet craving control</p>
                            <div class="buy-links mt-auto">
                                <a href="https://www.amazon.com/Quitine-Nicotine-Lozenges-Flavor-Smoking/dp/B0DN3YWVVB" target="_blank" class="buy-btn amazon">Buy on Amazon</a>
                            </div>
                        </div>
                    </div>

                    <!-- Patches -->
                    <div class="product-card reveal-up">
                        <div class="product-video-wrap">
                            <iframe src="https://www.youtube.com/embed/3e4-_X_5kWA?rel=0&modestbranding=1" allow="autoplay; fullscreen" allowfullscreen></iframe>
                        </div>
                        <div class="product-body">
                            <h3>Nicotine Patches</h3>
                            <p class="prod-sub">24-hour steady nicotine release</p>
                            <div class="buy-links mt-auto">
                                <a href="https://a.co/d/08cWSVRk" target="_blank" class="buy-btn amazon">Buy on Amazon</a>
                            </div>
                        </div>
                    </div>

                    <!-- Inhalers -->
                    <div class="product-card reveal-up delay-1">
                        <div class="product-video-wrap">
                            <iframe src="https://www.youtube.com/embed/TlkLj4IY25s?rel=0&modestbranding=1" allow="autoplay; fullscreen" allowfullscreen></iframe>
                        </div>
                        <div class="product-body">
                            <h3>Nicotine Inhalers</h3>
                            <p class="prod-sub">Mimics the hand-to-mouth habit</p>
                            <div class="buy-links mt-auto">
                                <a href="https://a.co/d/0fB0F24d" target="_blank" class="buy-btn amazon">Buy on Amazon</a>
                            </div>
                        </div>
                    </div>

                    <!-- Nasal Spray -->
                    <div class="product-card reveal-up delay-2">
                        <div class="product-video-wrap">
                            <iframe src="https://www.youtube.com/embed/1ofPBXHDVDc?rel=0&modestbranding=1" allow="autoplay; fullscreen" allowfullscreen></iframe>
                        </div>
                        <div class="product-body">
                            <h3>Nicotine Nasal Spray</h3>
                            <p class="prod-sub">Fastest nicotine delivery</p>
                            <div class="buy-links mt-auto">
                                <a href="https://a.co/d/0atPe6Zg" target="_blank" class="buy-btn amazon">Buy on Amazon</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ══════════════════ COST CALCULATOR PAGE ══════════════════ -->
        <div id="page-calculator" class="page-section">
            <div class="page-inner" style="max-width: 800px;">
                <div class="page-hero reveal-up text-center">
                    <span class="section-tag">Cost Calculator</span>
                    <h2>What is it really costing you?</h2>
                    <p>Adjust your habit below to see the money — and the time — smoking takes from you.</p>
                </div>
                
                <div class="glass-card reveal-up" style="margin-bottom: 2rem;">
                    <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 2rem;">
                        <div class="input-group">
                            <label style="display:block; margin-bottom: 0.5rem; font-weight:600; color: rgba(255,255,255,0.8);">Cigarettes per day</label>
                            <input type="number" id="calc-cigs" value="20" min="1" max="100" style="width:100%; padding:1rem; border-radius:12px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); color:white; font-size:1.1rem; outline:none;">
                        </div>
                        <div class="input-group">
                            <label style="display:block; margin-bottom: 0.5rem; font-weight:600; color: rgba(255,255,255,0.8);">Price per pack (EGP)</label>
                            <input type="number" id="calc-price" value="100" min="1" max="1000" style="width:100%; padding:1rem; border-radius:12px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); color:white; font-size:1.1rem; outline:none;">
                        </div>
                    </div>
                </div>

                <div class="products-grid" style="grid-template-columns: 1fr 1fr;">
                    <div class="glass-card reveal-up" style="text-align:center; padding: 2rem;">
                        <h3 id="calc-daily" style="font-size:2.5rem; color:#5bb89a; margin-bottom:0.5rem;">100 EGP</h3>
                        <p style="color: rgba(255,255,255,0.6); font-weight:600;">per day</p>
                    </div>
                    <div class="glass-card reveal-up" style="text-align:center; padding: 2rem;">
                        <h3 id="calc-monthly" style="font-size:2.5rem; color:#5bb89a; margin-bottom:0.5rem;">3,000 EGP</h3>
                        <p style="color: rgba(255,255,255,0.6); font-weight:600;">per month</p>
                    </div>
                    <div class="glass-card reveal-up" style="text-align:center; padding: 2rem;">
                        <h3 id="calc-yearly" style="font-size:2.5rem; color:#5bb89a; margin-bottom:0.5rem;">36,500 EGP</h3>
                        <p style="color: rgba(255,255,255,0.6); font-weight:600;">per year</p>
                    </div>
                    <div class="glass-card reveal-up" style="text-align:center; padding: 2rem;">
                        <h3 id="calc-fiveyears" style="font-size:2.5rem; color:#5bb89a; margin-bottom:0.5rem;">182,500 EGP</h3>
                        <p style="color: rgba(255,255,255,0.6); font-weight:600;">over 5 years</p>
                    </div>
                </div>
                
                <div class="calc-cigs-year reveal-up delay-1">
                    <p>Total cigarettes smoked per year:</p>
                    <span id="calc-cigs-yearly">7,300</span>
                </div>
            </div>
        </div>

        <!-- ══════════════════ TREATMENT PAGE ══════════════════ -->
        <div id="page-treatment" class="page-section">
            <div class="page-inner">
                <div class="page-hero reveal-up">
                    <span class="section-tag">Treatment Plans</span>
                    <h2>Comprehensive Treatment</h2>
                    <p>Smoking cessation is most successful when behavioral support is combined with evidence-based medications.</p>
                </div>
                
                <div class="treatment-tab-nav reveal-up">
                    <button class="tab-btn active" data-target="tab-med">Medical Treatment</button>
                    <button class="tab-btn" data-target="tab-psych">Psychological Treatment</button>
                    <button class="tab-btn" data-target="tab-mohp">MOHP Role</button>
                </div>
                
                <div class="tab-content reveal-up delay-1">
                    <div id="tab-med" class="tab-panel active">
                        <div class="nrt-block">
                            <h4>Nicotine Replacement Therapy (NRT)</h4>
                            <p>NRT provides nicotine without the harmful chemicals found in tobacco smoke. It helps reduce withdrawal symptoms and cravings.</p>
                            <ul>
                                <li><strong>Patches:</strong> Steady nicotine release over 24 hours.</li>
                                <li><strong>Gum & Lozenges:</strong> Fast relief for sudden cravings.</li>
                                <li><strong>Inhalers & Sprays:</strong> Prescription options for severe addiction.</li>
                            </ul>
                        </div>
                        <div class="nrt-block">
                            <h4>Prescription Medications</h4>
                            <p>Medications like Varenicline (Champix) block nicotine receptors in the brain, making smoking less enjoyable and reducing cravings.</p>
                            <ul>
                                <li>Highly effective when used as prescribed.</li>
                                <li>Requires consultation with a healthcare provider.</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div id="tab-psych" class="tab-panel">
                        <div class="psych-methods">
                            <div class="psych-method">
                                <div class="method-num">METHOD 1</div>
                                <h4>Cognitive Behavioral Therapy</h4>
                                <p>Helps identify triggers and develop coping strategies to change smoking behavior patterns.</p>
                            </div>
                            <div class="psych-method">
                                <div class="method-num">METHOD 2</div>
                                <h4>Support Groups</h4>
                                <p>Sharing experiences with others who are quitting increases motivation and accountability.</p>
                            </div>
                            <div class="psych-method">
                                <div class="method-num">METHOD 3</div>
                                <h4>Counseling</h4>
                                <p>One-on-one sessions with a cessation specialist to build a personalized quit plan.</p>
                            </div>
                            <div class="psych-method">
                                <div class="method-num">METHOD 4</div>
                                <h4>Stress Management</h4>
                                <p>Learning new ways to handle stress without relying on nicotine.</p>
                            </div>
                        </div>
                    </div>
                    
                    <div id="tab-mohp" class="tab-panel">
                        <div class="mohp-grid">
                            <div class="mohp-item">
                                <div class="mohp-num">16805</div>
                                <h4>National Quitline</h4>
                                <p>Free, confidential telephone counseling and support for anyone trying to quit smoking.</p>
                            </div>
                            <div class="mohp-item">
                                <div class="mohp-num">🏥</div>
                                <h4>Cessation Clinics</h4>
                                <p>Specialized clinics offering medical and psychological support across the country.</p>
                            </div>
                            <div class="mohp-item">
                                <div class="mohp-num">⚖️</div>
                                <h4>Laws & Regulation</h4>
                                <p>Enforcing smoke-free public spaces and banning tobacco advertising to protect public health.</p>
                            </div>
                            <div class="mohp-item">
                                <div class="mohp-num">📢</div>
                                <h4>Public Campaigns</h4>
                                <p>Raising awareness about the dangers of smoking and promoting healthy, smoke-free lifestyles.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ══════════════════ TRACKER PAGE ══════════════════ -->
        <div id="page-track" class="page-section">
            <div class="page-inner" style="max-width: 600px;">
                <div class="page-hero text-center reveal-up">
                    <span class="section-tag">Progress Tracker</span>
                    <h2>Track your progress</h2>
                    <p>Watch your smoke-free days and money saved grow in real-time.</p>
                </div>
                
                <div id="tracker-signup" class="glass-card reveal-up">
                    <h3 style="margin-bottom: 1rem; font-size: 1.5rem;">Begin Your Journey</h3>
                    <p style="color: rgba(255,255,255,0.7); margin-bottom: 2rem;">Enter your details to activate your personalized tracker.</p>
                    
                    <form id="tracker-form" style="display:flex; flex-direction:column; gap:1.25rem;">
                        <div>
                            <label style="display:block; margin-bottom: 0.5rem; font-weight:600;">Full Name</label>
                            <input type="text" required placeholder="Omar Elkabbany" style="width:100%; padding:1rem; border-radius:12px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); color:white; font-size:1rem; outline:none;">
                        </div>
                        <div>
                            <label style="display:block; margin-bottom: 0.5rem; font-weight:600;">Email Address</label>
                            <input type="email" required placeholder="omar@example.com" style="width:100%; padding:1rem; border-radius:12px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); color:white; font-size:1rem; outline:none;">
                        </div>
                        <div>
                            <label style="display:block; margin-bottom: 0.5rem; font-weight:600;">My Quit Date</label>
                            <input type="date" id="quit-date" required style="width:100%; padding:1rem; border-radius:12px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); color:white; font-size:1rem; outline:none; color-scheme: dark;">
                        </div>
                        <button type="submit" class="cta-btn primary-cta" style="margin-top: 1rem; width:100%; justify-content:center; padding: 1rem; font-size:1.1rem;">
                            Start Tracking
                            <span class="cta-glow"></span>
                        </button>
                    </form>
                </div>

                <div id="tracker-dashboard" class="reveal-up" style="display:none;">
                    <div class="glass-card" style="text-align:center; padding: 3rem; margin-bottom:1.5rem; border-color:#5bb89a; background:rgba(91,184,154,0.05);">
                        <div style="font-size: 4rem; margin-bottom: 1rem;">🎉</div>
                        <h3 id="track-days" style="font-size:5rem; font-weight:900; color:#5bb89a; line-height:1;">0</h3>
                        <p style="color: white; font-size:1.2rem; font-weight:600; letter-spacing: 0.05em; text-transform: uppercase; margin-top:0.5rem;">Smoke-Free Days</p>
                    </div>
                    
                    <div class="glass-card" style="text-align:center; padding: 2rem;">
                        <h3 id="track-money" style="font-size:2.5rem; color:#5bb89a; margin-bottom:0.5rem;">0 EGP</h3>
                        <p style="color: rgba(255,255,255,0.7); font-weight:600;">Money Saved</p>
                        <p style="color: rgba(255,255,255,0.4); font-size:0.8rem; margin-top:0.75rem;">Based on your Cost Calculator settings</p>
                    </div>
                    
                    <div style="text-align:center;">
                        <button id="reset-tracker" class="reset-btn">Reset Tracker</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
"""

html = html[:home_start] + new_pages + html[home_end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
