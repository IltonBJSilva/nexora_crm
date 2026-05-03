document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.querySelector("[data-sidebar-search]");
    const groups = Array.from(document.querySelectorAll("[data-sidebar-group]"));
    const links = Array.from(document.querySelectorAll("[data-sidebar-link]"));
    const labelNodes = Array.from(document.querySelectorAll(".sidebar-link__label"));

    if (!searchInput) {
        return;
    }

    groups.forEach((group) => {
        group.dataset.defaultOpen = group.hasAttribute("open") ? "true" : "false";
    });

    const normalize = (value) =>
        value
            .toLowerCase()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "");

    const escapeHtml = (value) =>
        value
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;");

    labelNodes.forEach((node) => {
        node.dataset.originalLabel = node.textContent || "";
    });

    const highlightLabel = (node, query) => {
        const original = node.dataset.originalLabel || node.textContent || "";
        if (!query) {
            node.innerHTML = escapeHtml(original);
            return;
        }

        const escapedQuery = query.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
        const regex = new RegExp(`(${escapedQuery})`, "ig");
        node.innerHTML = escapeHtml(original).replace(regex, "<mark>$1</mark>");
    };

    const applyFilter = () => {
        const rawQuery = searchInput.value.trim();
        const query = normalize(rawQuery);

        links.forEach((link) => {
            if (link.closest(".nav")) {
                const label = normalize(link.dataset.sidebarLabel || link.textContent || "");
                link.parentElement?.style?.removeProperty("display");
                link.style.display = !query || label.includes(query) ? "" : "none";
            }
        });

        groups.forEach((group) => {
            const groupLabel = normalize(group.dataset.groupLabel || "");
            const items = Array.from(group.querySelectorAll("[data-sidebar-item]"));
            let visibleItems = 0;

            items.forEach((item) => {
                const link = item.querySelector("[data-sidebar-link]");
                const labelNode = item.querySelector(".sidebar-link__label");
                const label = normalize(link?.dataset.sidebarLabel || link?.textContent || "");
                const matches = !query || label.includes(query) || groupLabel.includes(query);
                item.style.display = matches ? "" : "none";
                if (labelNode) {
                    highlightLabel(labelNode, rawQuery);
                }
                if (matches) {
                    visibleItems += 1;
                }
            });

            const shouldShowGroup = visibleItems > 0 || (!query && items.length > 0);
            group.style.display = shouldShowGroup ? "" : "none";

            if (!query) {
                if (group.dataset.defaultOpen === "true") {
                    group.setAttribute("open", "");
                } else {
                    group.removeAttribute("open");
                }
            } else if (visibleItems > 0) {
                group.setAttribute("open", "");
            }
        });
    };

    searchInput.addEventListener("input", applyFilter);

    document.addEventListener("keydown", (event) => {
        const isShortcut = (event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k";
        if (!isShortcut) {
            return;
        }

        event.preventDefault();
        searchInput.focus();
        searchInput.select();
    });
});
