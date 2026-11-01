/**
 * StudentHub - Events Dynamic Renderer
 * Course: AIUE203 - Web Development Fundamentals (Practical 6)
 * Author: Daksh Harkhani (25AIML019), CSPIT, CHARUSAT
 */

document.addEventListener("DOMContentLoaded", function () {
    const container = document.getElementById("events-app");
    if (!container) return;

    const DATA_URL = "../assets/data/events.json";
    const CACHE_KEY = "studenthub_events_cache";
    const PAGE_SIZE = 5;

    // State
    let rawEvents = [];
    let filteredEvents = [];
    let currentPage = 1;
    let searchQuery = "";
    let selectedCategory = "all";
    let selectedStatus = "all";
    let selectedSort = "date-asc";
    let isDataCached = false;
    let cacheTimestamp = null;

    // Build Static UI Scaffolding
    container.textContent = ""; // Clear existing fallback

    // Live Region for Screen Readers
    const liveAnnouncer = document.createElement("div");
    liveAnnouncer.setAttribute("aria-live", "polite");
    liveAnnouncer.className = "visually-hidden";
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
    controlBar.setAttribute("aria-label", "Search and filter events");

    // Search Input
    const searchGroup = document.createElement("div");
    searchGroup.className = "control-group";
    const searchLabel = document.createElement("label");
    searchLabel.htmlFor = "events-search";
    searchLabel.textContent = "Search Events:";
    const searchInput = document.createElement("input");
    searchInput.type = "text";
    searchInput.id = "events-search";
    searchInput.placeholder = "Search by title or description...";
    searchGroup.appendChild(searchLabel);
    searchGroup.appendChild(searchInput);
    controlBar.appendChild(searchGroup);

    // Category Filter
    const catGroup = document.createElement("div");
    catGroup.className = "control-group";
    const catLabel = document.createElement("label");
    catLabel.htmlFor = "events-category";
    catLabel.textContent = "Category:";
    const catSelect = document.createElement("select");
    catSelect.id = "events-category";
    const catOptions = ["all", "Technical", "Cultural", "Sports", "Academic", "Workshop"];
    catOptions.forEach((cat) => {
        const opt = document.createElement("option");
        opt.value = cat;
        opt.textContent = cat === "all" ? "All Categories" : cat;
        catSelect.appendChild(opt);
    });
    catGroup.appendChild(catLabel);
    catGroup.appendChild(catSelect);
    controlBar.appendChild(catGroup);

    // Status Filter
    const statusGroup = document.createElement("div");
    statusGroup.className = "control-group";
    const statusLabel = document.createElement("label");
    statusLabel.htmlFor = "events-status";
    statusLabel.textContent = "Status:";
    const statusSelect = document.createElement("select");
    statusSelect.id = "events-status";
    const statusOptions = ["all", "Upcoming", "Ongoing", "Completed"];
    statusOptions.forEach((st) => {
        const opt = document.createElement("option");
        opt.value = st;
        opt.textContent = st === "all" ? "All Statuses" : st;
        statusSelect.appendChild(opt);
    });
    statusGroup.appendChild(statusLabel);
    statusGroup.appendChild(statusSelect);
    controlBar.appendChild(statusGroup);

    // Sort Dropdown
    const sortGroup = document.createElement("div");
    sortGroup.className = "control-group";
    const sortLabel = document.createElement("label");
    sortLabel.htmlFor = "events-sort";
    sortLabel.textContent = "Sort By:";
    const sortSelect = document.createElement("select");
    sortSelect.id = "events-sort";
    const sortOptions = [
        { value: "date-asc", label: "Date (Earliest First)" },
        { value: "date-desc", label: "Date (Latest First)" },
        { value: "title-asc", label: "Title (A to Z)" },
        { value: "title-desc", label: "Title (Z to A)" }
    ];
    sortOptions.forEach((s) => {
        const opt = document.createElement("option");
        opt.value = s.value;
        opt.textContent = s.label;
        sortSelect.appendChild(opt);
    });
    sortGroup.appendChild(sortLabel);
    sortGroup.appendChild(sortSelect);
    controlBar.appendChild(sortGroup);

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

    // 2. Status Bar (Counters + Badges)
    const statusBar = document.createElement("div");
    statusBar.className = "status-bar";

    const countSpan = document.createElement("span");
    countSpan.className = "result-count";
    countSpan.textContent = "Loading events...";
    statusBar.appendChild(countSpan);

    const badgeSpan = document.createElement("span");
    badgeSpan.className = "data-badge live";
    badgeSpan.textContent = "Connecting...";
    statusBar.appendChild(badgeSpan);

    container.appendChild(statusBar);

    // 3. Content Viewport Container
    const contentArea = document.createElement("div");
    contentArea.className = "content-area";
    container.appendChild(contentArea);

    // 4. Pagination Container
    const paginationWrapper = document.createElement("div");
    container.appendChild(paginationWrapper);

    /**
     * Load Dataset using DataLoader
     */
    async function loadData(forceRefresh = false) {
        showLoading();
        try {
            const result = await DataLoader.fetchDataset(DATA_URL, CACHE_KEY, { forceRefresh });
            rawEvents = result.data;
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
        countSpan.textContent = "Fetching events dataset...";

        const loadingDiv = document.createElement("div");
        loadingDiv.className = "loading-state";
        loadingDiv.setAttribute("role", "status");

        const spinner = document.createElement("div");
        spinner.className = "spinner";
        loadingDiv.appendChild(spinner);

        const text = document.createElement("p");
        text.textContent = "Loading campus events via Fetch API...";
        loadingDiv.appendChild(text);

        contentArea.appendChild(loadingDiv);
    }

    function showError(message) {
        contentArea.textContent = "";
        paginationWrapper.textContent = "";
        countSpan.textContent = "Failed to load events.";

        badgeSpan.className = "data-badge error";
        badgeSpan.textContent = "Fetch Failed";

        const errDiv = document.createElement("div");
        errDiv.className = "error-state";
        errDiv.setAttribute("role", "alert");

        const h3 = document.createElement("h3");
        h3.textContent = "Unable to load events data";
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
     * Filter, Sort, and Paginate
     */
    function applyFiltersAndRender(resetPage = false) {
        if (resetPage) {
            currentPage = 1;
        }

        const query = searchQuery.toLowerCase().trim();

        filteredEvents = rawEvents.filter((ev) => {
            const matchTitle = (ev.title || "").toLowerCase().includes(query);
            const matchDesc = (ev.description || "").toLowerCase().includes(query);
            const matchSearch = query === "" || matchTitle || matchDesc;

            const matchCategory = selectedCategory === "all" ||
                (ev.category || "").toLowerCase() === selectedCategory.toLowerCase();

            const matchStatus = selectedStatus === "all" ||
                (ev.status || "").toLowerCase() === selectedStatus.toLowerCase();

            return matchSearch && matchCategory && matchStatus;
        });

        // Sorting
        filteredEvents.sort((a, b) => {
            switch (selectedSort) {
                case "date-asc":
                    return (a.date || "").localeCompare(b.date || "");
                case "date-desc":
                    return (b.date || "").localeCompare(a.date || "");
                case "title-asc":
                    return (a.title || "").localeCompare(b.title || "");
                case "title-desc":
                    return (b.title || "").localeCompare(a.title || "");
                default:
                    return 0;
            }
        });

        renderView();
    }

    /**
     * Render the table and pagination controls safely
     */
    function renderView() {
        contentArea.textContent = "";
        paginationWrapper.textContent = "";

        const total = filteredEvents.length;
        countSpan.textContent = `Showing ${total} event${total === 1 ? "" : "s"} (filtered from ${rawEvents.length} total)`;
        liveAnnouncer.textContent = `Event list updated. ${total} events available.`;

        if (total === 0) {
            const emptyDiv = document.createElement("div");
            emptyDiv.className = "empty-state";

            const h3 = document.createElement("h3");
            h3.textContent = "No matching events found";
            emptyDiv.appendChild(h3);

            const p = document.createElement("p");
            p.textContent = "Try adjusting your search terms or clearing the category and status filters.";
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

        // Apply Pagination
        const paginated = Paginator.paginate(filteredEvents, currentPage, PAGE_SIZE);
        currentPage = paginated.currentPage;

        // Render Semantic Table
        const table = document.createElement("table");
        table.className = "data-table events-table";
        table.setAttribute("aria-label", "Campus Events Schedule");

        const thead = document.createElement("thead");
        const headerRow = document.createElement("tr");
        ["Event Title", "Category", "Date & Time", "Venue", "Status", "Details"].forEach((heading) => {
            const th = document.createElement("th");
            th.textContent = heading;
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);
        table.appendChild(thead);

        const tbody = document.createElement("tbody");
        paginated.items.forEach((eventItem) => {
            const tr = document.createElement("tr");

            // Title & Description Cell
            const tdTitle = document.createElement("td");
            tdTitle.style.textAlign = "left";
            const titleBold = document.createElement("strong");
            titleBold.textContent = eventItem.title;
            tdTitle.appendChild(titleBold);
            if (eventItem.description) {
                const descP = document.createElement("div");
                descP.style.fontSize = "13px";
                descP.style.color = "var(--text-muted)";
                descP.style.marginTop = "4px";
                descP.textContent = eventItem.description;
                tdTitle.appendChild(descP);
            }
            tr.appendChild(tdTitle);

            // Category Cell
            const tdCat = document.createElement("td");
            tdCat.textContent = eventItem.category || "General";
            tr.appendChild(tdCat);

            // Date & Time Cell
            const tdDate = document.createElement("td");
            const dateSpan = document.createElement("div");
            dateSpan.style.fontWeight = "600";
            dateSpan.textContent = eventItem.date || "";
            tdDate.appendChild(dateSpan);
            if (eventItem.time) {
                const timeSpan = document.createElement("div");
                timeSpan.style.fontSize = "12px";
                timeSpan.style.color = "var(--text-muted)";
                timeSpan.textContent = eventItem.time;
                tdDate.appendChild(timeSpan);
            }
            tr.appendChild(tdDate);

            // Venue Cell
            const tdVenue = document.createElement("td");
            tdVenue.textContent = eventItem.venue || "Campus";
            tr.appendChild(tdVenue);

            // Status Cell
            const tdStatus = document.createElement("td");
            const pill = document.createElement("span");
            const statusKey = (eventItem.status || "upcoming").toLowerCase();
            pill.className = `status-pill ${statusKey}`;
            pill.textContent = eventItem.status || "Upcoming";
            tdStatus.appendChild(pill);
            tr.appendChild(tdStatus);

            // Action / Details Cell
            const tdAction = document.createElement("td");
            const detailBtn = document.createElement("button");
            detailBtn.type = "button";
            detailBtn.className = "btn-view-details";
            detailBtn.textContent = "View Details";
            detailBtn.addEventListener("click", () => openEventModal(eventItem));
            tdAction.appendChild(detailBtn);
            tr.appendChild(tdAction);

            tbody.appendChild(tr);
        });
        table.appendChild(tbody);
        contentArea.appendChild(table);

        // Render Pagination Controls
        if (paginated.totalPages > 1) {
            const paginationNav = Paginator.renderControls(paginated, (newPage) => {
                currentPage = newPage;
                renderView();
                table.scrollIntoView({ behavior: "smooth", block: "start" });
            });
            paginationWrapper.appendChild(paginationNav);
        }
    }

    function resetAllFilters() {
        searchQuery = "";
        searchInput.value = "";
        selectedCategory = "all";
        catSelect.value = "all";
        selectedStatus = "all";
        statusSelect.value = "all";
        selectedSort = "date-asc";
        sortSelect.value = "date-asc";
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

    statusSelect.addEventListener("change", (e) => {
        selectedStatus = e.target.value;
        applyFiltersAndRender(true);
    });

    sortSelect.addEventListener("change", (e) => {
        selectedSort = e.target.value;
        applyFiltersAndRender(false);
    });

    resetBtn.addEventListener("click", resetAllFilters);

    refreshBtn.addEventListener("click", () => {
        loadData(true);
    });

    /**
     * Accessible Event Details Modal Dialog
     * Strictly uses DOM APIs to preserve Practical 6 compliance
     */
    function openEventModal(eventItem) {
        // Remove existing modal if open
        const existing = document.querySelector(".event-modal-backdrop");
        if (existing) existing.remove();

        const backdrop = document.createElement("div");
        backdrop.className = "event-modal-backdrop";
        backdrop.setAttribute("role", "dialog");
        backdrop.setAttribute("aria-modal", "true");
        backdrop.setAttribute("aria-labelledby", "event-modal-title");

        const dialog = document.createElement("div");
        dialog.className = "event-modal-dialog";

        // Header
        const header = document.createElement("div");
        header.className = "event-modal-header";

        const titleBox = document.createElement("div");
        const title = document.createElement("h3");
        title.id = "event-modal-title";
        title.textContent = eventItem.title;
        titleBox.appendChild(title);

        const statusBadge = document.createElement("span");
        statusBadge.className = `status-pill ${(eventItem.status || "upcoming").toLowerCase()}`;
        statusBadge.textContent = eventItem.status || "Upcoming";
        titleBox.appendChild(statusBadge);

        const closeBtn = document.createElement("button");
        closeBtn.type = "button";
        closeBtn.className = "event-modal-close-btn";
        closeBtn.setAttribute("aria-label", "Close dialog");
        closeBtn.textContent = "×";
        closeBtn.addEventListener("click", () => backdrop.remove());

        header.appendChild(titleBox);
        header.appendChild(closeBtn);
        dialog.appendChild(header);

        // Body
        const body = document.createElement("div");
        body.className = "event-modal-body";

        // Alert box for registration messages
        const alertBox = document.createElement("div");
        alertBox.className = "event-modal-alert";
        body.appendChild(alertBox);

        // Meta Grid
        const metaGrid = document.createElement("div");
        metaGrid.className = "event-modal-meta-grid";

        const metaItems = [
            { label: "Date", value: eventItem.date || "TBD" },
            { label: "Time", value: eventItem.time || "TBD" },
            { label: "Venue", value: eventItem.venue || "Campus" },
            { label: "Category", value: eventItem.category || "General" },
            { label: "Eligibility", value: "All Enrolled Students (FYAIML / B.Tech)" },
            { label: "Organized By", value: "CSPIT StudentHub & Campus Clubs" }
        ];

        metaItems.forEach((m) => {
            const item = document.createElement("div");
            item.className = "modal-meta-item";
            const strong = document.createElement("strong");
            strong.textContent = m.label;
            const span = document.createElement("span");
            span.textContent = m.value;
            item.appendChild(strong);
            item.appendChild(span);
            metaGrid.appendChild(item);
        });
        body.appendChild(metaGrid);

        // Description
        const descHeading = document.createElement("h4");
        descHeading.className = "event-modal-desc-heading";
        descHeading.textContent = "About This Event";
        body.appendChild(descHeading);

        const descP = document.createElement("p");
        descP.textContent = eventItem.description || "Join us for an exciting campus experience.";
        body.appendChild(descP);

        dialog.appendChild(body);

        // Footer
        const footer = document.createElement("div");
        footer.className = "event-modal-footer";

        const dismissBtn = document.createElement("button");
        dismissBtn.type = "button";
        dismissBtn.className = "btn-modal-secondary";
        dismissBtn.textContent = "Close";
        dismissBtn.addEventListener("click", () => backdrop.remove());

        const registerBtn = document.createElement("button");
        registerBtn.type = "button";
        registerBtn.className = "btn-modal-register";
        registerBtn.textContent = "Register for Event";

        // Evaluate event status and registration eligibility
        const rawStatus = (eventItem.status || "").toLowerCase();
        const todayStr = "2026-10-31"; // University current academic calendar date
        const eventDateStr = eventItem.date || "";
        const isDatePast = eventDateStr && eventDateStr < todayStr;
        const isCompleted = (rawStatus === "completed") || isDatePast;
        const isCancelled = (rawStatus === "cancelled");
        const isClosed = (rawStatus === "closed");

        if (isCompleted) {
            registerBtn.disabled = true;
            registerBtn.className = "btn-modal-secondary";
            registerBtn.style.cursor = "not-allowed";
            registerBtn.style.opacity = "0.7";
            registerBtn.textContent = "Event Concluded";
            alertBox.className = "event-modal-alert info";
            alertBox.textContent = "This event took place on " + (eventItem.date || "a past date") + " and has concluded. Registrations are closed.";
        } else if (isCancelled) {
            registerBtn.disabled = true;
            registerBtn.className = "btn-modal-secondary";
            registerBtn.style.cursor = "not-allowed";
            registerBtn.style.opacity = "0.7";
            registerBtn.textContent = "Event Cancelled";
            alertBox.className = "event-modal-alert error";
            alertBox.textContent = "This event has been cancelled. Registrations are not accepted.";
        } else if (isClosed) {
            registerBtn.disabled = true;
            registerBtn.className = "btn-modal-secondary";
            registerBtn.style.cursor = "not-allowed";
            registerBtn.style.opacity = "0.7";
            registerBtn.textContent = "Registration Closed";
            alertBox.className = "event-modal-alert info";
            alertBox.textContent = "Registrations are currently closed for this event.";
        } else {
            // Check logged-in user registration status for this event
            fetch("../api/events/register.php?event_id=" + eventItem.id)
                .then((r) => r.json())
                .then((statusData) => {
                    if (statusData && statusData.is_registered) {
                        registerBtn.disabled = true;
                        registerBtn.className = "btn-modal-register";
                        registerBtn.style.background = "#059669";
                        registerBtn.textContent = "Already Registered ✓";
                        alertBox.className = "event-modal-alert success";
                        alertBox.textContent = "You are already registered for this event. View it in your Student Portal.";
                    }
                })
                .catch(() => {});
        }

        registerBtn.addEventListener("click", function () {
            if (isCompleted || isCancelled || isClosed) {
                return;
            }

            registerBtn.disabled = true;
            registerBtn.textContent = "Processing...";

            // 1. Verify user identity
            fetch("../api/auth/me.php")
                .then((res) => res.json())
                .then((authData) => {
                    if (!authData || !authData.authenticated) {
                        alertBox.className = "event-modal-alert info";
                        alertBox.textContent = "Sign in required to register for campus events. Redirecting to login...";
                        setTimeout(() => {
                            window.location.href = "login.html?error=unauthorized&redirect=events.html";
                        }, 1200);
                        return;
                    }

                    // 2. Submit registration to backend
                    fetch("../api/events/register.php", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ event_id: eventItem.id })
                    })
                        .then((res) => res.json().then(data => ({ status: res.status, body: data })))
                        .then(({ status, body }) => {
                            if (body.success) {
                                alertBox.className = "event-modal-alert success";
                                alertBox.textContent = body.message || "Registration Successful! This event has been added to your Student Portal.";
                                registerBtn.textContent = "Already Registered ✓";
                                registerBtn.style.background = "#059669";
                                registerBtn.disabled = true;
                            } else {
                                alertBox.className = "event-modal-alert error";
                                alertBox.textContent = body.message || body.error || "Registration could not be completed.";
                                if (body.already_registered) {
                                    registerBtn.textContent = "Already Registered ✓";
                                    registerBtn.style.background = "#059669";
                                    registerBtn.disabled = true;
                                } else if (body.event_status === "completed" || body.event_status === "closed") {
                                    registerBtn.textContent = "Registration Closed";
                                    registerBtn.className = "btn-modal-secondary";
                                    registerBtn.disabled = true;
                                } else {
                                    registerBtn.disabled = false;
                                    registerBtn.textContent = "Register for Event";
                                }
                            }
                        })
                        .catch((err) => {
                            alertBox.className = "event-modal-alert error";
                            alertBox.textContent = "Network error while registering. Please try again.";
                            registerBtn.disabled = false;
                            registerBtn.textContent = "Register for Event";
                        });
                })
                .catch(() => {
                    alertBox.className = "event-modal-alert error";
                    alertBox.textContent = "Unable to verify authentication. Please check your connection.";
                    registerBtn.disabled = false;
                    registerBtn.textContent = "Register for Event";
                });
        });

        footer.appendChild(dismissBtn);
        footer.appendChild(registerBtn);
        dialog.appendChild(footer);

        backdrop.appendChild(dialog);

        // Backdrop click to dismiss
        backdrop.addEventListener("click", (e) => {
            if (e.target === backdrop) backdrop.remove();
        });

        // ESC key to dismiss
        const keyHandler = (e) => {
            if (e.key === "Escape") {
                backdrop.remove();
                document.removeEventListener("keydown", keyHandler);
            }
        };
        document.addEventListener("keydown", keyHandler);

        document.body.appendChild(backdrop);
    }

    // Initial Load
    loadData();
});
