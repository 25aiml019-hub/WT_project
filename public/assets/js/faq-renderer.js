/**
 * StudentHub - FAQ Dynamic Renderer
 * Course: AIUE203 - Web Development Fundamentals (Practical 6)
 * Author: Anshika Badala (25AIML002), CSPIT, CHARUSAT
 */

document.addEventListener("DOMContentLoaded", function () {
    const container = document.getElementById("faq-app");
    if (!container) return;

    const DATA_URL = "../assets/data/faqs.json";
    const CACHE_KEY = "studenthub_faqs_cache";
    const PAGE_SIZE = 6;

    // State
    let rawFaqs = [];
    let filteredFaqs = [];
    let currentPage = 1;
    let searchQuery = "";
    let selectedCategory = "all";
    let isDataCached = false;
    let cacheTimestamp = null;
    const expandedFaqIds = new Set(); // Tracks currently opened accordions

    container.textContent = "";

    // Live Region
    const liveAnnouncer = document.createElement("div");
    liveAnnouncer.setAttribute("aria-live", "polite");
    liveAnnouncer.style.position = "absolute";
    liveAnnouncer.style.width = "1px";
    liveAnnouncer.style.height = "1px";
    liveAnnouncer.style.overflow = "hidden";
    liveAnnouncer.style.clip = "rect(0,0,0,0)";
    container.appendChild(liveAnnouncer);

    // 1. Control Bar
    const controlBar = document.createElement("div");
    controlBar.className = "control-bar";
    controlBar.setAttribute("role", "search");
    controlBar.setAttribute("aria-label", "Search and filter frequently asked questions");

    // Search Input
    const searchGroup = document.createElement("div");
    searchGroup.className = "control-group";
    searchGroup.style.flex = "2 1 250px";
    const searchLabel = document.createElement("label");
    searchLabel.htmlFor = "faq-search";
    searchLabel.textContent = "Search FAQ:";
    const searchInput = document.createElement("input");
    searchInput.type = "text";
    searchInput.id = "faq-search";
    searchInput.placeholder = "Search questions and answers...";
    searchGroup.appendChild(searchLabel);
    searchGroup.appendChild(searchInput);
    controlBar.appendChild(searchGroup);

    // Category Filter
    const catGroup = document.createElement("div");
    catGroup.className = "control-group";
    const catLabel = document.createElement("label");
    catLabel.htmlFor = "faq-category";
    catLabel.textContent = "Category:";
    const catSelect = document.createElement("select");
    catSelect.id = "faq-category";
    const categories = ["all", "General", "Admissions", "Academics", "Campus Life", "Administrative"];
    categories.forEach((cat) => {
        const opt = document.createElement("option");
        opt.value = cat;
        opt.textContent = cat === "all" ? "All Categories" : cat;
        catSelect.appendChild(opt);
    });
    catGroup.appendChild(catLabel);
    catGroup.appendChild(catSelect);
    controlBar.appendChild(catGroup);

    // Action Buttons
    const actionsGroup = document.createElement("div");
    actionsGroup.className = "control-actions";

    const resetBtn = document.createElement("button");
    resetBtn.type = "button";
    resetBtn.className = "btn btn-secondary";
    resetBtn.textContent = "Reset Filters";
    actionsGroup.appendChild(resetBtn);

    const refreshBtn = document.createElement("button");
    refreshBtn.type = "button";
    refreshBtn.className = "btn";
    refreshBtn.textContent = "Refresh Data";
    actionsGroup.appendChild(refreshBtn);

    controlBar.appendChild(actionsGroup);
    container.appendChild(controlBar);

    // 2. Status Bar
    const statusBar = document.createElement("div");
    statusBar.className = "status-bar";

    const countSpan = document.createElement("span");
    countSpan.className = "result-count";
    countSpan.textContent = "Loading FAQs...";
    statusBar.appendChild(countSpan);

    const badgeSpan = document.createElement("span");
    badgeSpan.className = "data-badge live";
    badgeSpan.textContent = "Connecting...";
    statusBar.appendChild(badgeSpan);

    container.appendChild(statusBar);

    // 3. Content Area
    const contentArea = document.createElement("div");
    contentArea.className = "content-area";
    container.appendChild(contentArea);

    // 4. Pagination Area
    const paginationWrapper = document.createElement("div");
    container.appendChild(paginationWrapper);

    /**
     * Load FAQ dataset
     */
    async function loadData(forceRefresh = false) {
        showLoading();
        try {
            const result = await DataLoader.fetchDataset(DATA_URL, CACHE_KEY, { forceRefresh });
            rawFaqs = result.data;
            isDataCached = result.fromCache;
            cacheTimestamp = result.timestamp;
            updateStatusBadge();
            applyFiltersAndRender(true);
        } catch (err) {
            showError(err.message);
        }
    }

    function updateStatusBadge() {
        badgeSpan.className = "data-badge " + (isDataCached ? "cached" : "live");
        const timeStr = cacheTimestamp ? new Date(cacheTimestamp).toLocaleTimeString() : "";
        badgeSpan.textContent = isDataCached ? `Cached Data (${timeStr})` : `Live Data (${timeStr})`;
    }

    function showLoading() {
        contentArea.textContent = "";
        paginationWrapper.textContent = "";
        countSpan.textContent = "Fetching FAQ dataset...";

        const loadingDiv = document.createElement("div");
        loadingDiv.className = "loading-state";
        loadingDiv.setAttribute("role", "status");

        const spinner = document.createElement("div");
        spinner.className = "spinner";
        loadingDiv.appendChild(spinner);

        const text = document.createElement("p");
        text.textContent = "Loading FAQs via Fetch API...";
        loadingDiv.appendChild(text);

        contentArea.appendChild(loadingDiv);
    }

    function showError(message) {
        contentArea.textContent = "";
        paginationWrapper.textContent = "";
        countSpan.textContent = "Failed to load FAQs.";

        badgeSpan.className = "data-badge error";
        badgeSpan.textContent = "Fetch Failed";

        const errDiv = document.createElement("div");
        errDiv.className = "error-state";
        errDiv.setAttribute("role", "alert");

        const h3 = document.createElement("h3");
        h3.textContent = "Unable to load FAQs";
        errDiv.appendChild(h3);

        const p = document.createElement("p");
        p.textContent = message;
        errDiv.appendChild(p);

        const retry = document.createElement("button");
        retry.type = "button";
        retry.className = "btn";
        retry.textContent = "Retry Connection";
        retry.addEventListener("click", () => loadData(true));
        errDiv.appendChild(retry);

        contentArea.appendChild(errDiv);
    }

    /**
     * Filter & Paginate
     */
    function applyFiltersAndRender(resetPage = false) {
        if (resetPage) {
            currentPage = 1;
        }

        const query = searchQuery.toLowerCase().trim();

        filteredFaqs = rawFaqs.filter((faqItem) => {
            const matchQ = (faqItem.question || "").toLowerCase().includes(query);
            const matchA = (faqItem.answer || "").toLowerCase().includes(query);
            const matchSearch = query === "" || matchQ || matchA;

            const matchCat = selectedCategory === "all" ||
                (faqItem.category || "").toLowerCase() === selectedCategory.toLowerCase();

            return matchSearch && matchCat;
        });

        renderView();
    }

    function renderView() {
        contentArea.textContent = "";
        paginationWrapper.textContent = "";

        const total = filteredFaqs.length;
        countSpan.textContent = `Showing ${total} question${total === 1 ? "" : "s"} (filtered from ${rawFaqs.length} total)`;
        liveAnnouncer.textContent = `FAQ list updated. ${total} questions available.`;

        if (total === 0) {
            const emptyDiv = document.createElement("div");
            emptyDiv.className = "empty-state";

            const h3 = document.createElement("h3");
            h3.textContent = "No matching FAQs found";
            emptyDiv.appendChild(h3);

            const p = document.createElement("p");
            p.textContent = "Try searching with different keywords or choosing another category.";
            emptyDiv.appendChild(p);

            const clearBtn = document.createElement("button");
            clearBtn.type = "button";
            clearBtn.className = "btn";
            clearBtn.textContent = "Clear All Filters";
            clearBtn.addEventListener("click", resetAllFilters);
            emptyDiv.appendChild(clearBtn);

            contentArea.appendChild(emptyDiv);
            return;
        }

        const paginated = Paginator.paginate(filteredFaqs, currentPage, PAGE_SIZE);
        currentPage = paginated.currentPage;

        // Render Accessible Accordions
        paginated.items.forEach((faqItem) => {
            const faqContainer = document.createElement("div");
            faqContainer.className = "faq-container";

            const isExpanded = expandedFaqIds.has(faqItem.id);
            const answerId = `faq-answer-${faqItem.id}`;
            const buttonId = `faq-btn-${faqItem.id}`;

            const questionBtn = document.createElement("button");
            questionBtn.type = "button";
            questionBtn.id = buttonId;
            questionBtn.className = "faq-question-btn";
            questionBtn.setAttribute("aria-expanded", isExpanded ? "true" : "false");
            questionBtn.setAttribute("aria-controls", answerId);

            // Question Text & Category Tag
            const titleSpan = document.createElement("span");
            titleSpan.textContent = (faqItem.id <= 5 ? `Q${faqItem.id}: ` : "") + faqItem.question;
            questionBtn.appendChild(titleSpan);

            if (faqItem.category) {
                const tag = document.createElement("span");
                tag.style.float = "right";
                tag.style.fontSize = "12px";
                tag.style.padding = "2px 8px";
                tag.style.borderRadius = "4px";
                tag.style.backgroundColor = "var(--hover-bg)";
                tag.style.color = "var(--primary-color)";
                tag.textContent = faqItem.category;
                questionBtn.appendChild(tag);
            }

            const answerDiv = document.createElement("div");
            answerDiv.id = answerId;
            answerDiv.className = "faq-answer";
            answerDiv.setAttribute("role", "region");
            answerDiv.setAttribute("aria-labelledby", buttonId);
            answerDiv.style.display = isExpanded ? "block" : "none";
            answerDiv.textContent = faqItem.answer;

            // Toggle Accordion Click Handler
            questionBtn.addEventListener("click", () => {
                if (expandedFaqIds.has(faqItem.id)) {
                    expandedFaqIds.delete(faqItem.id);
                    answerDiv.style.display = "none";
                    questionBtn.setAttribute("aria-expanded", "false");
                } else {
                    expandedFaqIds.add(faqItem.id);
                    answerDiv.style.display = "block";
                    questionBtn.setAttribute("aria-expanded", "true");
                }
            });

            faqContainer.appendChild(questionBtn);
            faqContainer.appendChild(answerDiv);
            contentArea.appendChild(faqContainer);
        });

        // Pagination Controls
        if (paginated.totalPages > 1) {
            const paginationNav = Paginator.renderControls(paginated, (newPage) => {
                currentPage = newPage;
                renderView();
                controlBar.scrollIntoView({ behavior: "smooth", block: "start" });
            });
            paginationWrapper.appendChild(paginationNav);
        }
    }

    function resetAllFilters() {
        searchQuery = "";
        searchInput.value = "";
        selectedCategory = "all";
        catSelect.value = "all";
        applyFiltersAndRender(true);
    }

    // Event Listeners
    searchInput.addEventListener("input", (e) => {
        searchQuery = e.target.value;
        applyFiltersAndRender(true);
    });

    catSelect.addEventListener("change", (e) => {
        selectedCategory = e.target.value;
        applyFiltersAndRender(true);
    });

    resetBtn.addEventListener("click", resetAllFilters);
    refreshBtn.addEventListener("click", () => loadData(true));

    // Initial Load
    loadData();
});
