// Dark Mode Toggle
document.addEventListener('DOMContentLoaded', () => {
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    const themeIcon = document.getElementById('themeIcon');
    const currentTheme = localStorage.getItem('theme') || 'light';
  
    // Initialize Theme
    if (currentTheme === 'dark') {
      document.body.setAttribute('data-theme', 'dark');
      themeIcon.classList.replace('fa-moon', 'fa-sun');
    }
  
    // Toggle Theme
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
        let theme = document.body.getAttribute('data-theme');
        if (theme === 'dark') {
            document.body.removeAttribute('data-theme');
            localStorage.setItem('theme', 'light');
            themeIcon.classList.replace('fa-sun', 'fa-moon');
        } else {
            document.body.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
            themeIcon.classList.replace('fa-moon', 'fa-sun');
        }
        });
    }

    // Initialize AOS
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            once: true,
            offset: 50
        });
    }

    // Loader Logic for Forms
    const uploadForm = document.getElementById('uploadForm');
    const loaderOverlay = document.getElementById('loader-overlay');

    if (uploadForm) {
        uploadForm.addEventListener('submit', (e) => {
            if (loaderOverlay) {
                loaderOverlay.style.display = 'flex';
            }
        });
    }

    // Drag and Drop Logic
    const uploadZone = document.getElementById('uploadZone');
    const fileInput = document.getElementById('actual-btn');
    const fileChosen = document.getElementById('file-chosen');
    const imagePreview = document.getElementById('imagePreview');

    if (uploadZone && fileInput) {
        // Handle click on the zone
        uploadZone.addEventListener('click', () => {
            fileInput.click();
        });

        // Handle drag events
        uploadZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadZone.classList.add('dragover');
        });

        uploadZone.addEventListener('dragleave', () => {
            uploadZone.classList.remove('dragover');
        });

        uploadZone.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadZone.classList.remove('dragover');
            
            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                updatePreview(fileInput.files[0]);
            }
        });

        // Handle file input change
        fileInput.addEventListener('change', () => {
            if (fileInput.files.length) {
                updatePreview(fileInput.files[0]);
            }
        });
    }

    function updatePreview(file) {
        if (file) {
            if (fileChosen) fileChosen.textContent = file.name;
            
            // Show preview if it's an image
            if (file.type.startsWith('image/') && imagePreview) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    imagePreview.src = e.target.result;
                    imagePreview.style.display = 'block';
                };
                reader.readAsDataURL(file);
            }
        }
    }
});
