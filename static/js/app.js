document.addEventListener("DOMContentLoaded", () => {
    const root = document.documentElement;
    const toggleButton = document.querySelector("[data-theme-toggle]");
    const toggleLabel = document.querySelector("[data-theme-label]");
    const toggleIcon = document.querySelector("[data-theme-icon]");
    const storageKey = "nexora-theme";

    if (!toggleButton) {
        return;
    }

    const updateThemeButton = (theme) => {
        const isLight = theme === "light";
        if (toggleLabel) {
            toggleLabel.textContent = isLight ? "Tema escuro" : "Tema claro";
        }
        if (toggleIcon) {
            toggleIcon.textContent = isLight ? "☾" : "◐";
        }
        toggleButton.setAttribute("aria-pressed", String(isLight));
    };

    const currentTheme = root.getAttribute("data-theme") || "dark";
    updateThemeButton(currentTheme);

    toggleButton.addEventListener("click", () => {
        const nextTheme = (root.getAttribute("data-theme") || "dark") === "dark" ? "light" : "dark";
        root.setAttribute("data-theme", nextTheme);
        localStorage.setItem(storageKey, nextTheme);
        updateThemeButton(nextTheme);
    });

    const deleteModal = document.querySelector("[data-delete-modal]");
    const deleteForm = document.querySelector("[data-delete-form]");
    const deleteTitle = document.querySelector("[data-delete-title]");
    const deleteCancel = document.querySelector("[data-delete-cancel]");
    const deleteTriggers = Array.from(document.querySelectorAll("[data-delete-trigger]"));

    if (deleteModal && deleteForm && deleteTitle && deleteTriggers.length) {
        const closeDeleteModal = () => {
            deleteModal.close();
            deleteForm.setAttribute("action", "");
        };

        deleteTriggers.forEach((trigger) => {
            trigger.addEventListener("click", () => {
                deleteForm.setAttribute("action", trigger.dataset.deleteUrl || "");
                deleteTitle.textContent = `Remover ${trigger.dataset.deleteLabel || "registro"}?`;
                deleteModal.showModal();
            });
        });

        deleteCancel?.addEventListener("click", closeDeleteModal);

        deleteModal.addEventListener("click", (event) => {
            const bounds = deleteModal.getBoundingClientRect();
            const clickedOutside =
                event.clientX < bounds.left ||
                event.clientX > bounds.right ||
                event.clientY < bounds.top ||
                event.clientY > bounds.bottom;

            if (clickedOutside) {
                closeDeleteModal();
            }
        });

        deleteModal.addEventListener("close", () => {
            deleteForm.setAttribute("action", "");
        });
    }
});
