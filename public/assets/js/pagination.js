/**
 * StudentHub - Reusable Client-Side Pagination Module
 * Course: AIUE203 - Web Development Fundamentals (Practical 6)
 * Author: Anshika Badala (25AIML002), CSPIT, CHARUSAT
 */

const Paginator = (function () {
    /**
     * Slice an array of items for the specified page and page size
     */
    function paginate(items, currentPage, pageSize) {
        const totalItems = items.length;
        const totalPages = Math.ceil(totalItems / pageSize) || 1;
        const validPage = Math.max(1, Math.min(currentPage, totalPages));

        const startIndex = (validPage - 1) * pageSize;
        const endIndex = Math.min(startIndex + pageSize, totalItems);
        const pagedItems = items.slice(startIndex, endIndex);

        return {
            items: pagedItems,
            totalItems: totalItems,
            totalPages: totalPages,
            currentPage: validPage,
            startIndex: startIndex,
            endIndex: endIndex
        };
    }

    /**
     * Render accessible DOM pagination controls
     * Uses textContent and createElement exclusively for safe DOM manipulation
     * @param {Object} paginationState - Output from paginate()
     * @param {Function} onPageChange - Callback when a page button is clicked
     * @returns {HTMLElement} - <nav class="pagination-container">
     */
    function renderPaginationControls(paginationState, onPageChange) {
        const { currentPage, totalPages, totalItems, startIndex, endIndex } = paginationState;

        const nav = document.createElement("nav");
        nav.className = "pagination-container";
        nav.setAttribute("aria-label", "Pagination Navigation");

        // Previous Button
        const prevBtn = document.createElement("button");
        prevBtn.type = "button";
        prevBtn.className = "pagination-btn";
        prevBtn.textContent = "« Previous";
        prevBtn.disabled = currentPage <= 1;
        prevBtn.setAttribute("aria-label", "Go to previous page");
        prevBtn.addEventListener("click", () => {
            if (currentPage > 1) {
                onPageChange(currentPage - 1);
            }
        });
        nav.appendChild(prevBtn);

        // Page Numbers (Show up to 5 visible pages or ellipses)
        const maxVisibleButtons = 5;
        let startPage = Math.max(1, currentPage - Math.floor(maxVisibleButtons / 2));
        let endPage = Math.min(totalPages, startPage + maxVisibleButtons - 1);

        if (endPage - startPage + 1 < maxVisibleButtons) {
            startPage = Math.max(1, endPage - maxVisibleButtons + 1);
        }

        for (let p = startPage; p <= endPage; p++) {
            const pageBtn = document.createElement("button");
            pageBtn.type = "button";
            pageBtn.className = "pagination-btn" + (p === currentPage ? " active" : "");
            pageBtn.textContent = String(p);
            pageBtn.setAttribute("aria-label", `Page ${p}`);
            if (p === currentPage) {
                pageBtn.setAttribute("aria-current", "page");
            } else {
                pageBtn.addEventListener("click", () => onPageChange(p));
            }
            nav.appendChild(pageBtn);
        }

        // Next Button
        const nextBtn = document.createElement("button");
        nextBtn.type = "button";
        nextBtn.className = "pagination-btn";
        nextBtn.textContent = "Next »";
        nextBtn.disabled = currentPage >= totalPages;
        nextBtn.setAttribute("aria-label", "Go to next page");
        nextBtn.addEventListener("click", () => {
            if (currentPage < totalPages) {
                onPageChange(currentPage + 1);
            }
        });
        nav.appendChild(nextBtn);

        // Page info text
        const infoSpan = document.createElement("span");
        infoSpan.className = "pagination-info";
        if (totalItems > 0) {
            infoSpan.textContent = `(Page ${currentPage} of ${totalPages} • Showing ${startIndex + 1}–${endIndex} of ${totalItems})`;
        } else {
            infoSpan.textContent = "(0 items)";
        }
        nav.appendChild(infoSpan);

        return nav;
    }

    return {
        paginate: paginate,
        renderControls: renderPaginationControls
    };
})();
