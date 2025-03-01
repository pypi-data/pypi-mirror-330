// Dark mode toggle functionality
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    
    // Save preference to localStorage
    if (document.body.classList.contains('dark-mode')) {
        localStorage.setItem('darkMode', 'enabled');
        document.getElementById('dark-mode-button').innerHTML = '<i class="fas fa-sun"></i>';
    } else {
        localStorage.setItem('darkMode', 'disabled');
        document.getElementById('dark-mode-button').innerHTML = '<i class="fas fa-moon"></i>';
    }
}

// Check for saved dark mode preference
document.addEventListener('DOMContentLoaded', function() {
    if (localStorage.getItem('darkMode') === 'enabled') {
        document.body.classList.add('dark-mode');
        document.getElementById('dark-mode-button').innerHTML = '<i class="fas fa-sun"></i>';
    }
    
    // Initialize filters
    initializeFilters();
});

// Initialize filter dropdown
function initializeFilters() {
    const filterToggle = document.getElementById('filterToggle');
    const filterOptions = document.getElementById('filterOptions');
    
    if (filterToggle && filterOptions) {
        filterToggle.addEventListener('click', function() {
            filterOptions.classList.toggle('active');
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', function(event) {
            if (!filterToggle.contains(event.target) && !filterOptions.contains(event.target)) {
                filterOptions.classList.remove('active');
            }
        });
        
        // Close dropdown with Escape key
        filterOptions.addEventListener('keydown', function(event) {
            if (event.key === 'Escape') {
                filterOptions.classList.remove('active');
                event.preventDefault();
                event.stopPropagation();
            }
        });
        
        // Set up filter options
        const sortButtons = document.querySelectorAll('.filter-option[data-sort]');
        
        sortButtons.forEach(button => {
            button.addEventListener('click', function() {
                sortButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                sortVideos(this.dataset.sort);
            });
        });
    }
}

// Search functionality
function searchVideos() {
    const searchInput = document.getElementById('searchInput');
    if (!searchInput) return;
    
    const query = searchInput.value.toLowerCase();
    const videoListItems = document.querySelectorAll('.video-list-item');
    
    // Search in video list items
    videoListItems.forEach(item => {
        const title = item.dataset.title.toLowerCase();
        const channel = item.dataset.channel.toLowerCase();
        
        if (title.includes(query) || channel.includes(query)) {
            item.style.display = '';
        } else {
            item.style.display = 'none';
        }
    });
}

// Sort videos by different criteria
function sortVideos(sortBy) {
    // Sort video list
    sortElements('.video-list', '.video-list-item', sortBy);
}

function sortElements(container, selector, sortBy) {
    const containers = document.querySelectorAll(container);
    
    containers.forEach(cont => {
        const items = Array.from(cont.querySelectorAll(selector));
        
        items.sort((a, b) => {
            if (sortBy === 'newest') {
                return new Date(b.dataset.date) - new Date(a.dataset.date);
            } else if (sortBy === 'oldest') {
                return new Date(a.dataset.date) - new Date(b.dataset.date);
            } else if (sortBy === 'duration') {
                const durationA = a.querySelector('.video-duration, .video-list-duration')?.textContent || '';
                const durationB = b.querySelector('.video-duration, .video-list-duration')?.textContent || '';
                
                // Convert duration to seconds for comparison
                const secondsA = convertDurationToSeconds(durationA);
                const secondsB = convertDurationToSeconds(durationB);
                
                return secondsB - secondsA; // Longest first
            }
            return 0;
        });
        
        // Reappend sorted items
        items.forEach(item => {
            cont.appendChild(item);
        });
    });
}

// Helper function to convert duration string to seconds
function convertDurationToSeconds(duration) {
    if (!duration) return 0;
    
    const parts = duration.split(':').map(part => parseInt(part, 10));
    
    if (parts.length === 3) {
        // Hours:Minutes:Seconds
        return parts[0] * 3600 + parts[1] * 60 + parts[2];
    } else if (parts.length === 2) {
        // Minutes:Seconds
        return parts[0] * 60 + parts[1];
    } else {
        return 0;
    }
}

// Set up keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // Focus search bar with / or f key (when not already in an input)
    if ((event.key === '/' || event.key === 'f') && 
        document.activeElement.tagName !== 'INPUT' && 
        document.activeElement.tagName !== 'TEXTAREA') {
        event.preventDefault();
        const searchInput = document.getElementById('searchInput');
        if (searchInput) searchInput.focus();
    }
    
    // Toggle dark mode with d key (when not in an input)
    if (event.key === 'd' && 
        document.activeElement.tagName !== 'INPUT' && 
        document.activeElement.tagName !== 'TEXTAREA') {
        toggleDarkMode();
    }
    
    // Handle Escape key for filter dropdown
    if (event.key === 'Escape') {
        // Close filter dropdown if open
        const filterOptions = document.getElementById('filterOptions');
        if (filterOptions && filterOptions.classList.contains('active')) {
            filterOptions.classList.remove('active');
        }
    }
}); 