<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>All Videos - TalkLink</title>
    {% if create_isolated_html %}
    <style>
    {% include "styles.css" %}
    </style>
    {% else %}
    <link rel="stylesheet" href="{{styles_file_path}}">
    {% endif %}
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <div class="page-container">
        <!-- Hero Section -->
        <header class="hero">
            <div class="hero-content">
                <div class="logo-container">
                    <svg class="logo" fill="currentColor" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"><path d="M344.854 687.167c26.725 56.8 66.665 111.099 118.91 161.654-109.515-16.445-200.574-83.285-250.026-175.73l131.114 14.076zM461.776 177.924c-106.691 16.718-195.535 81.185-245.233 170.432l128.342-12.64c26.395-55.654 65.729-108.624 116.89-157.793zM502.016 337.406l1.78-163.191h-0.362c-57.402 50.103-101.083 104.341-130.194 161.745l128.774 1.45zM224.829 388.081l-23.709-0.211-23.439-0.304-1.84 169.497-94.898-170.523-52.909-0.575-2.593 241.198 23.589 0.331 23.468 0.211 1.871-173.871 97.645 174.957 50.256 0.575 2.564-241.289zM450.373 433.36l0.211-21.506 0.271-21.357-177.611-1.9-2.593 241.289 183.132 1.93 0.241-21.446 0.211-21.387-132.697-1.418 0.663-62.954 117.977 1.266 0.211-20.694 0.211-20.814-117.977-1.238 0.575-51.161 127.175 1.387zM691.15 568.256l-33.06-175.501-53.664-0.635-36.349 176.255-38.43-177.009-52.397-0.603 64.553 242.012 23.922 0.241 23.981 0.304 39.907-189.616 36.711 190.401 24.071 0.331 23.889 0.241 69.742-240.566-50.949-0.544-41.929 174.687zM529.708 174.514h-0.362l-1.748 163.162 128.866 1.359c-27.932-58.038-70.404-113.18-126.754-164.521zM804.932 340.603c-53.633-89.519-145.152-151.602-251.828-164.202 68.335 52.922 106.493 106.707 131.741 162.933l120.086 1.266zM554.925 849.786c109.455-14.028 201.386-78.448 252.927-168.876l-130.547 9.845c-27.963 56.197-69.108 109.589-122.378 159.03zM648.738 690.455l-124.914-1.359-1.69 155.833c54.961-47.872 97.462-99.846 126.602-154.475zM981.396 521.109c-11.763-10.407-35.052-19.757-70.074-27.873-24.132-5.791-39.907-10.528-47.267-14.629-7.513-3.953-11.283-9.593-11.191-16.861 0.061-9.923 3.771-17.979 11.101-23.5 7.209-5.34 17.283-8.084 30.044-7.904 14.781 0.121 26.725 3.682 35.867 10.407 9.079 6.788 13.998 15.867 14.721 27.391l49.077 0.603c-1.569-24.282-10.769-43.469-27.6-57.887-16.741-14.419-38.703-21.748-65.729-22.02-28.837-0.331-51.852 6.335-68.956 19.728-17.073 13.546-25.73 32.246-25.973 55.535-0.211 20.905 6.004 36.349 18.642 46.393 12.819 9.984 38.338 19.517 76.469 28.415 20.753 4.827 34.238 9.562 40.572 13.786 6.395 4.346 9.593 10.979 9.502 20.151-0.09 9.199-4.705 16.259-13.786 21.387-9.109 5.068-21.628 7.54-37.766 7.359-15.596-0.181-27.813-3.71-36.439-10.738-8.746-6.91-13.212-16.711-13.634-29.652l-48.534-0.512c0.875 26.063 9.895 46.213 26.908 60.511 17.043 14.419 40.844 21.689 71.278 21.989 30.495 0.304 54.598-5.942 72.578-19.154 18.038-13.151 27.088-30.979 27.328-53.664 0.362-22.503-5.429-38.974-17.134-49.26zM496.586 844.508l1.69-155.651-124.914-1.359c28.053 55.201 69.348 108.05 123.223 157.009z" /></svg>
                    <h1>TalkLink</h1>
                </div>
                <p class="hero-tagline">Interactive transcripts for your favorite videos</p>
                <div class="hero-actions">
                    <a href="https://buymeacoffee.com/talklink" target="_blank" class="bmc-button">
                        <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee">
                        <span>Support TalkLink</span>
                    </a>
                    <button id="dark-mode-button" onClick="toggleDarkMode()" aria-label="Toggle dark mode">
                        <i class="fas fa-moon"></i>
                    </button>
                </div>
            </div>
        </header>
        
        <div class="container">
            <!-- Search and Filter Section -->
            <div class="search-section">
                <div class="search-container">
                    <i class="fas fa-search search-icon"></i>
                    <input type="text" id="searchInput" placeholder="Type '/' or 'f' to search, 'Esc' to clear..." 
                           onkeyup="searchVideos()" 
                           onkeydown="if(event.key==='Escape'){this.value='';this.blur();searchVideos();event.preventDefault();}">
                </div>
                <div class="filter-container">
                    <button id="filterToggle" class="filter-button">
                        <i class="fas fa-filter"></i> Filter
                    </button>
                    <div id="filterOptions" class="filter-dropdown">
                        <div class="filter-group">
                            <h3>Sort by</h3>
                            <div class="filter-options">
                                <button class="filter-option active" data-sort="newest">Newest</button>
                                <button class="filter-option" data-sort="oldest">Oldest</button>
                                <button class="filter-option" data-sort="duration">Duration</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Navigation Links -->
            <div class="navigation-links">
                <a href="{{ home_link }}" class="nav-link">
                    <i class="fas fa-home"></i> Home
                </a>
                <a href="{{ about_link }}" class="nav-link">
                    <i class="fas fa-info-circle"></i> About
                </a>
            </div>
            
            <!-- All Videos Section -->
            <section class="all-videos-section" id="all-videos">
                <div class="section-header">
                    <h2>All Videos</h2>
                </div>
                <div class="video-list">
                    <div class="video-list-header">
                        <span class="header-title">Title</span>
                        <span class="header-channel">Channel</span>
                        <span class="header-duration">Duration</span>
                        <span class="header-date">Date</span>
                    </div>
                    {% for channel, videos in index_map|dictsort %}
                        {% for video_id, video in videos.items() %}
                        <div class="video-list-item" data-channel="{{ channel }}" data-title="{{ video.title }}" data-date="{{ video.upload_date }}">
                            <a href="{{ video.talklink_file }}" class="video-list-title">{{ video.title }}</a>
                            <span class="video-list-channel">{{ channel }}</span>
                            <span class="video-list-duration">{{ video.duration }}</span>
                            <span class="video-list-date">{{ video.upload_date }}</span>
                        </div>
                        {% endfor %}
                    {% endfor %}
                </div>
            </section>
        </div>
        
        <!-- Footer -->
        <footer class="footer">
            <div class="footer-content">
                <div class="footer-logo">
                    <svg class="logo" fill="currentColor" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"><path d="M344.854 687.167c26.725 56.8 66.665 111.099 118.91 161.654-109.515-16.445-200.574-83.285-250.026-175.73l131.114 14.076zM461.776 177.924c-106.691 16.718-195.535 81.185-245.233 170.432l128.342-12.64c26.395-55.654 65.729-108.624 116.89-157.793zM502.016 337.406l1.78-163.191h-0.362c-57.402 50.103-101.083 104.341-130.194 161.745l128.774 1.45z" /></svg>
                    <span>TalkLink</span>
                </div>
                <div class="footer-links">
                    <a href="{{ home_link }}" class="footer-link">Home</a>
                    <a href="{{ about_link }}" class="footer-link">About</a>
                    <a href="#" class="footer-link">Privacy</a>
                    <a href="#" class="footer-link">Terms</a>
                    <a href="https://buymeacoffee.com/talklink" target="_blank" class="footer-link">Support</a>
                </div>
                <div class="footer-social">
                    {% for social in social_links %}
                    <a href="{{ social.url }}" class="social-link"><i class="{{ social.icon }}"></i></a>
                    {% endfor %}
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; {{ current_year }} TalkLink. All rights reserved.</p>
            </div>
        </footer>
    </div>
    
    {% if create_isolated_html %}
    <script>
    {% include "script.js" %}
    </script>
    {% else %}
    <script>
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
    </script>
    {% endif %}
</body>
</html> 