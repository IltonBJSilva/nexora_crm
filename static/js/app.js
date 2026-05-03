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
});
