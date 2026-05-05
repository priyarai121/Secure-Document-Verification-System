document.addEventListener('DOMContentLoaded', () => {
    // Auto-dismiss flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-alert');
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            msg.style.transform = 'translateX(100%)';
            msg.style.transition = 'all 0.3s ease-in';
            setTimeout(() => {
                msg.remove();
            }, 300);
        }, 5000);
    });

    // Client-side password confirmation validation
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        const password = document.getElementById('password');
        const confirmPassword = document.getElementById('confirm_password');
        const errorText = document.getElementById('passwordError');

        const validatePasswords = () => {
            if (confirmPassword.value && password.value !== confirmPassword.value) {
                errorText.style.display = 'block';
                confirmPassword.style.borderColor = 'var(--error-red)';
                return false;
            } else {
                errorText.style.display = 'none';
                confirmPassword.style.borderColor = 'var(--glass-border)';
                return true;
            }
        };

        password.addEventListener('input', validatePasswords);
        confirmPassword.addEventListener('input', validatePasswords);

        registerForm.addEventListener('submit', (e) => {
            if (!validatePasswords()) {
                e.preventDefault(); // Prevent submission if passwords don't match
                // Add a visual shake effect to the card
                const card = document.querySelector('.auth-card');
                card.style.transform = 'translateX(-10px)';
                setTimeout(() => card.style.transform = 'translateX(10px)', 100);
                setTimeout(() => card.style.transform = 'translateX(-10px)', 200);
                setTimeout(() => card.style.transform = 'translateX(0)', 300);
            }
        });
    }

    // Interactive Cybersecurity Background (Digital Rain)
    const canvas = document.getElementById('cyberBackground');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        
        let width = canvas.width = window.innerWidth;
        let height = canvas.height = window.innerHeight;
        
        // Characters to use for the rain
        const characters = '01ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()_+';
        const fontSize = 14;
        let columns = width / fontSize;
        
        const drops = [];
        for (let x = 0; x < columns; x++) {
            drops[x] = 1;
        }
        
        const draw = () => {
            // Translucent background to create fading effect
            ctx.fillStyle = 'rgba(10, 10, 15, 0.05)';
            ctx.fillRect(0, 0, width, height);
            
            ctx.fillStyle = '#00ff88'; // Neon green text
            ctx.font = fontSize + 'px monospace';
            
            for (let i = 0; i < drops.length; i++) {
                const text = characters.charAt(Math.floor(Math.random() * characters.length));
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                
                // Reset drop to top randomly, or increment
                if (drops[i] * fontSize > height && Math.random() > 0.975) {
                    drops[i] = 0;
                }
                drops[i]++;
            }
        };
        
        // Run animation
        setInterval(draw, 50);
        
        // Resize canvas correctly when window resizes
        window.addEventListener('resize', () => {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
            columns = width / fontSize;
            drops.length = 0;
            for (let x = 0; x < columns; x++) {
                drops[x] = 1;
            }
        });
    }

    // File Upload Logic
    const uploadZone = document.getElementById('upload-zone');
    const fileInput = document.getElementById('file-input');
    
    if (uploadZone && fileInput) {
        const progressContainer = document.getElementById('upload-progress-container');
        const progressFill = document.getElementById('progress-fill');
        const progressPercentage = document.getElementById('progress-percentage');
        const progressFilename = document.getElementById('progress-filename');
        const statusMessage = document.getElementById('upload-status-message');

        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadZone.addEventListener(eventName, preventDefaults, false);
            document.body.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        // Highlight upload zone on drag
        ['dragenter', 'dragover'].forEach(eventName => {
            uploadZone.addEventListener(eventName, () => {
                uploadZone.classList.add('dragover');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            uploadZone.addEventListener(eventName, () => {
                uploadZone.classList.remove('dragover');
            }, false);
        });

        // Handle dropped files
        uploadZone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            handleFiles(files);
        });

        // Handle file input change
        fileInput.addEventListener('change', function() {
            handleFiles(this.files);
        });

        function handleFiles(files) {
            if (files.length === 0) return;
            const file = files[0]; // Only handle single file for now
            uploadFile(file);
        }

        function uploadFile(file) {
            // Reset UI
            progressContainer.style.display = 'block';
            progressFill.style.width = '0%';
            progressPercentage.textContent = '0%';
            progressFilename.textContent = file.name;
            statusMessage.textContent = '';
            statusMessage.className = 'status-message';
            
            // Validate file size (16MB max)
            if (file.size > 16 * 1024 * 1024) {
                statusMessage.textContent = 'File too large. Max size is 16MB.';
                statusMessage.classList.add('error');
                return;
            }

            const formData = new FormData();
            formData.append('file', file);

            const xhr = new XMLHttpRequest();
            xhr.open('POST', '/upload', true);

            // Setup progress event
            xhr.upload.addEventListener('progress', (e) => {
                if (e.lengthComputable) {
                    const percentComplete = Math.round((e.loaded / e.total) * 100);
                    progressFill.style.width = percentComplete + '%';
                    progressPercentage.textContent = percentComplete + '%';
                }
            });

            // Handle response
            xhr.onload = function() {
                if (xhr.status === 200) {
                    const response = JSON.parse(xhr.responseText);
                    statusMessage.textContent = 'Upload complete! Verifying...';
                    statusMessage.classList.add('success');
                    progressFill.style.backgroundColor = 'var(--neon-green)';
                    
                    // Redirect after a short delay
                    setTimeout(() => {
                        window.location.href = response.redirect;
                    }, 1000);
                } else {
                    let errorMsg = 'Upload failed.';
                    try {
                        const response = JSON.parse(xhr.responseText);
                        if (response.error) errorMsg = response.error;
                    } catch (e) {}
                    
                    statusMessage.textContent = errorMsg;
                    statusMessage.classList.add('error');
                    progressFill.style.backgroundColor = 'var(--error-red)';
                }
            };

            xhr.onerror = function() {
                statusMessage.textContent = 'Network error occurred.';
                statusMessage.classList.add('error');
                progressFill.style.backgroundColor = 'var(--error-red)';
            };

            xhr.send(formData);
        }
    }
});
