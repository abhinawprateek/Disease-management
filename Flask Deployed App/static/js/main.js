// Dark Mode Toggle + Global UI Logic
document.addEventListener('DOMContentLoaded', () => {
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    const themeIcon = document.getElementById('themeIcon');
    const currentTheme = localStorage.getItem('theme') || 'light';

    /* =========================================
       THEME INITIALIZATION
    ========================================= */
    if (currentTheme === 'dark') {
        document.body.setAttribute('data-theme', 'dark');
        if (themeIcon) {
            themeIcon.classList.replace('fa-moon', 'fa-sun');
        }
    }

    /* =========================================
       THEME TOGGLE
    ========================================= */
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            let theme = document.body.getAttribute('data-theme');

            if (theme === 'dark') {
                document.body.removeAttribute('data-theme');
                localStorage.setItem('theme', 'light');
                if (themeIcon) {
                    themeIcon.classList.replace('fa-sun', 'fa-moon');
                }
            } else {
                document.body.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
                if (themeIcon) {
                    themeIcon.classList.replace('fa-moon', 'fa-sun');
                }
            }
        });
    }

    /* =========================================
       AOS INITIALIZATION
    ========================================= */
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            once: true,
            offset: 50
        });
    }

    /* =========================================
       LOADER LOGIC FOR FORMS
    ========================================= */
    const uploadForm = document.getElementById('uploadForm');
    const loaderOverlay = document.getElementById('loader-overlay');

    if (uploadForm) {
        uploadForm.addEventListener('submit', () => {
            if (loaderOverlay) {
                loaderOverlay.style.display = 'flex';
            }
        });
    }

    /* =========================================
       DRAG & DROP / FILE PREVIEW
    ========================================= */
    const uploadZone = document.getElementById('uploadZone');
    const fileInput = document.getElementById('actual-btn');
    const fileChosen = document.getElementById('file-chosen');
    const imagePreview = document.getElementById('imagePreview');

    if (uploadZone && fileInput) {
        // Click to browse
        uploadZone.addEventListener('click', () => {
            fileInput.click();
        });

        // Drag over
        uploadZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadZone.classList.add('dragover');
        });

        // Drag leave
        uploadZone.addEventListener('dragleave', () => {
            uploadZone.classList.remove('dragover');
        });

        // Drop file
        uploadZone.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadZone.classList.remove('dragover');

            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                updatePreview(fileInput.files[0]);
            }
        });

        // File input change
        fileInput.addEventListener('change', () => {
            if (fileInput.files.length) {
                updatePreview(fileInput.files[0]);
            }
        });
    }

    function updatePreview(file) {
        if (!file) return;

        if (fileChosen) {
            fileChosen.textContent = file.name;
        }

        // Show image preview
        if (file.type.startsWith('image/') && imagePreview) {
            const reader = new FileReader();
            reader.onload = (e) => {
                imagePreview.src = e.target.result;
                imagePreview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    }

    /* =========================================
       HERO VIDEO (HOME PAGE)
       Speed: 0.5x
    ========================================= */
    const heroVideo = document.querySelector('.hero-bg-video');

    if (heroVideo) {
        const setHeroVideoSpeed = () => {
            heroVideo.playbackRate = 0.50;
        };

        setHeroVideoSpeed();

        heroVideo.addEventListener('loadeddata', setHeroVideoSpeed);
        heroVideo.addEventListener('canplay', setHeroVideoSpeed);

        heroVideo.play().catch(() => {});
    }

    /* =========================================
       AI ENGINE VIDEO
       Speed: 0.3x
    ========================================= */
    const aiEngineVideo = document.querySelector('.ai-engine-bg-video');

    if (aiEngineVideo) {
        const setAiVideoSpeed = () => {
            aiEngineVideo.playbackRate = 0.40;
        };

        setAiVideoSpeed();

        aiEngineVideo.addEventListener('loadeddata', setAiVideoSpeed);
        aiEngineVideo.addEventListener('canplay', setAiVideoSpeed);

        aiEngineVideo.play().catch(() => {});
    }
    /* ---------------- CONTACT PAGE VIDEO ---------------- */
const contactVideo = document.querySelector(".contact-bg-video");

if (contactVideo) {
    contactVideo.playbackRate = 0.50;

    contactVideo.addEventListener("loadeddata", () => {
        contactVideo.playbackRate = 0.50;
    });

    contactVideo.play().catch(() => {});
}
});