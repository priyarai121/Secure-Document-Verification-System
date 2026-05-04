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
});
