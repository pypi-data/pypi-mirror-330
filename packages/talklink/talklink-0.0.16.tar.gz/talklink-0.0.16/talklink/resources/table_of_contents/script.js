// Check for saved dark mode preference
document.addEventListener('DOMContentLoaded', function() {
    // Check if user has a saved preference
    const darkModeSaved = localStorage.getItem('darkMode');
    
    // If dark mode was previously enabled, apply it
    if (darkModeSaved === 'enabled') {
        document.body.classList.add('dark-mode');
        document.getElementById('dark-mode-button').textContent = '🌞';
    }
    
    // Add subtle animation to channel items
    const channelItems = document.querySelectorAll('.channel-item');
    channelItems.forEach((item, index) => {
        item.style.animationDelay = `${index * 0.05}s`;
        item.classList.add('fade-in');
    });
});

// Toggle dark mode and save preference
function toggleDarkMode() {
    const darkModeButton = document.getElementById('dark-mode-button');
    
    // Toggle dark mode class
    document.body.classList.toggle('dark-mode');
    
    // Update button icon
    if (document.body.classList.contains('dark-mode')) {
        darkModeButton.textContent = '🌞';
        localStorage.setItem('darkMode', 'enabled');
    } else {
        darkModeButton.textContent = '🌙';
        localStorage.setItem('darkMode', 'disabled');
    }
    
    // Add transition effect
    document.body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
}

// Add smooth scrolling for anchor links
document.addEventListener('click', function(e) {
    const target = e.target;
    
    // Check if clicked element is a link with a hash
    if (target.tagName === 'A' && target.hash) {
        const element = document.querySelector(target.hash);
        if (element) {
            e.preventDefault();
            window.scrollTo({
                top: element.offsetTop,
                behavior: 'smooth'
            });
        }
    }
});