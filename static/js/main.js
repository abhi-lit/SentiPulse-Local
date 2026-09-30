// SentiPulse Local Business Reviews Analyzer - Client JavaScript (Dark Theme & Mouse Hover Animations)

let sentimentChart = null;
let aspectChart = null;

let currentAnalysis = window.INITIAL_ANALYSIS || {};
let currentRecommendations = window.INITIAL_RECOMMENDATIONS || {};
let currentBusiness = window.INITIAL_BUSINESS || {};

document.addEventListener("DOMContentLoaded", () => {
    lucide.createIcons();
    initCharts(currentAnalysis);
    initSurveyCharts();
    initMouseSpotlight();
    applyCardHoverTilt();
});

// Interactive Mouse Cursor Spotlight Follower
function initMouseSpotlight() {
    const spotlight = document.getElementById("mouse-spotlight");
    if (!spotlight) return;

    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;
    let currentX = mouseX;
    let currentY = mouseY;

    window.addEventListener("mousemove", (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    // Smooth lerp animation loop for the spotlight
    function animate() {
        currentX += (mouseX - currentX) * 0.15;
        currentY += (mouseY - currentY) * 0.15;
        spotlight.style.transform = `translate(${currentX}px, ${currentY}px) translate(-50%, -50%)`;
        requestAnimationFrame(animate);
    }
    animate();
}

// 3D Card Hover Tilt Animation
function applyCardHoverTilt() {
    const cards = document.querySelectorAll(".hover-tilt, .review-card");
    cards.forEach(card => {
        // Remove existing listeners if any
        card.onmousemove = (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const rotateX = ((y - centerY) / centerY) * -4;
            const rotateY = ((x - centerX) / centerX) * 4;
            card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateY(-4px)`;
        };
        card.onmouseleave = () => {
            card.style.transform = "perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px)";
        };
    });
}

// Initialize Chart.js with dark mode luxury palette
function initCharts(analysis) {
    const pcts = analysis.sentiment_percentages || { Positive: 0, Neutral: 0, Negative: 0 };
    
    // 1. Sentiment Polarity Donut Chart
    const donutCtx = document.getElementById("sentimentDoughnutChart").getContext("2d");
    sentimentChart = new Chart(donutCtx, {
        type: "doughnut",
        data: {
            labels: ["Positive", "Neutral", "Negative"],
            datasets: [{
                data: [pcts.Positive, pcts.Neutral, pcts.Negative],
                backgroundColor: ["#10b981", "#64748b", "#f43f5e"],
                hoverBackgroundColor: ["#34d399", "#94a3b8", "#fb7185"],
                borderWidth: 3,
                borderColor: "#111827",
                hoverOffset: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: "72%",
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: "rgba(15, 23, 42, 0.95)",
                    titleColor: "#ffffff",
                    bodyColor: "#cbd5e1",
                    borderColor: "rgba(99, 102, 241, 0.3)",
                    borderWidth: 1,
                    padding: 10,
                    callbacks: {
                        label: (ctx) => ` ${ctx.label}: ${ctx.raw}%`
                    }
                }
            }
        }
    });

    // 2. Aspect-Based Satisfaction Bar Chart
    const aspects = analysis.aspect_breakdown || {};
    const aspectLabels = Object.keys(aspects);
    const aspectValues = aspectLabels.map(k => aspects[k].pos_ratio || 0);
    const aspectColors = aspectValues.map(v => v >= 65 ? "#10b981" : (v >= 45 ? "#f59e0b" : "#f43f5e"));

    const barCtx = document.getElementById("aspectBarChart").getContext("2d");
    aspectChart = new Chart(barCtx, {
        type: "bar",
        data: {
            labels: aspectLabels,
            datasets: [{
                label: "Satisfaction (%)",
                data: aspectValues,
                backgroundColor: aspectColors,
                borderRadius: 8,
                barThickness: 18,
                hoverBackgroundColor: "#818cf8"
            }]
        },
        options: {
            indexAxis: "y",
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    beginAtZero: true,
                    max: 100,
                    grid: { color: "rgba(255, 255, 255, 0.07)" },
                    ticks: {
                        color: "#94a3b8",
                        font: { weight: "600" },
                        callback: (val) => val + "%"
                    }
                },
                y: {
                    grid: { display: false },
                    ticks: {
                        color: "#e2e8f0",
                        font: { size: 11, weight: "700" }
                    }
                }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: "rgba(15, 23, 42, 0.95)",
                    titleColor: "#ffffff",
                    bodyColor: "#cbd5e1",
                    borderColor: "rgba(99, 102, 241, 0.3)",
                    borderWidth: 1,
                    padding: 10,
                    callbacks: {
                        label: (ctx) => ` ${ctx.raw}% Positive Feedback`
                    }
                }
            }
        }
    });
}

// Update Charts when data changes
function updateCharts(analysis) {
    if (!analysis) return;
    const pcts = analysis.sentiment_percentages || { Positive: 0, Neutral: 0, Negative: 0 };
    if (sentimentChart) {
        sentimentChart.data.datasets[0].data = [pcts.Positive, pcts.Neutral, pcts.Negative];
        sentimentChart.update();
    }

    const aspects = analysis.aspect_breakdown || {};
    const aspectLabels = Object.keys(aspects);
    const aspectValues = aspectLabels.map(k => aspects[k].pos_ratio || 0);
    const aspectColors = aspectValues.map(v => v >= 65 ? "#10b981" : (v >= 45 ? "#f59e0b" : "#f43f5e"));

    if (aspectChart) {
        aspectChart.data.labels = aspectLabels;
        aspectChart.data.datasets[0].data = aspectValues;
        aspectChart.data.datasets[0].backgroundColor = aspectColors;
        aspectChart.update();
    }

    document.getElementById("chartPosPct").innerText = `${pcts.Positive}%`;
    document.getElementById("chartNeuPct").innerText = `${pcts.Neutral}%`;
    document.getElementById("chartNegPct").innerText = `${pcts.Negative}%`;
}

// Switch between pre-loaded sample businesses
async function switchSampleBusiness(bizId) {
    try {
        const res = await fetch(`/api/business/${bizId}`);
        if (!res.ok) throw new Error("Failed to fetch business data");
        const data = await res.json();
        renderCompleteDashboard(data.business, data.analysis, data.recommendations);
    } catch (err) {
        alert("Error loading business data: " + err.message);
    }
}

// Render the entire dashboard view with new data
function renderCompleteDashboard(business, analysis, recommendations) {
    currentBusiness = business;
    currentAnalysis = analysis;
    currentRecommendations = recommendations;

    // Header & Banner
    document.getElementById("bizName").innerText = business.name;
    document.getElementById("bizCategory").innerText = business.category;
    document.getElementById("bizLocation").innerText = business.location;
    document.getElementById("bizTwitter").innerText = business.twitter_handle;
    document.getElementById("bizExecutiveSummary").innerText = recommendations.summary;
    document.getElementById("bizGrade").innerText = recommendations.grade;
    document.getElementById("bizGradeDesc").innerText = recommendations.grade_desc;
    document.getElementById("bizScore").innerText = `${analysis.overall_sentiment_score}%`;

    // KPIs
    document.getElementById("kpiOverallScore").innerText = `${analysis.overall_sentiment_score}%`;
    document.getElementById("kpiNetPositive").innerText = `${analysis.sentiment_percentages.Positive}% Positive Ratio`;
    document.getElementById("kpiTotalReviews").innerText = analysis.total_reviews;
    document.getElementById("kpiGoogleCount").innerText = analysis.source_breakdown.google ? analysis.source_breakdown.google.total : 0;
    document.getElementById("kpiTwitterCount").innerText = analysis.source_breakdown.twitter ? analysis.source_breakdown.twitter.total : 0;
    document.getElementById("kpiNegativePct").innerText = `${analysis.sentiment_percentages.Negative}%`;
    document.getElementById("kpiNegativeCount").innerText = analysis.sentiment_counts.Negative;
    document.getElementById("kpiTopDriver").innerText = analysis.key_drivers.length > 0 ? analysis.key_drivers[0].word : "Service Quality";

    // Charts
    updateCharts(analysis);

    // Action Items
    const actionContainer = document.getElementById("actionItemsContainer");
    actionContainer.innerHTML = "";
    (recommendations.action_items || []).forEach(item => {
        let borderClass = "border-emerald-500/30 bg-emerald-950/20";
        let badgeClass = "bg-emerald-900/60 text-emerald-300 border border-emerald-500/40";
        if (item.priority === "High") {
            borderClass = "border-rose-500/30 bg-rose-950/20";
            badgeClass = "bg-rose-900/60 text-rose-300 border border-rose-500/40";
        } else if (item.priority === "Medium") {
            borderClass = "border-amber-500/30 bg-amber-950/20";
            badgeClass = "bg-amber-900/60 text-amber-300 border border-amber-500/40";
        }

        const div = document.createElement("div");
        div.className = `p-4 rounded-xl border ${borderClass} transition-all duration-300 hover:-translate-y-1 hover:shadow-xl`;
        div.innerHTML = `
            <div class="flex items-center justify-between mb-2">
                <span class="px-2.5 py-0.5 rounded-full text-[11px] font-bold ${badgeClass}">${item.priority} Priority</span>
                <span class="text-xs font-medium text-slate-400">${item.category}</span>
            </div>
            <h5 class="text-sm font-bold text-white mb-1.5">${item.title}</h5>
            <p class="text-xs text-slate-300 leading-relaxed">${item.details}</p>
        `;
        actionContainer.appendChild(div);
    });

    // Key Drivers
    const driversContainer = document.getElementById("keyDriversContainer");
    driversContainer.innerHTML = "";
    (analysis.key_drivers || []).forEach(d => {
        const span = document.createElement("span");
        span.className = "tag-chip inline-flex items-center px-3 py-1 rounded-xl text-xs font-medium bg-emerald-950/40 text-emerald-300 border border-emerald-500/30 shadow-sm";
        span.innerHTML = `<span class="w-1.5 h-1.5 rounded-full bg-emerald-400 mr-2 shadow-sm shadow-emerald-400"></span>${d.word} <span class="ml-1.5 text-emerald-400 font-bold">(${d.count})</span>`;
        driversContainer.appendChild(span);
    });

    // Pain Points
    const painContainer = document.getElementById("painPointsContainer");
    painContainer.innerHTML = "";
    (analysis.pain_points || []).forEach(p => {
        const span = document.createElement("span");
        span.className = "tag-chip inline-flex items-center px-3 py-1 rounded-xl text-xs font-medium bg-rose-950/40 text-rose-300 border border-rose-500/30 shadow-sm";
        span.innerHTML = `<span class="w-1.5 h-1.5 rounded-full bg-rose-400 mr-2 shadow-sm shadow-rose-400"></span>${p.word} <span class="ml-1.5 text-rose-400 font-bold">(${p.count})</span>`;
        painContainer.appendChild(span);
    });

    // Review Response Templates
    const templatesContainer = document.getElementById("responseTemplatesContainer");
    templatesContainer.innerHTML = "";
    (recommendations.response_templates || []).forEach(tmpl => {
        const div = document.createElement("div");
        div.className = "dark-glass rounded-xl p-4 border border-slate-800 flex flex-col justify-between hover-lift";
        div.innerHTML = `
            <div>
                <span class="text-xs font-bold text-indigo-400 block mb-1">${tmpl.scenario}</span>
                <p class="text-xs text-slate-400 mb-2 font-medium">${tmpl.subject}</p>
                <pre class="text-xs text-slate-300 bg-slate-950/90 p-3 rounded-xl border border-slate-800/90 whitespace-pre-wrap font-sans leading-relaxed select-all">${tmpl.template}</pre>
            </div>
            <button onclick="copyToClipboard(this)" class="btn-glow mt-3 inline-flex items-center justify-center px-3.5 py-1.5 rounded-xl text-xs font-bold bg-slate-800 text-slate-200 border border-slate-700 hover:bg-indigo-600 hover:text-white hover:border-indigo-500 transition">
                <i data-lucide="copy" class="w-3.5 h-3.5 mr-1.5"></i>
                Copy Response
            </button>
        `;
        templatesContainer.appendChild(div);
    });

    // Reviews List
    renderReviewsList(analysis.reviews);
    lucide.createIcons();
    applyCardHoverTilt();
}

// Render Review Feed Cards
function renderReviewsList(reviews) {
    const list = document.getElementById("reviewsList");
    list.innerHTML = "";

    reviews.forEach(r => {
        const card = document.createElement("div");
        card.className = "review-card p-4 rounded-xl border border-slate-800/80 transition-all duration-300";
        card.setAttribute("data-source", r.source);
        card.setAttribute("data-sentiment", r.sentiment);
        card.setAttribute("data-text", (r.text || "").toLowerCase());

        let badgeStyle = "bg-slate-800 text-slate-300 border-slate-700";
        if (r.sentiment === "Positive") badgeStyle = "bg-emerald-950/80 text-emerald-400 border-emerald-500/40 shadow-sm shadow-emerald-950";
        if (r.sentiment === "Negative") badgeStyle = "bg-rose-950/80 text-rose-400 border-rose-500/40 shadow-sm shadow-rose-950";

        const sourceBadge = r.source === "twitter"
            ? `<span class="inline-flex items-center px-2 py-0.5 rounded-lg text-xs font-semibold bg-sky-950/60 text-sky-400 border border-sky-800/50"><i data-lucide="twitter" class="w-3 h-3 mr-1"></i> Twitter</span>`
            : `<span class="inline-flex items-center px-2 py-0.5 rounded-lg text-xs font-semibold bg-amber-950/60 text-amber-400 border border-amber-800/50"><i data-lucide="globe" class="w-3 h-3 mr-1"></i> Google</span>`;

        let starsHtml = "";
        const starCount = r.rating || 4;
        for (let i = 0; i < starCount; i++) {
            starsHtml += `<i data-lucide="star" class="w-3.5 h-3.5 fill-current"></i>`;
        }

        let aspectsHtml = "";
        if (r.aspects) {
            Object.entries(r.aspects).forEach(([k, v]) => {
                let aspStyle = "bg-slate-800/60 text-slate-400 border border-slate-700/60";
                if (v.sentiment === "Positive") aspStyle = "bg-emerald-950/40 text-emerald-300 border border-emerald-500/30";
                if (v.sentiment === "Negative") aspStyle = "bg-rose-950/40 text-rose-300 border border-rose-500/30";
                aspectsHtml += `<span class="tag-chip text-xs px-2.5 py-0.5 rounded-lg font-medium ${aspStyle}">${k}: ${v.sentiment}</span>`;
            });
        }

        let emotionsHtml = "";
        if (r.emotions) {
            r.emotions.forEach(em => {
                emotionsHtml += `<span class="tag-chip text-xs px-2.5 py-0.5 rounded-lg font-medium bg-indigo-950/40 text-indigo-300 border border-indigo-500/30">💭 ${em}</span>`;
            });
        }

        card.innerHTML = `
            <div class="flex flex-wrap items-center justify-between gap-2 mb-2">
                <div class="flex items-center space-x-2">
                    ${sourceBadge}
                    <span class="text-xs font-bold text-white">${r.author}</span>
                    <span class="text-xs text-slate-500">• ${r.date || "Recent"}</span>
                </div>
                <div class="flex items-center space-x-2">
                    <div class="flex items-center text-amber-400 text-xs">${starsHtml}</div>
                    <span class="px-2.5 py-0.5 rounded-full text-xs font-bold border ${badgeStyle}">
                        ${r.sentiment} (${r.compound_score})
                    </span>
                </div>
            </div>
            <p class="text-xs sm:text-sm text-slate-200 leading-relaxed mb-3">"${r.text}"</p>
            <div class="flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-slate-800/60">
                <div class="flex flex-wrap items-center gap-1.5">
                    ${aspectsHtml}
                    ${emotionsHtml}
                </div>
                <button onclick="openReplyFromCard(this)" class="btn-glow text-xs text-indigo-400 hover:text-indigo-300 font-bold inline-flex items-center px-2.5 py-1 rounded-lg hover:bg-indigo-950/50 transition">
                    <i data-lucide="reply" class="w-3.5 h-3.5 mr-1"></i> Draft AI Reply
                </button>
            </div>
        `;
        list.appendChild(card);
    });
}

// Review Feed Filtering (Search + Platform + Sentiment)
function filterReviews() {
    const query = (document.getElementById("reviewSearchInput").value || "").toLowerCase();
    const platform = document.getElementById("platformFilter").value;
    const sentiment = document.getElementById("sentimentFilter").value;

    const cards = document.querySelectorAll(".review-card");
    cards.forEach(card => {
        const text = card.getAttribute("data-text");
        const src = card.getAttribute("data-source");
        const sent = card.getAttribute("data-sentiment");

        const matchesQuery = !query || text.includes(query);
        const matchesPlatform = platform === "all" || src === platform;
        const matchesSentiment = sentiment === "all" || sent === sentiment;

        if (matchesQuery && matchesPlatform && matchesSentiment) {
            card.classList.remove("hidden");
        } else {
            card.classList.add("hidden");
        }
    });
}

// Handle Scraper Modal Form Submission with visual progress animation
async function handleScrapeSubmit(e) {
    e.preventDefault();

    const name = document.getElementById("inputBizName").value.trim();
    const category = document.getElementById("inputCategory").value;
    const city = document.getElementById("inputCity").value.trim();
    const url = document.getElementById("inputUrl").value.trim();
    const manual = document.getElementById("inputManualReviews").value.trim();

    const progressBox = document.getElementById("scrapeProgressBox");
    const progressStep = document.getElementById("scrapeProgressStep");
    const progressPercent = document.getElementById("scrapeProgressPercent");
    const progressBar = document.getElementById("scrapeProgressBar");
    const submitBtn = document.getElementById("scrapeSubmitBtn");

    progressBox.classList.remove("hidden");
    submitBtn.disabled = true;

    // Step 1
    progressStep.innerHTML = `<i data-lucide="loader" class="w-4 h-4 mr-1.5 animate-spin"></i> Connecting to Google Reviews & Twitter/X scrapers...`;
    progressPercent.innerText = "30%";
    progressBar.style.width = "30%";
    lucide.createIcons();

    try {
        // Step 2 timer
        setTimeout(() => {
            progressStep.innerHTML = `<i data-lucide="loader" class="w-4 h-4 mr-1.5 animate-spin"></i> Parsing customer feedback & extracting keywords...`;
            progressPercent.innerText = "65%";
            progressBar.style.width = "65%";
            lucide.createIcons();
        }, 500);

        const response = await fetch("/api/scrape-and-analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                business_name: name,
                category: category,
                city: city,
                url: url,
                manual_reviews: manual
            })
        });

        // Step 3
        progressStep.innerHTML = `<i data-lucide="loader" class="w-4 h-4 mr-1.5 animate-spin"></i> Running VADER & Aspect-Based Sentiment analysis...`;
        progressPercent.innerText = "88%";
        progressBar.style.width = "88%";
        lucide.createIcons();

        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.error || "Scraping failed");
        }

        const data = await response.json();

        // Step 4: Done
        progressPercent.innerText = "100%";
        progressBar.style.width = "100%";
        progressStep.innerHTML = `<span class="text-emerald-400 font-bold">✓ Analysis complete!</span>`;

        setTimeout(() => {
            renderCompleteDashboard(data.business, data.analysis, data.recommendations);
            closeModal("scrapeModal");
            progressBox.classList.add("hidden");
            submitBtn.disabled = false;
        }, 400);

    } catch (err) {
        alert("Scraping error: " + err.message);
        progressBox.classList.add("hidden");
        submitBtn.disabled = false;
    }
}

// Single Review Tester
async function runSingleReviewAnalysis() {
    const text = document.getElementById("singleTestText").value.trim();
    const rating = document.getElementById("singleTestRating").value;

    if (!text) {
        alert("Please enter a review sentence or tweet to analyze.");
        return;
    }

    try {
        const res = await fetch("/api/analyze-single", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text, rating })
        });
        const data = await res.json();

        const resultsBox = document.getElementById("singleTestResults");
        resultsBox.classList.remove("hidden");

        const badge = document.getElementById("singleSentimentBadge");
        badge.innerText = `${data.sentiment} (${data.compound_score})`;
        if (data.sentiment === "Positive") {
            badge.className = "px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-950/80 text-emerald-400 border border-emerald-500/40 shadow-sm shadow-emerald-950";
        } else if (data.sentiment === "Negative") {
            badge.className = "px-2.5 py-0.5 rounded-full text-xs font-bold bg-rose-950/80 text-rose-400 border border-rose-500/40 shadow-sm shadow-rose-950";
        } else {
            badge.className = "px-2.5 py-0.5 rounded-full text-xs font-bold bg-slate-800 text-slate-300 border border-slate-700";
        }

        document.getElementById("singleScorePos").innerText = data.scores.pos;
        document.getElementById("singleScoreNeu").innerText = data.scores.neu;
        document.getElementById("singleScoreNeg").innerText = data.scores.neg;

        // Aspects
        const aspDiv = document.getElementById("singleAspectsList");
        aspDiv.innerHTML = "";
        if (data.aspects && Object.keys(data.aspects).length > 0) {
            Object.entries(data.aspects).forEach(([k, v]) => {
                const sp = document.createElement("span");
                sp.className = `tag-chip px-2 py-0.5 rounded-lg font-medium text-xs ${v.sentiment === 'Positive' ? 'bg-emerald-950/40 text-emerald-300 border border-emerald-500/30' : 'bg-rose-950/40 text-rose-300 border border-rose-500/30'}`;
                sp.innerText = `${k}: ${v.sentiment}`;
                aspDiv.appendChild(sp);
            });
        } else {
            aspDiv.innerHTML = `<span class="text-slate-500 italic text-xs">No specific service aspect keywords detected.</span>`;
        }

        // Suggested Reply
        document.getElementById("singleReplyDraft").innerText = data.suggested_reply;

    } catch (err) {
        alert("Analysis error: " + err.message);
    }
}

// Open reply modal directly from card element
function openReplyFromCard(btn) {
    const card = btn.closest(".review-card");
    if (!card) return;
    const authorEl = card.querySelector(".text-white");
    const author = authorEl ? authorEl.innerText.trim() : "Customer";
    const sentiment = card.getAttribute("data-sentiment") || "Neutral";
    const pEl = card.querySelector("p");
    const reviewText = pEl ? pEl.innerText.replace(/^"|"$/g, '').trim() : "";
    openInstantReply(author, sentiment, reviewText);
}

// Open Instant Tailored Reply Modal for a review
function openInstantReply(author, sentiment, reviewText) {
    document.getElementById("replyAuthor").innerText = author;
    document.getElementById("replyOriginalText").innerText = reviewText;

    let draft = "";
    const bName = currentBusiness.name || "Our Business";

    if (sentiment === "Negative") {
        draft = `Hello ${author},\n\nThank you for reaching out and sharing your feedback. We are deeply sorry that your experience with us at ${bName} was unsatisfactory. This does not reflect the quality standard we strive for.\n\nWe would love the chance to make this right. Please contact our manager at manager@${(bName.toLowerCase().replace(/[^a-z0-9]/g, ''))}.com so we can resolve this for you immediately.\n\nBest regards,\nCustomer Care Team`;
    } else if (sentiment === "Positive") {
        draft = `Hi ${author}!\n\nThank you so much for the fantastic feedback! We are thrilled to hear you had such a wonderful experience at ${bName}. Our team works hard to deliver the best service, and notes like yours make it all worthwhile.\n\nLooking forward to seeing you again soon!\n\nWarmly,\nThe ${bName} Team`;
    } else {
        draft = `Hello ${author},\n\nThank you for taking the time to review ${bName}. We appreciate your balanced comments and are continuously working to improve our service flow. If there is anything specific we can do for you, please let us know!\n\nSincerely,\nThe Management Team`;
    }

    document.getElementById("replyTextarea").value = draft;
    document.getElementById("replyCopyStatus").classList.add("hidden");
    openModal("replyModal");
}

function copyReplyText() {
    const text = document.getElementById("replyTextarea").value;
    navigator.clipboard.writeText(text).then(() => {
        const status = document.getElementById("replyCopyStatus");
        status.classList.remove("hidden");
        setTimeout(() => status.classList.add("hidden"), 2500);
    });
}

function copyToClipboard(button) {
    const pre = button.parentElement.querySelector("pre");
    if (pre) {
        navigator.clipboard.writeText(pre.innerText).then(() => {
            const original = button.innerHTML;
            button.innerHTML = `<span class="text-emerald-400 font-bold">✓ Copied!</span>`;
            setTimeout(() => button.innerHTML = original, 2000);
        });
    }
}

// Export Audit Report JSON
function exportAuditReportJSON() {
    const report = {
        title: "Local Business Review Sentiment Audit & Recommendations Report",
        generated_at: new Date().toISOString(),
        business: currentBusiness,
        analysis_summary: {
            overall_sentiment_score: currentAnalysis.overall_sentiment_score,
            total_reviews: currentAnalysis.total_reviews,
            percentages: currentAnalysis.sentiment_percentages,
            aspect_breakdown: currentAnalysis.aspect_breakdown,
            top_drivers: currentAnalysis.key_drivers,
            pain_points: currentAnalysis.pain_points
        },
        ai_recommendations: currentRecommendations
    };

    const blob = new Blob([JSON.stringify(report, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${(currentBusiness.name || 'business').toLowerCase().replace(/\s+/g, '_')}_sentiment_audit.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Modal Helpers
function openModal(id) {
    const modal = document.getElementById(id);
    if (modal) modal.classList.remove("hidden");
    lucide.createIcons();
}

function closeModal(id) {
    const modal = document.getElementById(id);
    if (modal) modal.classList.add("hidden");
}

// Initialize all 11 survey charts with dark theme aesthetics
function initSurveyCharts() {
    if (!window.SURVEY_METRICS || !window.SURVEY_METRICS.questions) return;
    
    window.SURVEY_METRICS.questions.forEach(q => {
        const canvasId = `survey_chart_${q.id}`;
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;
        const ctx = canvas.getContext("2d");
        
        new Chart(ctx, {
            type: "doughnut",
            data: {
                labels: q.data.map(d => d.label),
                datasets: [{
                    data: q.data.map(d => d.percentage),
                    backgroundColor: q.data.map(d => d.color),
                    borderWidth: 2,
                    borderColor: "#111827",
                    hoverBorderColor: "#ffffff",
                    hoverOffset: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: "64%",
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: "rgba(15, 23, 42, 0.95)",
                        titleColor: "#ffffff",
                        bodyColor: "#cbd5e1",
                        borderColor: "rgba(99, 102, 241, 0.3)",
                        borderWidth: 1,
                        padding: 8,
                        callbacks: {
                            label: (ctx) => ` ${ctx.label}: ${ctx.raw}%`
                        }
                    }
                }
            }
        });
    });
}

// Switch between Business Sentiment Dashboard & Field Survey Analytics
function switchDashboardTab(tabName) {
    const sentimentSec = document.getElementById("sentimentDashboardSection");
    const surveySec = document.getElementById("surveyDashboardSection");
    const btnSentiment = document.getElementById("tabBtnSentiment");
    const btnSurvey = document.getElementById("tabBtnSurvey");

    if (tabName === "survey") {
        sentimentSec.classList.add("hidden");
        surveySec.classList.remove("hidden");
        btnSurvey.classList.add("bg-indigo-600", "text-white", "shadow-lg", "shadow-indigo-600/30");
        btnSurvey.classList.remove("text-slate-400");
        btnSentiment.classList.remove("bg-indigo-600", "text-white", "shadow-lg", "shadow-indigo-600/30");
        btnSentiment.classList.add("text-slate-400");
    } else {
        surveySec.classList.add("hidden");
        sentimentSec.classList.remove("hidden");
        btnSentiment.classList.add("bg-indigo-600", "text-white", "shadow-lg", "shadow-indigo-600/30");
        btnSentiment.classList.remove("text-slate-400");
        btnSurvey.classList.remove("bg-indigo-600", "text-white", "shadow-lg", "shadow-indigo-600/30");
        btnSurvey.classList.add("text-slate-400");
    }
    applyCardHoverTilt();
    lucide.createIcons();
}

// Category filter for the survey cards
function filterSurveyCards(category) {
    const buttons = document.querySelectorAll(".survey-filter-btn");
    buttons.forEach(b => {
        if (b.getAttribute("data-cat") === category) {
            b.classList.add("bg-indigo-600", "text-white", "border-indigo-500");
            b.classList.remove("bg-slate-900/80", "text-slate-400", "border-slate-800");
        } else {
            b.classList.remove("bg-indigo-600", "text-white", "border-indigo-500");
            b.classList.add("bg-slate-900/80", "text-slate-400", "border-slate-800");
        }
    });

    const cards = document.querySelectorAll(".survey-question-card");
    cards.forEach(c => {
        const cat = c.getAttribute("data-category");
        if (category === "all" || cat === category) {
            c.classList.remove("hidden");
        } else {
            c.classList.add("hidden");
        }
    });
}

