/**
 * StudentHub - Reusable Data Loader & Cache Manager
 * Course: AIUE203 - Web Development Fundamentals (Practical 6)
 * Author: Anshika Badala (25AIML002), CSPIT, CHARUSAT
 */

const DataLoader = (function () {
    const DEFAULT_TTL_MS = 10 * 60 * 1000; // 10 minutes cache validity

    /**
     * Safely read from localStorage
     */
    function getCache(key) {
        try {
            const raw = localStorage.getItem(key);
            if (!raw) return null;
            const parsed = JSON.parse(raw);
            if (!parsed || !parsed.timestamp || !Array.isArray(parsed.data)) {
                return null;
            }
            return parsed;
        } catch (e) {
            console.warn("Storage access failed for key:", key, e);
            return null;
        }
    }

    /**
     * Safely write to localStorage
     */
    function setCache(key, data) {
        try {
            const entry = {
                timestamp: Date.now(),
                data: data
            };
            localStorage.setItem(key, JSON.stringify(entry));
        } catch (e) {
            console.warn("Unable to cache dataset:", key, e);
        }
    }

    /**
     * Fetch JSON dataset with caching, validation, and error recovery
     * @param {string} url - URL path to the JSON resource
     * @param {string} cacheKey - Storage key identifier
     * @param {Object} options - { forceRefresh: boolean, ttl: number }
     * @returns {Promise<{ data: Array, fromCache: boolean, timestamp: number }>}
     */
    async function fetchDataset(url, cacheKey, options = {}) {
        const forceRefresh = options.forceRefresh === true;
        const ttl = typeof options.ttl === "number" ? options.ttl : DEFAULT_TTL_MS;

        const cached = getCache(cacheKey);

        // If cache is fresh and forceRefresh is false, serve from cache
        if (!forceRefresh && cached && (Date.now() - cached.timestamp < ttl)) {
            return {
                data: cached.data,
                fromCache: true,
                timestamp: cached.timestamp
            };
        }

        try {
            const response = await fetch(url, {
                cache: forceRefresh ? "no-store" : "default"
            });

            if (!response.ok) {
                throw new Error(`HTTP Error ${response.status}: ${response.statusText || "Resource not found"}`);
            }

            const data = await response.json();

            if (!Array.isArray(data)) {
                throw new Error("Dataset format error: Root element must be a JSON array.");
            }

            // Save fresh data to cache
            setCache(cacheKey, data);

            return {
                data: data,
                fromCache: false,
                timestamp: Date.now()
            };
        } catch (networkError) {
            console.error("Fetch API error loading:", url, networkError);

            // Stale cache fallback if network fails
            if (cached && Array.isArray(cached.data)) {
                console.info("Recovering with stale cached data for:", cacheKey);
                return {
                    data: cached.data,
                    fromCache: true,
                    isStale: true,
                    timestamp: cached.timestamp,
                    warning: networkError.message
                };
            }

            // Re-throw with user-friendly context
            throw new Error(
                networkError.message ||
                "Failed to fetch dataset. Please ensure a local web server is running or check your connection."
            );
        }
    }

    return {
        fetchDataset: fetchDataset,
        getCache: getCache,
        setCache: setCache
    };
})();
