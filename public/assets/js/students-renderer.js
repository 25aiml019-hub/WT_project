/**
 * StudentHub - Student Directory Dynamic Renderer
 * Course: AIUE203 - Web Development Fundamentals (Practical 6)
 * Author: Daksh Harkhani (25AIML019), CSPIT, CHARUSAT
 */

document.addEventListener("DOMContentLoaded", function () {
    const container = document.getElementById("students-app");
    if (!container) return;

    const DATA_URL = (function () {
        if (typeof window !== "undefined" && window.location) {
            const loc = window.location.pathname;
            if (loc.includes("/pages/")) {
                return "../assets/data/students.json";
            }
            if (loc.includes("/public/")) {
                return "assets/data/students.json";
            }
        }
        return "../assets/data/students.json";
    })();
    const CACHE_KEY = "studenthub_students_cache";
    const PAGE_SIZE = 10;

    // State
    let rawStudents = [];
    let filteredStudents = [];
    let currentPage = 1;
    let searchQuery = "";
    let selectedCourse = "all";
    let selectedYear = "all";
    let selectedSort = "name-asc";
    let isDataCached = false;
    let cacheTimestamp = null;

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
    controlBar.setAttribute("aria-label", "Search and filter student directory");

    // Search Input
    const searchGroup = document.createElement("div");
    searchGroup.className = "control-group";
    const searchLabel = document.createElement("label");
    searchLabel.htmlFor = "students-search";
    searchLabel.textContent = "Search Student Directory:";
    const searchInput = document.createElement("input");
    searchInput.type = "text";
    searchInput.id = "students-search";
    searchInput.placeholder = "Search by name, course, or department...";
    searchGroup.appendChild(searchLabel);
    searchGroup.appendChild(searchInput);
    controlBar.appendChild(searchGroup);

    // Course Filter
    const courseGroup = document.createElement("div");
    courseGroup.className = "control-group";
    const courseLabel = document.createElement("label");
    courseLabel.htmlFor = "students-course";
    courseLabel.textContent = "Course:";
    const courseSelect = document.createElement("select");
    courseSelect.id = "students-course";
    const courses = ["all", "B.Tech", "BCA", "M.Tech", "MCA"];
    courses.forEach((c) => {
        const opt = document.createElement("option");
        opt.value = c;
        opt.textContent = c === "all" ? "All Courses" : c;
        courseSelect.appendChild(opt);
    });
    courseGroup.appendChild(courseLabel);
    courseGroup.appendChild(courseSelect);
    controlBar.appendChild(courseGroup);

    // Year Filter
    const yearGroup = document.createElement("div");
    yearGroup.className = "control-group";
    const yearLabel = document.createElement("label");
    yearLabel.htmlFor = "students-year";
    yearLabel.textContent = "Academic Year:";
    const yearSelect = document.createElement("select");
    yearSelect.id = "students-year";
    const years = ["all", "1st Year", "2nd Year", "3rd Year", "4th Year"];
    years.forEach((y) => {
        const opt = document.createElement("option");
        opt.value = y;
        opt.textContent = y === "all" ? "All Years" : y;
        yearSelect.appendChild(opt);
    });
    yearGroup.appendChild(yearLabel);
    yearGroup.appendChild(yearSelect);
    controlBar.appendChild(yearGroup);

    // Sort Dropdown
    const sortGroup = document.createElement("div");
    sortGroup.className = "control-group";
    const sortLabel = document.createElement("label");
    sortLabel.htmlFor = "students-sort";
    sortLabel.textContent = "Sort By Name:";
    const sortSelect = document.createElement("select");
    sortSelect.id = "students-sort";
    const sortOptions = [
        { value: "name-asc", label: "Name (A to Z)" },
        { value: "name-desc", label: "Name (Z to A)" }
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

    // 2. Status Bar
    const statusBar = document.createElement("div");
    statusBar.className = "status-bar";

    const countSpan = document.createElement("span");
    countSpan.className = "result-count";
    countSpan.textContent = "Loading students...";
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
     * Load Students Dataset
     */
    async function loadData(forceRefresh = false) {
        showLoading();
        try {
            const result = await DataLoader.fetchDataset(DATA_URL, CACHE_KEY, { forceRefresh });
            rawStudents = result.data;
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
        countSpan.textContent = "Fetching student directory...";

        const loadingDiv = document.createElement("div");
        loadingDiv.className = "loading-state";
        loadingDiv.setAttribute("role", "status");

        const spinner = document.createElement("div");
        spinner.className = "spinner";
        loadingDiv.appendChild(spinner);

        const text = document.createElement("p");
        text.textContent = "Loading student directory via Fetch API...";
        loadingDiv.appendChild(text);

        contentArea.appendChild(loadingDiv);
    }

    function showError(message) {
        contentArea.textContent = "";
        paginationWrapper.textContent = "";
        countSpan.textContent = "Failed to load student directory.";

        badgeSpan.className = "data-badge error";
        badgeSpan.textContent = "Fetch Failed";

        const errDiv = document.createElement("div");
        errDiv.className = "error-state";
        errDiv.setAttribute("role", "alert");

        const h3 = document.createElement("h3");
        h3.textContent = "Unable to load student directory";
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
     * Filter & Sort
     */
    function applyFiltersAndRender(resetPage = false) {
        if (resetPage) {
            currentPage = 1;
        }

        const query = searchQuery.toLowerCase().trim();

        filteredStudents = rawStudents.filter((student) => {
            const matchName = (student.name || "").toLowerCase().includes(query);
            const matchCourse = (student.course || "").toLowerCase().includes(query);
            const matchDept = (student.department || "").toLowerCase().includes(query);
            const matchRoll = (student.roll_number || "").toLowerCase().includes(query);
            const matchBatch = (student.batch || "").toLowerCase().includes(query);
            const matchCounselor = (student.counselor || "").toLowerCase().includes(query);
            const matchSearch = query === "" || matchName || matchCourse || matchDept || matchRoll || matchBatch || matchCounselor;

            const matchCourseFilter = selectedCourse === "all" ||
                (student.course || "").toLowerCase() === selectedCourse.toLowerCase();

            const matchYearFilter = selectedYear === "all" ||
                (student.year || "").toLowerCase() === selectedYear.toLowerCase();

            return matchSearch && matchCourseFilter && matchYearFilter;
        });

        // Sorting
        filteredStudents.sort((a, b) => {
            const nameA = a.name || "";
            const nameB = b.name || "";
            if (selectedSort === "name-asc") {
                return nameA.localeCompare(nameB);
            } else {
                return nameB.localeCompare(nameA);
            }
        });

        renderView();
    }

    function renderView() {
        contentArea.textContent = "";
        paginationWrapper.textContent = "";

        const total = filteredStudents.length;
        countSpan.textContent = `Showing ${total} student${total === 1 ? "" : "s"} (filtered from ${rawStudents.length} total)`;
        liveAnnouncer.textContent = `Student directory updated. ${total} records available.`;

        if (total === 0) {
            const emptyDiv = document.createElement("div");
            emptyDiv.className = "empty-state";

            const h3 = document.createElement("h3");
            h3.textContent = "No matching students found";
            emptyDiv.appendChild(h3);

            const p = document.createElement("p");
            p.textContent = "Try searching with a different name, course, or department filter.";
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

        const paginated = Paginator.paginate(filteredStudents, currentPage, PAGE_SIZE);
        currentPage = paginated.currentPage;

        // Render Semantic Data Table
        const table = document.createElement("table");
        table.className = "data-table";
        table.setAttribute("aria-label", "Student Directory Records");

        const thead = document.createElement("thead");
        const headerRow = document.createElement("tr");
        ["Roll No", "Student Name", "Course", "Year", "Department"].forEach((heading) => {
            const th = document.createElement("th");
            th.textContent = heading;
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);
        table.appendChild(thead);

        const tbody = document.createElement("tbody");
        paginated.items.forEach((student) => {
            const tr = document.createElement("tr");

            // Roll Number
            const tdRoll = document.createElement("td");
            tdRoll.style.fontFamily = "monospace";
            tdRoll.textContent = student.roll_number || String(student.id);
            tr.appendChild(tdRoll);

            // Name
            const tdName = document.createElement("td");
            tdName.style.textAlign = "left";
            const nameBold = document.createElement("strong");
            nameBold.textContent = student.name;
            tdName.appendChild(nameBold);
            if (student.batch) {
                const batchBadge = document.createElement("span");
                batchBadge.style.display = "inline-block";
                batchBadge.style.marginLeft = "8px";
                batchBadge.style.padding = "2px 6px";
                batchBadge.style.fontSize = "11px";
                batchBadge.style.background = "#EFF6FF";
                batchBadge.style.color = "#2563EB";
                batchBadge.style.borderRadius = "4px";
                batchBadge.style.fontWeight = "600";
                batchBadge.textContent = student.batch;
                tdName.appendChild(batchBadge);
            }
            tr.appendChild(tdName);

            // Course
            const tdCourse = document.createElement("td");
            tdCourse.textContent = student.course || "";
            tr.appendChild(tdCourse);

            // Year
            const tdYear = document.createElement("td");
            tdYear.textContent = student.year || "";
            tr.appendChild(tdYear);

            // Department
            const tdDept = document.createElement("td");
            tdDept.style.textAlign = "left";
            tdDept.textContent = student.department || "";
            tr.appendChild(tdDept);

            tbody.appendChild(tr);
        });
        table.appendChild(tbody);
        contentArea.appendChild(table);

        // Pagination Controls
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
        selectedCourse = "all";
        courseSelect.value = "all";
        selectedYear = "all";
        yearSelect.value = "all";
        selectedSort = "name-asc";
        sortSelect.value = "name-asc";
        applyFiltersAndRender(true);
    }

    // Event Listeners
    searchInput.addEventListener("input", (e) => {
        searchQuery = e.target.value;
        applyFiltersAndRender(true);
    });

    courseSelect.addEventListener("change", (e) => {
        selectedCourse = e.target.value;
        applyFiltersAndRender(true);
    });

    yearSelect.addEventListener("change", (e) => {
        selectedYear = e.target.value;
        applyFiltersAndRender(true);
    });

    sortSelect.addEventListener("change", (e) => {
        selectedSort = e.target.value;
        applyFiltersAndRender(false);
    });

    resetBtn.addEventListener("click", resetAllFilters);
    refreshBtn.addEventListener("click", () => loadData(true));

    // Initial Load
    loadData();
});
