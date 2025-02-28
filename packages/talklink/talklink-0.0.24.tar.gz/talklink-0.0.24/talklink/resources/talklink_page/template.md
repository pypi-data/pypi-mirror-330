<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ video_title }}</title>
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100..900;1,100..900&display=swap');
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    {% if create_isolated_html %}
    <style>
    {% include "styles.css" %}
    </style>
    {% else %}
    <link rel="stylesheet" href="{{styles_file_path}}">
    {% endif %}
</head>
<body class="dark-mode">
    <div class="container">
        <header class="header">
            <div class="header-left">
                <a href="{{toc}}">
                <svg class="logo" fill="currentColor" viewBox="0 0 1024 1024" fill="#000000" class="icon" version="1.1" xmlns="http://www.w3.org/2000/svg"><path d="M344.854 687.167c26.725 56.8 66.665 111.099 118.91 161.654-109.515-16.445-200.574-83.285-250.026-175.73l131.114 14.076zM461.776 177.924c-106.691 16.718-195.535 81.185-245.233 170.432l128.342-12.64c26.395-55.654 65.729-108.624 116.89-157.793zM502.016 337.406l1.78-163.191h-0.362c-57.402 50.103-101.083 104.341-130.194 161.745l128.774 1.45zM224.829 388.081l-23.709-0.211-23.439-0.304-1.84 169.497-94.898-170.523-52.909-0.575-2.593 241.198 23.589 0.331 23.468 0.211 1.871-173.871 97.645 174.957 50.256 0.575 2.564-241.289zM450.373 433.36l0.211-21.506 0.271-21.357-177.611-1.9-2.593 241.289 183.132 1.93 0.241-21.446 0.211-21.387-132.697-1.418 0.663-62.954 117.977 1.266 0.211-20.694 0.211-20.814-117.977-1.238 0.575-51.161 127.175 1.387zM691.15 568.256l-33.06-175.501-53.664-0.635-36.349 176.255-38.43-177.009-52.397-0.603 64.553 242.012 23.922 0.241 23.981 0.304 39.907-189.616 36.711 190.401 24.071 0.331 23.889 0.241 69.742-240.566-50.949-0.544-41.929 174.687zM529.708 174.514h-0.362l-1.748 163.162 128.866 1.359c-27.932-58.038-70.404-113.18-126.754-164.521zM804.932 340.603c-53.633-89.519-145.152-151.602-251.828-164.202 68.335 52.922 106.493 106.707 131.741 162.933l120.086 1.266zM554.925 849.786c109.455-14.028 201.386-78.448 252.927-168.876l-130.547 9.845c-27.963 56.197-69.108 109.589-122.378 159.030zM648.738 690.455l-124.914-1.359-1.69 155.833c54.961-47.872 97.462-99.846 126.602-154.475zM981.396 521.109c-11.763-10.407-35.052-19.757-70.074-27.873-24.132-5.791-39.907-10.528-47.267-14.629-7.513-3.953-11.283-9.593-11.191-16.861 0.061-9.923 3.771-17.979 11.101-23.5 7.209-5.34 17.283-8.084 30.044-7.904 14.781 0.121 26.725 3.682 35.867 10.407 9.079 6.788 13.998 15.867 14.721 27.391l49.077 0.603c-1.569-24.282-10.769-43.469-27.6-57.887-16.741-14.419-38.703-21.748-65.729-22.020-28.837-0.331-51.852 6.335-68.956 19.728-17.073 13.546-25.73 32.246-25.973 55.535-0.211 20.905 6.004 36.349 18.642 46.393 12.819 9.984 38.338 19.517 76.469 28.415 20.753 4.827 34.238 9.562 40.572 13.786 6.395 4.346 9.593 10.979 9.502 20.151-0.090 9.199-4.705 16.259-13.786 21.387-9.109 5.068-21.628 7.54-37.766 7.359-15.596-0.181-27.813-3.71-36.439-10.738-8.746-6.91-13.212-16.711-13.634-29.652l-48.534-0.512c0.875 26.063 9.895 46.213 26.908 60.511 17.043 14.419 40.844 21.689 71.278 21.989 30.495 0.304 54.598-5.942 72.578-19.154 18.038-13.151 27.088-30.979 27.328-53.664 0.362-22.503-5.429-38.974-17.134-49.26zM496.586 844.508l1.69-155.651-124.914-1.359c28.053 55.201 69.348 108.050 123.223 157.009z" /></svg>
                </a>
            </div>
            <div class="header-center">
                <input type="text" id="searchBar" placeholder="Type '/' to search" 
                       onkeyup="filterTranscript()" 
                       onkeydown="if(event.key==='Escape'){event.preventDefault();}">
            </div>
            <div class="header-right">
                <button id="dark-mode-toggle" class="header-button" onClick="toggleDarkMode()" aria-label="Toggle dark mode"><i class="fas fa-moon"></i></button>
            </div>
        </header>
        <main id="main-container">
            <!-- Common filter dropdown that works for both views -->
            <div id="common-filter-dropdown" class="filter-dropdown">
                <div id="filterOptions" class="filter-options">
                    {% for speaker in speakers %}
                    <button onclick="filterBySpeaker('{{ speaker }}')">{{ speaker }}</button>
                    {% endfor %}
                </div>
            </div>
            
            <section id="transcript-list" class="speaker-list-section">
                <div class="list-button-container">
                    <div class="tab active" id="transcript-tab" onclick="toggleTranscript()">Transcript</div>
                    <div class="tab inactive" id="claims-tab" onclick="toggleClaims()">Claims</div>
                </div>
                <button class="tools-toggle" onclick="toggleTools()">Tools <i>▼</i></button>
                <div id="extra-tools">
                    <div class="filter-dropdown">
                        <button class="tool-button" onclick="toggleFilterDropdown()">Filter by speaker</button>
                    </div>
                    <div>
                        <button class="tool-button" onclick="getVideoTime()">Catchup to video</button>
                    </div>
                    <div>
                        <button class="tool-button" onclick="toggleAssignSpeakers()">Assign speakers</button>
                    </div>
                </div>
                <div class="speaker-list">
                    <ul>
                        {% for utterance in transcript.utterances %}
                        <li class="talk-item" data-speaker="{{ utterance.speaker }}" data-start-time="{{ utterance.start_time }}">
                            <span class="badge" style="background-color: {{ badgeColor[utterance.speaker] }}; color: #ffffff;">{{ utterance.speaker }}</span>
                            <div class="talk-content">
                                <span class="talk-text">{{ utterance.text }}</span>
                                <div class="talk-actions">
                                    <a href="#" onclick="jumpToTime({{ utterance.start_time }})" class="time">({{ format_timestamp(utterance.start_time) }})</a>
                                    <button class="options-button" onclick="toggleOptions(event)">...</button>
                                    <div class="options-popup" style="display: none;">
                                        <button onclick="copyToClipboard(event)">Copy text</button>
                                        <button onclick="copyLinkToClipboard(event, {{ utterance.start_time }})">Copy link</button>
                                        <button class="close-button" onclick="closePopup(event)">Cancel</button>
                                    </div>
                                </div>
                            </div>
                        </li>
                        {% endfor %}
                    </ul>
                </div>
            </section>
            
            <section id="claims-list" class="speaker-list-section hidden">
                <div class="list-button-container">
                    <div class="tab inactive" id="transcript-tab" onclick="toggleTranscript()">Transcript</div>
                    <div class="tab active" id="claims-tab" onclick="toggleClaims()">Claims</div>
                </div>
                <button class="tools-toggle" onclick="toggleTools()">Tools <i>▼</i></button>
                <div id="extra-tools">
                    <div class="filter-dropdown">
                        <button class="tool-button" onclick="toggleFilterDropdown()">Filter by speaker</button>
                    </div>
                    <div>
                        <button class="tool-button" onclick="getVideoTime()">Catchup to video</button>
                    </div>
                    <div>
                        <button class="tool-button" onclick="toggleAssignSpeakers()">Assign speakers</button>
                    </div>
                </div>
                <div class="speaker-list">
                    <ul> 
                        {% for utterance in claims.utterances %}
                        {% for claim in utterance.claims %}
                        <li class="talk-item claim-opinion" data-speaker="{{ utterance.speaker }}" data-start-time="{{ utterance.start_time }}">
                            <span class="badge" style="background-color: {{ badgeColor[utterance.speaker] }}; color: #ffffff;">{{ utterance.speaker }}</span>
                            <div class="talk-content">
                                <span class="talk-text">{{ claim.text }}</span>
                                <div class="talk-actions">
                                    <span class="claim-badge" style="background-color: {{ claimTypeColors[claim.type|default('general')] }};">{{ claim.type|default('general') }}</span>
                                    <a href="#" onclick="jumpToTime({{ utterance.start_time }})" class="time">({{ format_timestamp(utterance.start_time) }})</a>
                                    <button class="options-button" onclick="toggleOptions(event)">...</button>
                                    <div class="options-popup" style="display: none;">
                                        <button onclick="copyToClipboard(event)">Copy text</button>
                                        <button onclick="copyLinkToClipboard(event, {{ utterance.start_time }})">Copy link</button>
                                        <button class="close-button" onclick="closePopup(event)">Cancel</button>
                                    </div>
                                </div>
                            </div>
                        </li>
                        {% endfor %}
                        {% endfor %}
                    </ul>
                </div>
            </section>
            
            <!-- Resizable divider -->
            <div id="resizable-divider" class="resizable-divider">
                <div class="divider-handle"></div>
            </div>
            
            <section id="video-section" tabindex="0">
                <div id="video-player" class="responsive-video"></div>
                <script>
                    var player;
                    function onYouTubeIframeAPIReady() {
                        player = new YT.Player('video-player', {
                            videoId: '{{ video_id }}',
                            events: {
                                'onReady': onPlayerReady,
                                'onStateChange': onPlayerStateChange
                            },
                            playerVars: {
                                enablejsapi: 1,
                                playsinline: 1
                            }
                        });
                    }
                </script>
            </section>
        </main>
    </div>
    <div id="assignSpeakersModal" class="modal" style="display: none;">
        <div class="modal-content">
            <span class="close" onclick="closeModal()">&times;</span>
            <div class="modal-header">
                <h2>Assign Speakers</h2>
            </div>
            <div class="modal-body">
                <form id="speaker-form" onsubmit="saveAssignments(event)">
                    <div id="speaker-inputs"></div>
                    <div class="speaker-form-actions">
                        <button type="submit">Save</button>
                        <button type="button" onclick="exportSpeakerMap()" class="export-button">Export JSON</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
    <div id="helpModal" class="modal" style="display: none;">
        <div class="modal-content">
            <span class="close" onclick="closeHelp()">&times;</span>
            <div class="modal-header">
                <h2>Help</h2>
            </div>
            <div class="modal-body">
                <h3>Welcome to TalkLink!</h3>
                <p>TalkLink helps you navigate video content easily. Here's how to use all the features:</p>
                
                <h4>Navigation</h4>
                <ul>
                    <li><strong>Transcript/Claims Tabs:</strong> Switch between full transcript and key claims extracted from the video.</li>
                    <li><strong>Search Bar:</strong> Type '/' to focus the search bar. Enter keywords to find specific content in the transcript or claims.</li>
                    <li><strong>Dark Mode:</strong> Toggle between light and dark mode using the sun/moon button in the header.</li>
                </ul>
                
                <h4>Video Interaction</h4>
                <ul>
                    <li><strong>Jump to Time:</strong> Click on any timestamp to jump to that exact moment in the video.</li>
                    <li><strong>Catchup to Video:</strong> Click "Catchup to video" to scroll the transcript to match the current video playback position.</li>
                </ul>
                
                <h4>Content Management</h4>
                <ul>
                    <li><strong>Filter by Speaker:</strong> Click "Filter by speaker" to show only statements from specific speakers.</li>
                    <li><strong>Assign Speakers:</strong> Rename speakers for better identification using the "Assign speakers" button.</li>
                    <li><strong>Options Menu (...):</strong> Click the three dots next to any statement to:
                        <ul>
                            <li>Copy the text of that statement</li>
                            <li>Copy a direct link to that moment in the video</li>
                        </ul>
                    </li>
                </ul>
                
                <h4>Claims View</h4>
                <ul>
                    <li><strong>Claim Types:</strong> In the Claims tab, each claim is labeled with its type (fact, opinion, etc.) with a colored badge.</li>
                    <li><strong>Claim Navigation:</strong> Claims provide a condensed view of the key points made in the video.</li>
                </ul>
                
                <h4>Keyboard Shortcuts</h4>
                <div class="keyboard-shortcuts-container">
                    <div class="shortcuts-column">
                        <h5>Navigation</h5>
                        <ul>
                            <li><strong>j</strong> or <strong>↓</strong> - Next item</li>
                            <li><strong>k</strong> or <strong>↑</strong> - Previous item</li>
                            <li><strong>g</strong> - Go to first item</li>
                            <li><strong>G</strong> - Go to last item</li>
                            <li><strong>h</strong> - Catchup to video</li>
                        </ul>
                        
                        <h5>Tabs & Tools</h5>
                        <ul>
                            <li><strong>t</strong> - Switch to Transcript</li>
                            <li><strong>c</strong> - Switch to Claims</li>
                            <li><strong>a</strong> - Assign speakers</li>
                        </ul>
                    </div>
                    
                    <div class="shortcuts-column">
                        <h5>Search</h5>
                        <ul>
                            <li><strong>/</strong> or <strong>f</strong> - Focus search bar</li>
                        </ul>
                        
                        <h5>Video Controls</h5>
                        <ul>
                            <li><strong>v</strong> - Toggle video focus on/off</li>
                            <li><strong>Space</strong> - Play/Pause video (when focused)</li>
                            <li><strong>←</strong> - Rewind 5 seconds (when focused)</li>
                            <li><strong>→</strong> - Forward 5 seconds (when focused)</li>
                            <li><strong>↑</strong> - Increase volume (when focused)</li>
                            <li><strong>↓</strong> - Decrease volume (when focused)</li>
                            <li><strong>m</strong> - Mute/Unmute (when focused)</li>
                        </ul>
                        
                        <h5>Focused Item Actions</h5>
                        <ul>
                            <li><strong>Enter</strong> - Jump to timestamp</li>
                            <li><strong>y</strong> - Copy text</li>
                            <li><strong>l</strong> - Copy link</li>
                        </ul>
                        
                        <h5>Other</h5>
                        <ul>
                            <li><strong>d</strong> - Toggle dark mode</li>
                            <li><strong>?</strong> - Show help</li>
                            <li><strong>Esc</strong> - Close popups/modals</li>
                        </ul>
                    </div>
                </div>
                
                <p>TalkLink makes video content more accessible by allowing you to read, search, and navigate through transcripts and key points with ease!</p>
            </div>
        </div>
    </div>  
    
    <div class="help-button-container">
        <button id="help-button" onClick="toggleHelp()" aria-label="Help">?</button>
    </div>
    
    <div class="dark-mode-button-mobile">
        <button onClick="toggleDarkMode()" aria-label="Toggle dark mode"><i class="fas fa-moon"></i></button>
    </div>
    
    {% if create_isolated_html %}
    <script>
    {% include "script.js" %}
    </script>
    {% else %}
    <script src="{{script_file_path}}"></script>
    {% endif %}
    <script>
        // Initialize YouTube API
        var tag = document.createElement('script');
        tag.src = "https://www.youtube.com/iframe_api";
        var firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
        
        // ... existing script code ...
        
        // Resizable divider functionality
        function initResizableDivider() {
            const divider = document.getElementById('resizable-divider');
            const speakerList = document.getElementById('transcript-list');
            const claimsList = document.getElementById('claims-list');
            const videoSection = document.getElementById('video-section');
            const container = document.getElementById('main-container');
            
            // Only enable on desktop
            if (window.innerWidth <= 768) {
                divider.style.display = 'none';
                return;
            }
            
            let isDragging = false;
            let startX, startSpeakerWidth, startVideoWidth;
            
            // Improved mouse event handlers with better cleanup
            function handleMouseDown(e) {
                // Prevent any ongoing drag operation
                if (isDragging) {
                    handleMouseUp();
                }
                
                isDragging = true;
                divider.classList.add('dragging');
                startX = e.clientX;
                
                // Get the current widths
                const activeList = document.querySelector('.speaker-list-section:not(.hidden)');
                startSpeakerWidth = activeList.offsetWidth;
                startVideoWidth = videoSection.offsetWidth;
                
                // Prevent text selection during drag
                document.body.style.userSelect = 'none';
                document.body.style.cursor = 'col-resize'; // Change cursor for entire body during drag
                
                // Disable pointer events on the video to prevent it from capturing mouse events
                videoSection.style.pointerEvents = 'none';
                
                // Add event listeners for dragging - attach to window for better tracking
                window.addEventListener('mousemove', handleMouseMove, true);
                window.addEventListener('mouseup', handleMouseUp, true);
                
                e.preventDefault();
                e.stopPropagation();
            }
            
            // Track the last position to smooth out rapid movements
            let lastX = null;
            let lastDx = 0;
            
            function handleMouseMove(e) {
                if (!isDragging) return;
                
                // Ensure the event is handled at this level
                e.preventDefault();
                e.stopPropagation();
                
                const activeList = document.querySelector('.speaker-list-section:not(.hidden)');
                const containerWidth = container.offsetWidth;
                
                // Get current mouse position
                const currentX = e.clientX;
                
                // If this is the first move after mousedown, initialize lastX
                if (lastX === null) {
                    lastX = startX;
                }
                
                // Calculate raw delta
                const rawDx = currentX - startX;
                
                // Apply smoothing for rapid direction changes
                // Use a weighted average of current and previous movement
                const smoothingFactor = 0.8; // Increased for more responsiveness
                const smoothedDx = (rawDx * smoothingFactor) + (lastDx * (1 - smoothingFactor));
                
                // Apply sensitivity after smoothing
                const sensitivity = 1.0; // Neutral sensitivity for more predictable movement
                const dx = smoothedDx * sensitivity;
                
                // Store for next calculation
                lastDx = smoothedDx;
                lastX = currentX;
                
                // Calculate new widths with bounds checking
                let newSpeakerWidth = ((startSpeakerWidth + dx) / containerWidth * 100);
                let newVideoWidth = ((startVideoWidth - dx) / containerWidth * 100);
                
                // Apply min width constraints (in percentage)
                const minWidth = 300 / containerWidth * 100;
                const maxWidth = 100 - minWidth;
                
                // Clamp values to ensure they stay within bounds
                newSpeakerWidth = Math.max(minWidth, Math.min(maxWidth, newSpeakerWidth));
                newVideoWidth = 100 - newSpeakerWidth;
                
                // Apply the new widths with requestAnimationFrame for smoother updates
                requestAnimationFrame(() => {
                    // Apply the new widths
                    activeList.style.width = `${newSpeakerWidth}%`;
                    videoSection.style.width = `${newVideoWidth}%`;
                    
                    // Also update the other list (claims or transcript) to maintain consistency
                    if (activeList === speakerList) {
                        claimsList.style.width = `${newSpeakerWidth}%`;
                    } else {
                        speakerList.style.width = `${newSpeakerWidth}%`;
                    }
                    
                    // Apply responsive styling based on width
                    applyResponsiveStyling(newSpeakerWidth, containerWidth);
                });
            }
            
            function handleMouseUp(e) {
                if (!isDragging) return;
                
                // Clean up
                isDragging = false;
                divider.classList.remove('dragging');
                document.body.style.userSelect = '';
                document.body.style.cursor = ''; // Reset cursor
                
                // Re-enable pointer events on the video
                videoSection.style.pointerEvents = '';
                
                // Reset tracking variables
                lastX = null;
                lastDx = 0;
                
                // Remove all event listeners - use capture phase to match the add
                window.removeEventListener('mousemove', handleMouseMove, true);
                window.removeEventListener('mouseup', handleMouseUp, true);
                
                // Prevent any default behavior
                if (e) {
                    e.preventDefault();
                    e.stopPropagation();
                }
            }
            
            // Function to apply responsive styling based on width
            function applyResponsiveStyling(widthPercent, containerWidth) {
                const actualWidth = (widthPercent / 100) * containerWidth;
                const speakerListSections = document.querySelectorAll('.speaker-list-section');
                
                speakerListSections.forEach(section => {
                    // When width gets too narrow
                    if (actualWidth < 400) {
                        section.classList.add('narrow-view');
                    } else {
                        section.classList.remove('narrow-view');
                    }
                    
                    // Extra narrow view
                    if (actualWidth < 350) {
                        section.classList.add('extra-narrow-view');
                    } else {
                        section.classList.remove('extra-narrow-view');
                    }
                });
            }
            
            // Add event listener for mouse down on the divider
            divider.addEventListener('mousedown', handleMouseDown);
            
            // Handle window resize
            window.addEventListener('resize', function() {
                // Force cleanup any ongoing drag operation
                if (isDragging) {
                    handleMouseUp();
                }
                
                if (window.innerWidth <= 768) {
                    divider.style.display = 'none';
                    
                    // Reset widths for mobile view
                    speakerList.style.width = '';
                    claimsList.style.width = '';
                    videoSection.style.width = '';
                    
                    // Remove responsive classes
                    document.querySelectorAll('.speaker-list-section').forEach(section => {
                        section.classList.remove('narrow-view', 'extra-narrow-view');
                    });
                } else {
                    divider.style.display = 'flex';
                    
                    // Check if we need to apply responsive styling
                    const activeList = document.querySelector('.speaker-list-section:not(.hidden)');
                    if (activeList) {
                        const containerWidth = container.offsetWidth;
                        const listWidthPercent = (activeList.offsetWidth / containerWidth) * 100;
                        applyResponsiveStyling(listWidthPercent, containerWidth);
                    }
                }
            });
            
            // Initial check for responsive styling
            const activeList = document.querySelector('.speaker-list-section:not(.hidden)');
            if (activeList) {
                const containerWidth = container.offsetWidth;
                const listWidthPercent = (activeList.offsetWidth / containerWidth) * 100;
                applyResponsiveStyling(listWidthPercent, containerWidth);
            }
        }
        
        // Initialize resizable divider when DOM is loaded
        document.addEventListener('DOMContentLoaded', function() {
            initResizableDivider();
        });
    </script>
</body>
</html>
