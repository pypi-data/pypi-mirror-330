// Check for saved dark mode preference
document.addEventListener('DOMContentLoaded', function() {
    // Apply dark mode if saved
    const darkMode = localStorage.getItem('darkMode');
    if (darkMode === 'enabled') {
        document.body.classList.add('dark-mode');
        
        // Update dark mode button icon
        const darkModeButton = document.getElementById('dark-mode-button');
        if (darkModeButton) {
            const icon = darkModeButton.querySelector('i');
            if (icon) {
                icon.className = 'fas fa-sun';
            }
        }
    }

    // Add animations to elements
    animateElements();

    // Initialize filter dropdown
    initializeFilters();
    
    // Add keyboard event listeners
    setupKeyboardShortcuts();
});

// Set up keyboard shortcuts
function setupKeyboardShortcuts() {
    // Add event listener for the search input to handle Escape key
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keydown', function(event) {
            if (event.key === 'Escape') {
                this.value = '';
                this.blur();
                searchVideos();
                event.preventDefault();
                event.stopPropagation();
            }
        });
    }
    
    // Add global keyboard shortcuts
    document.addEventListener('keydown', function(event) {
        // Focus search bar with / or f key (when not already in an input)
        if ((event.key === '/' || event.key === 'f') && 
            document.activeElement.tagName !== 'INPUT' && 
            document.activeElement.tagName !== 'TEXTAREA') {
            event.preventDefault();
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
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Add subtle animations to elements
function animateElements() {
    const elements = document.querySelectorAll('.video-card, .channel-card, .video-list-item');
    elements.forEach((element, index) => {
        element.classList.add('fade-in');
        element.style.animationDelay = `${index * 0.05}s`;
    });
}

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
        const viewButtons = document.querySelectorAll('.filter-option[data-view]');
        
        sortButtons.forEach(button => {
            button.addEventListener('click', function() {
                sortButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                sortVideos(this.dataset.sort);
            });
        });
        
        viewButtons.forEach(button => {
            button.addEventListener('click', function() {
                viewButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                filterView(this.dataset.view);
            });
        });
    }
}

// Search functionality
function searchVideos() {
    const searchInput = document.getElementById('searchInput');
    if (!searchInput) return;
    
    const query = searchInput.value.toLowerCase();
    const videoCards = document.querySelectorAll('.video-card');
    const channelVideoItems = document.querySelectorAll('.channel-video-item');
    const channelCards = document.querySelectorAll('.channel-card');
    
    // Search in video cards (Today and Yesterday sections)
    videoCards.forEach(card => {
        const title = card.dataset.title.toLowerCase();
        const channel = card.dataset.channel.toLowerCase();
        
        if (title.includes(query) || channel.includes(query)) {
            card.style.display = '';
        } else {
            card.style.display = 'none';
        }
    });
    
    // Search in channel video items
    channelVideoItems.forEach(item => {
        const title = item.dataset.title.toLowerCase();
        
        if (title.includes(query)) {
            item.style.display = '';
        } else {
            item.style.display = 'none';
        }
    });
    
    // Hide empty channel cards
    channelCards.forEach(card => {
        const visibleItems = card.querySelectorAll('.channel-video-item[style="display: none;"]');
        if (visibleItems.length === 0 && query !== '') {
            card.style.display = 'none';
        } else {
            card.style.display = '';
        }
    });
    
    // Show/hide empty sections
    updateSectionVisibility();
}

// Sort videos by different criteria
function sortVideos(sortBy) {
    // Sort video cards
    sortElements('.video-grid', '.video-card', sortBy);
    
    // Sort channel videos
    document.querySelectorAll('.channel-videos').forEach(channelVideos => {
        sortElements(channelVideos, '.channel-video-item', sortBy);
    });
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

// Convert duration string (HH:MM:SS or MM:SS) to seconds
function convertDurationToSeconds(duration) {
    if (!duration) return 0;
    
    const parts = duration.split(':').map(Number);
    
    if (parts.length === 3) {
        // HH:MM:SS
        return parts[0] * 3600 + parts[1] * 60 + parts[2];
    } else if (parts.length === 2) {
        // MM:SS
        return parts[0] * 60 + parts[1];
    }
    
    return 0;
}

// Filter view (all, channels, recent)
function filterView(view) {
    const todaySection = document.getElementById('today');
    const yesterdaySection = document.getElementById('yesterday');
    const channelsSection = document.getElementById('channels');
    
    if (view === 'all') {
        if (todaySection) todaySection.style.display = '';
        if (yesterdaySection) yesterdaySection.style.display = '';
        if (channelsSection) channelsSection.style.display = '';
    } else if (view === 'channels') {
        if (todaySection) todaySection.style.display = 'none';
        if (yesterdaySection) yesterdaySection.style.display = 'none';
        if (channelsSection) channelsSection.style.display = '';
    } else if (view === 'recent') {
        if (todaySection) todaySection.style.display = '';
        if (yesterdaySection) yesterdaySection.style.display = '';
        if (channelsSection) channelsSection.style.display = 'none';
    }
}

// Update section visibility based on search results
function updateSectionVisibility() {
    const sections = document.querySelectorAll('.recent-videos-section, .channels-section');
    
    sections.forEach(section => {
        const visibleItems = section.querySelectorAll('.video-card:not([style="display: none;"]), .channel-card:not([style="display: none;"])');
        
        if (visibleItems.length === 0) {
            section.style.display = 'none';
        } else {
            section.style.display = '';
        }
    });
}


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
});
