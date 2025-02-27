// FZY.JS
(function () {
    const SCORE_MIN = -1 / 0,
      SCORE_MAX = 1 / 0,
      SCORE_GAP_LEADING = -0.000005,
      SCORE_GAP_TRAILING = -0.000005,
      SCORE_GAP_INNER = -0.000001,
      SCORE_MATCH_CONSECUTIVE = 1,
      SCORE_MATCH_SLASH = 0.4,
      SCORE_MATCH_WORD = 0.95,
      SCORE_MATCH_CAPITAL = 0.1,
      SCORE_MATCH_DOT = 0.6;

    function islower(r) {
      return r.toLowerCase() === r;
    }
    function isupper(r) {
      return r.toUpperCase() === r;
    }
    function precompute_bonus(r) {
      for (var C = r.length, _ = new Array(C), e = "/", t = 0; t < C; t++) {
        var A = r[t];
        "/" === e
          ? (_[t] = SCORE_MATCH_SLASH)
          : "-" === e || "_" === e || " " === e
          ? (_[t] = SCORE_MATCH_WORD)
          : "." === e
          ? (_[t] = SCORE_MATCH_DOT)
          : islower(e) && isupper(A)
          ? (_[t] = SCORE_MATCH_CAPITAL)
          : (_[t] = 0),
          (e = A);
      }
      return _;
    }
    function compute(r, C, _, e) {
      for (
        var t = r.length,
          A = C.length,
          E = r.toLowerCase(),
          O = C.toLowerCase(),
          o = precompute_bonus(C),
          S = 0;
        S < t;
        S++
      ) {
        (_[S] = new Array(A)), (e[S] = new Array(A));
        for (
          var R = SCORE_MIN,
            n = S === t - 1 ? SCORE_GAP_TRAILING : SCORE_GAP_INNER,
            s = 0;
          s < A;
          s++
        )
          if (E[S] === O[s]) {
            var M = SCORE_MIN;
            S
              ? s &&
                (M = Math.max(
                  e[S - 1][s - 1] + o[s],
                  _[S - 1][s - 1] + SCORE_MATCH_CONSECUTIVE
                ))
              : (M = s * SCORE_GAP_LEADING + o[s]),
              (_[S][s] = M),
              (e[S][s] = R = Math.max(M, R + n));
          } else (_[S][s] = SCORE_MIN), (e[S][s] = R += n);
      }
    }
    function score(r, C) {
      var _ = r.length,
        e = C.length;
      if (!_ || !e) return SCORE_MIN;
      if (_ === e) return SCORE_MAX;
      if (e > 1024) return SCORE_MIN;
      var t = new Array(_),
        A = new Array(_);
      return compute(r, C, t, A), A[_ - 1][e - 1];
    }
    function positions(r, C) {
      var _ = r.length,
        e = C.length,
        t = new Array(_);
      if (!_ || !e) return t;
      if (_ === e) {
        for (var A = 0; A < _; A++) t[A] = A;
        return t;
      }
      if (e > 1024) return t;
      var E = new Array(_),
        O = new Array(_);
      compute(r, C, E, O);
      for (var o = !1, S = (A = _ - 1, e - 1); A >= 0; A--)
        for (; S >= 0; S--)
          if (
            E[A][S] !== SCORE_MIN &&
            (o || E[A][S] === O[A][S])
          ) {
            (o = A && S && O[A][S] === E[A - 1][S - 1] + SCORE_MATCH_CONSECUTIVE),
              (t[A] = S--);
            break;
          }
      return t;
    }
    function hasMatch(r, C) {
      (r = r.toLowerCase()), (C = C.toLowerCase());
      for (var _ = r.length, e = 0, t = 0; e < _; e += 1)
        if (0 === (t = C.indexOf(r[e], t) + 1)) return !1;
      return !0;
    }

    // Expose functions and constants to the global scope
    window.stringScoring = {
      SCORE_GAP_INNER,
      SCORE_GAP_LEADING,
      SCORE_GAP_TRAILING,
      SCORE_MATCH_CAPITAL,
      SCORE_MATCH_CONSECUTIVE,
      SCORE_MATCH_DOT,
      SCORE_MATCH_SLASH,
      SCORE_MATCH_WORD,
      SCORE_MAX,
      SCORE_MIN,
      hasMatch,
      positions,
      score,
    };
  })();

// SCRIPT.JS
const selectedSpeakers = new Set();

function filterTranscript() {
    const searchInput = document.getElementById('searchBar').value.toLowerCase();
    const items = Array.from(document.querySelectorAll('.talk-item'));

    // Check if search input is empty
    if (searchInput === '') {
        items.forEach(item => {
            // Ensure speaker filters are respected when search input is empty
            const matchesSpeaker = selectedSpeakers.size === 0 || selectedSpeakers.has(item.getAttribute('data-speaker'));
            item.style.display = matchesSpeaker ? '' : 'none'; // Show all items if search input is empty and matches speaker
            item.querySelector('.talk-text').innerHTML = item.querySelector('.talk-text').textContent; // Reset to original text
        });
        return; // Exit the function early
    }

    // Split search input into words for matching
    const searchWords = searchInput.split(' ');

    // Filter items based on fuzzy matching and selected speakers
    const filteredItems = items.filter(item => {
        const text = item.querySelector('.talk-text').textContent.toLowerCase();
        const matchesSearch = searchWords.some(word => item.textContent.toLowerCase().includes(word)); // Check if any word matches
        const matchesSpeaker = selectedSpeakers.size === 0 || selectedSpeakers.has(item.getAttribute('data-speaker')); // Check if item matches selected speakers
        return matchesSearch && matchesSpeaker; // Return true if both conditions are met
    });

    // Highlight matched text
    items.forEach(item => {
        const textElement = item.querySelector('.talk-text');
        const originalText = textElement.textContent; // Store original text
        if (searchInput) {
            const regex = new RegExp(`(${searchInput.replace(/\s+/g, '\\s*')})`, 'gi'); // Create a regex for the search input, allowing for whitespace variations
            textElement.innerHTML = originalText.replace(regex, '<span class="highlight">$1</span>'); // Highlight matches
        } else {
            textElement.innerHTML = originalText; // Reset to original text if search input is empty
        }
    });

    // Sort filtered items by score
    filteredItems.sort((a, b) => {
        const scoreA = searchWords.reduce((score, word) => {
            const matchScore = window.stringScoring.score(word, a.textContent.toLowerCase());
            return score + (matchScore > 0 ? matchScore : 0); // Add match score or 0 if no match
        }, 0);
        
        const scoreB = searchWords.reduce((score, word) => {
            const matchScore = window.stringScoring.score(word, b.textContent.toLowerCase());
            return score + (matchScore > 0 ? matchScore : 0); // Add match score or 0 if no match
        }, 0);

        return scoreB - scoreA; // Sort in descending order
    });

    // Show the top 10 results
    const topItems = filteredItems.slice(0, 20);

    // Hide all items first
    items.forEach(item => item.style.display = 'none');

    // Show only the top items
    topItems.forEach(item => item.style.display = '');
}

function toggleList() {
    console.log("toggleList");
    const transcriptList = document.getElementById('transcript-list');
    const claimsList = document.getElementById('claims-list');
    
    transcriptList.classList.toggle('hidden');
    claimsList.classList.toggle('hidden');

    // Update active tab
    const transcriptTab = document.getElementById('transcript-tab');
    const claimsTab = document.getElementById('claims-tab');
    
    if (transcriptList.classList.contains('hidden')) {
        transcriptTab.classList.remove('active');
        transcriptTab.classList.add('inactive'); // Add inactive class
        claimsTab.classList.add('active');
        claimsTab.classList.remove('inactive'); // Remove inactive class
    } else {
        transcriptTab.classList.toggle('active');
        transcriptTab.classList.remove('inactive'); // Remove inactive class
        claimsTab.classList.remove('active');
        claimsTab.classList.add('inactive'); // Add inactive class
    }
}

function toggleClaims() {
    console.log("toggleList");
    const transcriptList = document.getElementById('transcript-list');
    const claimsList = document.getElementById('claims-list');
    
    transcriptList.classList.toggle('hidden');
    claimsList.classList.toggle('hidden');

    // Update active tab
    const transcriptTab = document.getElementById('transcript-tab');
    const claimsTab = document.getElementById('claims-tab');
    
    if (transcriptList.classList.contains('hidden')) {
        transcriptTab.classList.remove('active');
        transcriptTab.classList.add('inactive'); // Add inactive class
        claimsTab.classList.add('active');
        claimsTab.classList.remove('inactive'); // Remove inactive class
        
        // Show notification
        showFocusNotification("Switched to Claims view");
    } else {
        transcriptTab.classList.toggle('active');
        transcriptTab.classList.remove('inactive'); // Remove inactive class
        claimsTab.classList.remove('active');
        claimsTab.classList.add('inactive'); // Add inactive class
        
        // Show notification
        showFocusNotification("Switched to Transcript view");
    }
}

function toggleTranscript() {
    console.log("toggleList");
    const transcriptList = document.getElementById('transcript-list');
    const claimsList = document.getElementById('claims-list');
    
    transcriptList.classList.toggle('hidden');
    claimsList.classList.toggle('hidden');

    // Update active tab
    const transcriptTab = document.getElementById('transcript-tab');
    const claimsTab = document.getElementById('claims-tab');
    
    if (transcriptList.classList.contains('hidden')) {
        transcriptTab.classList.remove('active');
        transcriptTab.classList.add('inactive'); // Add inactive class
        claimsTab.classList.add('active');
        claimsTab.classList.remove('inactive'); // Remove inactive class
        
        // Show notification
        showFocusNotification("Switched to Claims view");
    } else {
        transcriptTab.classList.toggle('active');
        transcriptTab.classList.remove('inactive'); // Remove inactive class
        claimsTab.classList.remove('active');
        claimsTab.classList.add('inactive'); // Add inactive class
        
        // Show notification
        showFocusNotification("Switched to Transcript view");
    }
}

function toggleHelp() {
    const helpModal = document.getElementById('helpModal');
    if (!helpModal) return; // Safety check
    
    if (helpModal.style.display === 'block') {
        helpModal.style.display = 'none';
        document.body.classList.remove('modal-open');
    } else {
        helpModal.style.display = 'block';
        document.body.classList.add('modal-open');
        
        // Ensure the modal is visible by forcing a reflow
        helpModal.offsetHeight;
    }
}

function closeHelp() {
    const helpModal = document.getElementById('helpModal');
    if (!helpModal) return; // Safety check
    
    helpModal.style.display = 'none';
    document.body.classList.remove('modal-open');
}

function toggleTheme() {
    const body = document.body;
    body.classList.toggle('dark');
}

function scrollToTime(seconds) {
    var list = document.getElementById('transcript-list');
    if (list.classList.contains('hidden')) {
        list = document.getElementById('claims-list');
    }
    const items = list.querySelectorAll('.talk-item');
    items.forEach(item => {
        const startTime = item.getAttribute('data-start-time');
        if (startTime <= seconds) {
            item.scrollIntoView({ behavior: 'smooth' });
        }
    });
}

function jumpToTime(seconds) {
    const iframe = document.querySelector('#video-section iframe');
    const originalSrc = iframe.src.split('?')[0]; // Get the original src without query parameters
    //iframe.src = `${originalSrc}?start=${seconds}&autoplay=1`; // Reset src and add new timestamp
    player.seekTo(seconds);
    
    // Format the timestamp for display (MM:SS)
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    const formattedTime = `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
    
    // Show notification
    showFocusNotification(`Jumped to ${formattedTime}`);
}

function toggleOptions(event) {
    const popup = event.target.nextElementSibling; // Get the next sibling (the popup)
    if (popup) {
        // Toggle display
        popup.style.display = (popup.style.display === "block") ? "none" : "block"; // Ensure it toggles between block and none
    }
}

function closePopup(event) {
    const popup = event.target.closest('.options-popup');
    if (popup) {
        popup.style.display = 'none'; // Hide the popup
    }
}

function copyToClipboard(event) {
    const transcriptItem = event.target.closest('.talk-item'); // Get the closest transcript item
    if (transcriptItem) {
        const textToCopy = transcriptItem.querySelector('.talk-text').textContent; // Get the text from the span with class 'talk-text'
        navigator.clipboard.writeText(textToCopy) // Copy to clipboard
            .then(() => {
                showFocusNotification("Text copied to clipboard");
            })
            .catch(err => {
                showFocusNotification("Failed to copy text");
                console.error('Failed to copy: ', err);
            });
    }

    const popup = event.target.closest('.options-popup');
    if (popup) {
        popup.style.display = 'none'; // Hide the popup
    }
}

function copyLinkToClipboard(event, timestamp) {  // Accept timestamp as a parameter
    const transcriptItem = event.target.closest('.talk-item'); // Get the closest transcript item
    
    // Get the video ID directly from the player object
    let videoId;
    
    try {
        // First try to get it from the player object
        if (player && player.getVideoData) {
            videoId = player.getVideoData().video_id;
        }
        
        // If that fails, try the old method as fallback
        if (!videoId) {
            const iframeSrc = document.querySelector('#video-section iframe').src;
            const videoIdMatch = iframeSrc.match(/embed\/([a-zA-Z0-9_-]+)/);
            videoId = videoIdMatch ? videoIdMatch[1] : null;
        }
        
        if (videoId) {
            const linkToCopy = `https://www.youtube.com/watch?v=${videoId}&t=${timestamp}s`; // Generate the link with timestamp
            navigator.clipboard.writeText(linkToCopy) // Copy to clipboard
                .then(() => {
                    console.log('Link copied to clipboard!');
                    // Format the timestamp for display (MM:SS)
                    const minutes = Math.floor(timestamp / 60);
                    const remainingSeconds = Math.floor(timestamp % 60);
                    const formattedTime = `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
                    showFocusNotification(`Link to ${formattedTime} copied`);
                })
                .catch(err => {
                    showFocusNotification("Failed to copy link");
                    console.error('Failed to copy: ', err); // Error handling
                });
        } else {
            showFocusNotification("Failed to get video ID");
            console.error('Failed to get video ID');
        }
    } catch (err) {
        showFocusNotification("Failed to copy link");
        console.error('Failed to copy link: ', err);
    }
    
    // Close the popup if it exists
    const popup = event.target.closest('.options-popup');
    if (popup) {
        popup.style.display = 'none'; // Hide the popup
    }
}

function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    
    // Update header dark mode button
    const darkModeButton = document.getElementById('dark-mode-toggle');
    if (darkModeButton) {
        const icon = darkModeButton.querySelector('i');
        if (document.body.classList.contains('dark-mode')) {
            icon.className = 'fas fa-sun';
        } else {
            icon.className = 'fas fa-moon';
        }
    }
    
    // Update mobile dark mode button
    const mobileDarkModeButton = document.querySelector('.dark-mode-button-mobile button');
    if (mobileDarkModeButton) {
        const icon = mobileDarkModeButton.querySelector('i');
        if (document.body.classList.contains('dark-mode')) {
            icon.className = 'fas fa-sun';
        } else {
            icon.className = 'fas fa-moon';
        }
    }
    
    // Save preference to localStorage
    if (document.body.classList.contains('dark-mode')) {
        localStorage.setItem('darkMode', 'enabled');
    } else {
        localStorage.setItem('darkMode', 'disabled');
    }
}

function toggleFilterDropdown() {
    const filterOptions = document.getElementById('filterOptions');
    
    if (filterOptions) {
        // Toggle the display of the filter options
        if (filterOptions.classList.contains('active')) {
            filterOptions.classList.remove('active');
        } else {
            // Position the dropdown near the button that was clicked
            const button = event.target.closest('.tool-button');
            if (button) {
                const rect = button.getBoundingClientRect();
                const filterDropdown = document.getElementById('common-filter-dropdown');
                
                // Position the dropdown below the button
                filterDropdown.style.position = 'absolute';
                filterDropdown.style.top = `${rect.bottom}px`;
                filterDropdown.style.left = `${rect.left}px`;
                filterDropdown.style.zIndex = '1000';
            }
            
            filterOptions.classList.add('active');
        }
    } else {
        console.error("Element with ID 'filterOptions' not found.");
    }
}

function closeFilterDropdown() {
    const filterOptions = document.getElementById('filterOptions');
    if (filterOptions) {
        filterOptions.classList.remove('active');
    }
}

function filterBySpeaker(speaker) {
    const items = document.querySelectorAll('.talk-item');
    const filterButtons = document.querySelectorAll('#filterOptions button');

    // Toggle the selected speaker
    if (selectedSpeakers.has(speaker)) {
        selectedSpeakers.delete(speaker);
    } else {
        selectedSpeakers.add(speaker);
    }

    // Update the selected class on filter buttons
    filterButtons.forEach(button => {
        if (selectedSpeakers.has(button.textContent)) {
            button.classList.add('selected'); // Add selected class
        } else {
            button.classList.remove('selected'); // Remove selected class
        }
    });

    // Apply filtering to both transcript and claims views
    items.forEach(item => {
        item.style.display = selectedSpeakers.size === 0 || selectedSpeakers.has(item.getAttribute('data-speaker')) ? '' : 'none';
    });

    // Update the filter display
    updateFilterDisplay();
    
    // Show notification about the filter state
    if (selectedSpeakers.size === 0) {
        showFocusNotification("Showing all speakers");
    } else if (selectedSpeakers.size === 1) {
        showFocusNotification(`Filtered to speaker: ${Array.from(selectedSpeakers)[0]}`);
    } else {
        showFocusNotification(`Filtered to ${selectedSpeakers.size} speakers`);
    }
}

function updateFilterDisplay() {
    selectedSpeakers.forEach(speaker => {
        const speakerElement = document.createElement('span');
        speakerElement.textContent = speaker;
        speakerElement.onclick = () => {
            selectedSpeakers.delete(speaker);
            updateFilterDisplay(); // Update display after removal
            filterBySpeaker(''); // Refresh filter
        };
    });
}

window.addEventListener('keydown', function(event) {
    if (event.key === '/') {
        event.preventDefault(); // Prevent default action (e.g., scrolling)
        document.getElementById('searchBar').focus(); // Focus on the search bar
    }
    
    // Note: Escape key handling has been moved to the enhanced keyboard shortcut handler
    // to provide more comprehensive functionality and avoid conflicts
});

window.onclick = function(event) {
    // Close filter dropdown when clicking outside
    if (!event.target.matches('.filter-dropdown button') && 
        !event.target.matches('.tool-button') &&
        !event.target.matches('#filterOptions') && 
        !event.target.matches('#filterOptions *')) {
        closeFilterDropdown();
    }
    
    // Close options popup when clicking outside
    if (!event.target.matches('.options-button') && 
        !event.target.matches('.options-popup') && 
        !event.target.matches('.options-popup *')) {
        const popups = document.querySelectorAll('.options-popup');
        popups.forEach(popup => {
            if (popup.style.display === 'block') {
                popup.style.display = 'none';
            }
        });
    }
}

function toggleAssignSpeakers() {
    const modal = document.getElementById('assignSpeakersModal');
    const speakerInputs = document.getElementById('speaker-inputs');
    speakerInputs.innerHTML = ''; // Clear previous inputs

    // Get unique speakers
    const items = Array.from(document.querySelectorAll('.talk-item'));
    const uniqueSpeakers = new Set(items.map(item => item.getAttribute('data-speaker')));
    console.log("uniqueSpeakers", uniqueSpeakers);

    // Load saved speaker mappings from localStorage
    let savedMappings = {};
    try {
        // Get the current video ID
        let videoId;
        if (player && player.getVideoData) {
            videoId = player.getVideoData().video_id;
        }
        
        if (!videoId) {
            const iframeSrc = document.querySelector('#video-section iframe').src;
            const videoIdMatch = iframeSrc.match(/embed\/([a-zA-Z0-9_-]+)/);
            videoId = videoIdMatch ? videoIdMatch[1] : null;
        }
        
        if (videoId) {
            // Use video-specific storage key
            const storageKey = `speakerMappings_${videoId}`;
            const savedData = localStorage.getItem(storageKey);
            if (savedData) {
                savedMappings = JSON.parse(savedData);
                console.log(`Loaded saved speaker mappings for video ${videoId}:`, savedMappings);
            }
        } else {
            console.warn("Could not determine video ID for loading speaker mappings in modal");
        }
    } catch (error) {
        console.error("Error loading speaker mappings from localStorage:", error);
    }

    // Create input fields for each unique speaker
    uniqueSpeakers.forEach(speaker => {
        const div = document.createElement('div');
        // Use saved mapping if available
        const savedName = savedMappings[speaker] || '';
        div.innerHTML = `<div class="speaker-input-container">
            <label class="speaker-label">${speaker}</label>
            <input class="speaker-input" type="text" placeholder="Enter new name" value="${savedName}">
        </div>`;
        speakerInputs.appendChild(div);
    });

    // Add event listener for Escape key
    const handleEscapeKey = function(event) {
        if (event.key === 'Escape') {
            closeModal();
            document.removeEventListener('keydown', handleEscapeKey);
        }
    };
    document.addEventListener('keydown', handleEscapeKey);

    modal.style.display = 'block'; // Show the modal
    document.body.classList.add('modal-open'); // Prevent body scrolling
    
    // Focus the first input field
    const firstInput = modal.querySelector('.speaker-input');
    if (firstInput) {
        setTimeout(() => firstInput.focus(), 100);
    }
}

function closeModal() {
    const modal = document.getElementById('assignSpeakersModal');
    modal.style.display = 'none'; // Hide the modal
    document.body.classList.remove('modal-open'); // Re-enable body scrolling
}

function saveAssignments(event) {
    event.preventDefault(); // Prevent the default form submission

    const assignments = {}; // Object to hold speaker assignments
    const inputs = document.querySelectorAll('#speaker-inputs input'); // Get all input fields
    console.log("inputs", inputs);
    
    // Track changes for notification
    let changedSpeakers = 0;

    // For each input field, use its container to safely locate the associated label.
    inputs.forEach(input => {
        const label = input.parentElement.querySelector('label.speaker-label');
        if (label) {
            const originalSpeaker = label.textContent.trim();
            // If the input is empty, keep the original speaker name
            const newSpeaker = input.value.trim() || originalSpeaker;
            assignments[originalSpeaker] = newSpeaker;
            
            // Count changed speakers for notification
            if (newSpeaker !== originalSpeaker && input.value.trim() !== '') {
                changedSpeakers++;
            }
        }
    });

    console.log("Speaker assignments:", assignments); // Log the assignments for verification

    // Save to localStorage in the format that aligns with generate_speaker_map
    try {
        // Get the current video ID
        let videoId;
        if (player && player.getVideoData) {
            videoId = player.getVideoData().video_id;
        }
        
        if (!videoId) {
            const iframeSrc = document.querySelector('#video-section iframe').src;
            const videoIdMatch = iframeSrc.match(/embed\/([a-zA-Z0-9_-]+)/);
            videoId = videoIdMatch ? videoIdMatch[1] : null;
        }
        
        if (!videoId) {
            console.error("Could not determine video ID for speaker mappings");
            return;
        }
        
        // Create a speaker map in the format: {"Unknown A": "Real Name"}
        const speakerMap = {};
        Object.entries(assignments).forEach(([originalSpeaker, newSpeaker]) => {
            if (newSpeaker && newSpeaker !== originalSpeaker) {
                speakerMap[originalSpeaker] = newSpeaker;
            }
        });
        
        // Save to localStorage with video-specific key
        const storageKey = `speakerMappings_${videoId}`;
        localStorage.setItem(storageKey, JSON.stringify(speakerMap));
        console.log(`Saved speaker mappings to localStorage for video ${videoId}:`, speakerMap);
        
        // Reset the flag so that if we reload the page, the notification will show
        speakerMappingsLoaded = false;
    } catch (error) {
        console.error("Error saving speaker mappings to localStorage:", error);
    }

    // Update each talk item with the new assigned speaker names (if any)
    Object.entries(assignments).forEach(([oldSpeaker, newSpeaker]) => {
        console.log("oldSpeaker", oldSpeaker);
        const items = document.querySelectorAll(`.talk-item[data-speaker="${oldSpeaker}"]`);
        console.log("items", items);
        items.forEach(item => {
            // Update the data attribute for correctly filtered content later
            item.setAttribute('data-speaker', newSpeaker);
            // Also update the displayed badge text if present
            const badge = item.querySelector('.badge');
            if (badge) {
                badge.textContent = newSpeaker;
            }
        });
    });

    // Update the filter buttons to reflect any new speaker names
    updateFilterButtons();
    
    // Show notification about the changes
    if (changedSpeakers > 0) {
        showFocusNotification(`${changedSpeakers} speaker${changedSpeakers > 1 ? 's' : ''} renamed successfully`);
    } else {
        showFocusNotification("No speaker names were changed");
    }

    closeModal(); // Close the modal after saving
}

// Expose the function to the global scope so that the inline "onsubmit" call works.
window.saveAssignments = saveAssignments;

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("speaker-form")
        .addEventListener("submit", saveAssignments);

    // Initially populate the filter buttons based on current talk items
    updateFilterButtons();
    
    // Load and apply saved speaker mappings
    loadSavedSpeakerMappings();
});

// New function: updateFilterButtons()
// This function gathers all unique speakers from the talk items and
// dynamically creates filter buttons in the container.
function updateFilterButtons() {
    const container = document.getElementById('filterOptions');
    if (!container) return;
    
    // Get all unique speakers from the talk items
    const items = document.querySelectorAll('.talk-item');
    const speakersSet = new Set();
    items.forEach(item => {
        speakersSet.add(item.getAttribute('data-speaker'));
    });
    const speakers = Array.from(speakersSet).sort();
    
    // Clear the container before adding new buttons
    container.innerHTML = '';
    speakers.forEach(speaker => {
        const button = document.createElement('button');
        button.textContent = speaker;
        // Set up the onclick handler to filter by speaker.
        button.onclick = function() { filterBySpeaker(speaker); };
        container.appendChild(button);
    });
}

// Flag to track if speaker mappings have been loaded
let speakerMappingsLoaded = false;

// Function to load and apply saved speaker mappings from localStorage
function loadSavedSpeakerMappings() {
    console.log("Attempting to load saved speaker mappings...");
    try {
        // Get the current video ID
        let videoId;
        if (player && player.getVideoData) {
            videoId = player.getVideoData().video_id;
            console.log(`Retrieved video ID from player: ${videoId}`);
        } else {
            console.log("Player or getVideoData not available, trying fallback method");
        }
        
        if (!videoId) {
            const iframeSrc = document.querySelector('#video-section iframe')?.src;
            if (iframeSrc) {
                const videoIdMatch = iframeSrc.match(/embed\/([a-zA-Z0-9_-]+)/);
                videoId = videoIdMatch ? videoIdMatch[1] : null;
                console.log(`Retrieved video ID from iframe src: ${videoId}`);
            } else {
                console.log("Could not find iframe src");
            }
        }
        
        if (!videoId) {
            console.error("Could not determine video ID for loading speaker mappings");
            return;
        }
        
        // Use video-specific storage key
        const storageKey = `speakerMappings_${videoId}`;
        console.log(`Looking for speaker mappings with key: ${storageKey}`);
        const savedData = localStorage.getItem(storageKey);
        
        if (savedData) {
            const speakerMap = JSON.parse(savedData);
            console.log(`Loading saved speaker mappings for video ${videoId}:`, speakerMap);
            
            // Apply the mappings to all talk items
            Object.entries(speakerMap).forEach(([originalSpeaker, newSpeaker]) => {
                console.log(`Applying mapping: "${originalSpeaker}" -> "${newSpeaker}"`);
                const items = document.querySelectorAll(`.talk-item[data-speaker="${originalSpeaker}"]`);
                console.log(`Found ${items.length} items with speaker "${originalSpeaker}"`);
                
                items.forEach(item => {
                    // Update the data attribute
                    item.setAttribute('data-speaker', newSpeaker);
                    // Update the badge text
                    const badge = item.querySelector('.badge');
                    if (badge) {
                        badge.textContent = newSpeaker;
                    }
                });
            });
            
            // Update filter buttons to reflect the new speaker names
            updateFilterButtons();
            
            // Show notification if any mappings were applied and we haven't shown it before
            const mappingCount = Object.keys(speakerMap).length;
            if (mappingCount > 0 && !speakerMappingsLoaded) {
                showFocusNotification(`Applied ${mappingCount} saved speaker mapping${mappingCount > 1 ? 's' : ''}`);
                speakerMappingsLoaded = true;
            }
        } else {
            console.log(`No saved speaker mappings found for video ${videoId}`);
        }
    } catch (error) {
        console.error("Error loading speaker mappings from localStorage:", error);
        if (!speakerMappingsLoaded) {
            showFocusNotification('Failed to load speaker mappings');
        }
    }
}

// VIDEO PLAYER

var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";

var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

function onPlayerReady(event) {
    console.log("Player is ready!");
    // Start timestamp tracking when player is ready
    setupTimestampTracking();
    
    // Load saved timestamp
    loadSavedTimestamp();
    
    // Load saved speaker mappings
    loadSavedSpeakerMappings();
}

// Global variable to track the currently focused talk item
let currentFocusedItem = null;
let isVideoFocused = false;
let currentTimestampItem = null; // New variable to track the item at current timestamp

// Add a variable to store the last focused item before focusing on video
let lastFocusedItem = null;

// Function to highlight the item at current timestamp
function highlightCurrentTimestampItem(currentTime) {
    // Remove highlight from previous timestamp item
    if (currentTimestampItem) {
        currentTimestampItem.classList.remove('current-timestamp-item');
    }
    
    // Find the item closest to the current time
    const activeList = document.getElementById('transcript-list').classList.contains('hidden') 
        ? document.getElementById('claims-list') 
        : document.getElementById('transcript-list');
    
    const items = Array.from(activeList.querySelectorAll('.talk-item'));
    if (items.length === 0) return;
    
    // Find the item with the closest timestamp that's less than or equal to the current time
    let closestItem = null;
    let closestTime = -1;
    
    items.forEach(item => {
        const startTime = parseFloat(item.getAttribute('data-start-time'));
        if (startTime <= currentTime && startTime > closestTime) {
            closestTime = startTime;
            closestItem = item;
        }
    });
    
    // Highlight the found item
    if (closestItem) {
        closestItem.classList.add('current-timestamp-item');
        currentTimestampItem = closestItem;
    }
}

// Modify the getVideoTime function to also highlight the current timestamp item
function getVideoTime() {
    if (player && player.getCurrentTime) {
        var currentTime = player.getCurrentTime();
        scrollToTime(currentTime);
        
        // Find the item closest to the current time and focus it
        const activeList = document.getElementById('transcript-list').classList.contains('hidden') 
            ? document.getElementById('claims-list') 
            : document.getElementById('transcript-list');
        
        const items = Array.from(activeList.querySelectorAll('.talk-item'));
        if (items.length === 0) return;
        
        // Find the item with the closest timestamp that's less than or equal to the current time
        let closestItem = null;
        let closestTime = -1;
        
        items.forEach(item => {
            const startTime = parseFloat(item.getAttribute('data-start-time'));
            if (startTime <= currentTime && startTime > closestTime) {
                closestTime = startTime;
                closestItem = item;
            }
        });
        
        // Focus the found item
        if (closestItem) {
            focusItem(closestItem);
            showFocusNotification("Caught up to current time");
        }
    }
}

// Add a function to periodically check and update the current timestamp highlight
function setupTimestampTracking() {
    // Check every second for the current video position
    setInterval(() => {
        if (player && player.getCurrentTime && typeof player.getPlayerState === 'function') {
            // Check if player is playing (state 1)
            if (player.getPlayerState() === 1) {
                const currentTime = player.getCurrentTime();
                highlightCurrentTimestampItem(currentTime);
                
                // Save current timestamp to localStorage every 5 seconds
                if (Math.floor(currentTime) % 5 === 0) {
                    saveVideoTimestamp(currentTime);
                }
            }
        }
    }, 1000);
}

// Function to save video timestamp to localStorage
function saveVideoTimestamp(timestamp) {
    try {
        if (player && player.getVideoData) {
            const videoId = player.getVideoData().video_id;
            if (videoId) {
                localStorage.setItem(`videoTimestamp_${videoId}`, timestamp.toString());
                console.log(`Saved timestamp ${timestamp} for video ${videoId}`);
            }
        }
    } catch (error) {
        console.error("Error saving video timestamp to localStorage:", error);
    }
}

// Function to show a resume notification with buttons
function showResumeNotification(timestamp) {
    // Check if notification already exists and remove it
    let notification = document.getElementById('resume-notification');
    if (notification) {
        notification.remove();
    }
    
    // Create new notification
    notification = document.createElement('div');
    notification.id = 'resume-notification';
    notification.className = 'resume-notification';
    
    // Format the timestamp
    const formattedTime = formatTime(timestamp);
    
    // Create notification content
    notification.innerHTML = `
        <div class="resume-message">Resume from ${formattedTime}?</div>
        <div class="resume-buttons">
            <button id="resume-yes" class="resume-button">Yes</button>
            <button id="resume-no" class="resume-button">No</button>
        </div>
    `;
    
    // Add to body
    document.body.appendChild(notification);
    
    // Add event listeners to buttons
    document.getElementById('resume-yes').addEventListener('click', function() {
        player.seekTo(timestamp, true);
        showFocusNotification(`Resumed from ${formattedTime}`);
        notification.remove();
    });
    
    document.getElementById('resume-no').addEventListener('click', function() {
        notification.remove();
    });
    
    // Auto-remove after 10 seconds if no action
    setTimeout(() => {
        if (document.getElementById('resume-notification')) {
            notification.remove();
        }
    }, 10000);
}

// Function to load saved timestamp from localStorage
function loadSavedTimestamp() {
    try {
        if (player && player.getVideoData) {
            const videoId = player.getVideoData().video_id;
            if (videoId) {
                const savedTimestamp = localStorage.getItem(`videoTimestamp_${videoId}`);
                if (savedTimestamp) {
                    const timestamp = parseFloat(savedTimestamp);
                    console.log(`Loaded saved timestamp ${timestamp} for video ${videoId}`);
                    
                    // Show custom resume notification
                    showResumeNotification(timestamp);
                }
            }
        }
    } catch (error) {
        console.error("Error loading saved timestamp from localStorage:", error);
    }
}

// Helper function to format time as MM:SS
function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
}

// Add event listener for player state changes
function onPlayerStateChange(event) {
    console.log("Player state changed:", event.data);
    // When video is playing (state 1), start highlighting current timestamp
    if (event.data === 1) { // 1 is the code for YT.PlayerState.PLAYING
        const currentTime = player.getCurrentTime();
        highlightCurrentTimestampItem(currentTime);
    }
    
    // Save timestamp when video is paused (state 2)
    if (event.data === 2) { // 2 is the code for YT.PlayerState.PAUSED
        const currentTime = player.getCurrentTime();
        saveVideoTimestamp(currentTime);
    }
}

// Function to toggle the tools section in mobile view
function toggleTools() {
    const toolsButtons = document.querySelectorAll('#extra-tools');
    const toggleButtons = document.querySelectorAll('.tools-toggle');
    
    toolsButtons.forEach(toolsSection => {
        toolsSection.classList.toggle('expanded');
    });
    
    toggleButtons.forEach(button => {
        button.classList.toggle('collapsed');
        // Change the text based on state
        if (button.classList.contains('collapsed')) {
            button.innerHTML = 'Tools <i>▲</i>';
        } else {
            button.innerHTML = 'Tools <i>▼</i>';
        }
    });
    
    // Show notification about the tools state
    const isExpanded = toolsButtons[0]?.classList.contains('expanded');
    showFocusNotification(isExpanded ? "Tools expanded" : "Tools collapsed");
}

// Function to make talk-items clickable to jump to their timestamp
function makeItemsClickable() {
    const talkItems = document.querySelectorAll('.talk-item');
    talkItems.forEach(item => {
        item.addEventListener('click', function(event) {
            // Only trigger if the click is on the item itself or the talk-text, not on buttons or links
            if (event.target === item || 
                event.target.classList.contains('talk-text') || 
                event.target.classList.contains('talk-content') ||
                event.target.classList.contains('badge')) {
                const startTime = item.getAttribute('data-start-time');
                if (startTime) {
                    // Focus the item first
                    focusItem(item);
                    // Then jump to the timestamp
                    jumpToTime(parseFloat(startTime));
                    event.preventDefault();
                }
            }
        });
    });
}

// Add to the DOMContentLoaded event listener
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tools toggle buttons
    function initializeToolsToggle() {
        const toggleButtons = document.querySelectorAll('.tools-toggle');
        const toolsButtons = document.querySelectorAll('#extra-tools');
        const isMobile = window.innerWidth <= 768;
        
        // Make sure toggle buttons are visible on mobile
        toggleButtons.forEach(button => {
            if (isMobile) {
                button.style.display = 'flex';
                button.style.visibility = 'visible';
                button.style.opacity = '1';
                
                // Set initial state
                if (!button.classList.contains('collapsed')) {
                    button.classList.add('collapsed');
                    button.innerHTML = 'Tools <i>▲</i>';
                }
            } else {
                // On desktop, we don't need the toggle button
                button.style.display = 'none';
            }
        });
        
        // Set initial state of tools section
        toolsButtons.forEach(toolsSection => {
            if (isMobile) {
                toolsSection.classList.remove('expanded');
            } else {
                toolsSection.classList.add('expanded');
            }
        });
    }
    
    // Call initialization function
    initializeToolsToggle();
    
    // Also initialize on resize
    window.addEventListener('resize', initializeToolsToggle);
    
    // Initialize keyboard shortcuts help modal
    initKeyboardShortcutsHelp();
    
    // Setup timestamp tracking
    setupTimestampTracking();
    
    // Make talk-items clickable
    makeItemsClickable();
});

// ======================================================
// Keyboard Shortcuts
// ======================================================

// Enhanced keyboard shortcut handler
window.addEventListener('keydown', function(event) {
    // Skip if we're in an input field or textarea
    if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
        // Special case for Escape key in search bar
        if (event.key === 'Escape' && event.target.id === 'searchBar') {
            console.log('Escape key pressed in search bar - event handler triggered');
            // Remove these lines to prevent clearing the search bar
            // event.target.value = '';
             event.target.blur();
             filterTranscript();
            
            // You might still want to prevent default behavior
            event.preventDefault();
        }
        return;
    }
    
    // Skip if a modal is open (except for Escape key)
    const modalOpen = document.querySelector('.modal[style*="display: block"]');
    if (modalOpen && event.key !== 'Escape') return;
    
    // Handle Escape key for modals and unfocusing
    if (event.key === 'Escape') {
        // Close modals
        if (modalOpen) {
            closeModal();
            closeHelp();
        }
        
        // Close filter dropdown
        closeFilterDropdown();
        
        // Close options popups
        const popups = document.querySelectorAll('.options-popup');
        popups.forEach(popup => {
            popup.style.display = 'none';
        });
        
        // Unfocus any focused item
        if (currentFocusedItem) {
            currentFocusedItem.classList.remove('focused-item');
            currentFocusedItem = null;
            // Remove the event listener to prevent duplicates
            document.removeEventListener('keydown', handleFocusedItemKeydown);
            showFocusNotification("Navigation unfocused");
        }
        
        // Unfocus video if it's focused
        if (isVideoFocused) {
            const videoSection = document.getElementById('video-section');
            if (videoSection) {
                videoSection.classList.remove('video-focused');
            }
            isVideoFocused = false;
            showFocusNotification("Video controls inactive");
        }
        
        event.preventDefault();
        return;
    }
    
    // If video is focused, handle video-specific shortcuts
    if (isVideoFocused) {
        switch (event.key) {
            case ' ': // Space bar
                event.preventDefault();
                toggleVideoPlayback();
                break;
            case 'ArrowLeft':
                event.preventDefault();
                seekVideo(-5); // Rewind 5 seconds
                break;
            case 'ArrowRight':
                event.preventDefault();
                seekVideo(5); // Forward 5 seconds
                break;
            case 'ArrowUp':
                event.preventDefault();
                changeVolume(10); // Increase volume
                break;
            case 'ArrowDown':
                event.preventDefault();
                changeVolume(-10); // Decrease volume
                break;
            case 'm':
                event.preventDefault();
                toggleMute();
                break;
            case 'v':
                event.preventDefault();
                focusVideo(); // Toggle video focus
                break;
        }
        return;
    }
    
    // Handle global shortcuts when video is not focused
    switch (event.key) {
        case '/':
        case 'f':
            event.preventDefault();
            document.getElementById('searchBar').focus();
            break;
        case 'j':
        case 'ArrowDown': // Add ArrowDown for scrolling down
            event.preventDefault();
            focusNextItem();
            break;
        case 'k':
        case 'ArrowUp': // Add ArrowUp for scrolling up
            event.preventDefault();
            focusPreviousItem();
            break;
        case 'g':
            event.preventDefault();
            focusFirstItem();
            break;
        case 'G':
            if (event.shiftKey) {
                event.preventDefault();
                focusLastItem();
            }
            break;
        case 'v':
            event.preventDefault();
            focusVideo();
            break;
        case 't':
            event.preventDefault();
            toggleTranscript();
            break;
        case 'c':
            event.preventDefault();
            toggleClaims();
            break;
        case 'h':
            event.preventDefault();
            getVideoTime();
            break;
        case 'd':
            event.preventDefault();
            toggleDarkMode();
            break;
        case 'a':
            event.preventDefault();
            toggleAssignSpeakers();
            break;
        case '?':
            event.preventDefault();
            toggleHelp();
            break;
        case 'Enter':
            if (currentFocusedItem) {
                event.preventDefault();
                const startTime = parseFloat(currentFocusedItem.getAttribute('data-start-time'));
                jumpToTime(startTime);
            }
            break;
        case 'y':
            if (currentFocusedItem) {
                event.preventDefault();
                const textElement = currentFocusedItem.querySelector('.talk-text');
                if (textElement) {
                    const text = textElement.textContent;
                    navigator.clipboard.writeText(text)
                        .then(() => {
                            showFocusNotification('Text copied to clipboard');
                        })
                        .catch(err => {
                            console.error('Failed to copy text: ', err);
                            showFocusNotification('Failed to copy text');
                        });
                }
            }
            break;
        case 'l':
            if (!event.ctrlKey && !event.metaKey) {
                // Copy link to clipboard
                const startTimeForLink = currentFocusedItem.getAttribute('data-start-time');
                if (startTimeForLink) {
                    // Get the video ID directly from the player object
                    let videoId;
                    
                    try {
                        // First try to get it from the player object
                        if (player && player.getVideoData) {
                            videoId = player.getVideoData().video_id;
                        }
                        
                        // If that fails, try the old method as fallback
                        if (!videoId) {
                            const iframeSrc = document.querySelector('#video-section iframe').src;
                            const videoIdMatch = iframeSrc.match(/embed\/([a-zA-Z0-9_-]+)/);
                            videoId = videoIdMatch ? videoIdMatch[1] : null;
                        }
                        
                        if (videoId) {
                            const linkToCopy = `https://www.youtube.com/watch?v=${videoId}&t=${startTimeForLink}s`;
                            navigator.clipboard.writeText(linkToCopy)
                                .then(() => {
                                    // Format the timestamp for display (MM:SS)
                                    const minutes = Math.floor(startTimeForLink / 60);
                                    const remainingSeconds = Math.floor(startTimeForLink % 60);
                                    const formattedTime = `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
                                    showFocusNotification(`Link to ${formattedTime} copied`);
                                })
                                .catch(err => {
                                    showFocusNotification("Failed to copy link");
                                    console.error('Failed to copy: ', err);
                                });
                            event.preventDefault();
                        } else {
                            showFocusNotification("Failed to get video ID");
                            console.error('Failed to get video ID');
                        }
                    } catch (err) {
                        showFocusNotification("Failed to copy link");
                        console.error('Failed to copy link: ', err);
                    }
                }
            }
            break;
    }
});

// Function to focus on the video
function focusVideo() {
    const videoSection = document.getElementById('video-section');
    if (videoSection) {
        // Toggle focus state
        if (isVideoFocused) {
            // If already focused, unfocus it
            videoSection.classList.remove('video-focused');
            isVideoFocused = false;
            
            // Restore focus to the last focused item if available
            if (lastFocusedItem) {
                focusItem(lastFocusedItem);
                // Don't reset lastFocusedItem here so it persists
            }
        } else {
            // Store the currently focused item before focusing on video
            if (currentFocusedItem) {
                lastFocusedItem = currentFocusedItem;
            }
            
            // Focus on video
            videoSection.focus();
            videoSection.classList.add('video-focused');
            isVideoFocused = true;
            
            // Remove focus from any talk item
            if (currentFocusedItem) {
                currentFocusedItem.classList.remove('focused-item');
                currentFocusedItem = null;
            }
        }
        
        // Show a temporary notification about the focus state
        showFocusNotification(isVideoFocused ? "Video controls active" : "Video controls inactive");
    }
}

// Function to show a temporary notification
function showFocusNotification(message) {
    // Check if notification already exists and remove it
    let notification = document.getElementById('focus-notification');
    if (notification) {
        notification.remove();
    }
    
    // Create new notification
    notification = document.createElement('div');
    notification.id = 'focus-notification';
    notification.textContent = message;
    notification.className = 'focus-notification';
    
    // Add to body
    document.body.appendChild(notification);
    
    // Remove after 2 seconds
    setTimeout(() => {
        notification.classList.add('fade-out');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 500);
    }, 1500);
}

// Function to toggle video playback
function toggleVideoPlayback() {
    if (player && typeof player.getPlayerState === 'function') {
        const state = player.getPlayerState();
        if (state === 1) { // Playing
            player.pauseVideo();
            showFocusNotification("Paused");
        } else {
            player.playVideo();
            showFocusNotification("Playing");
        }
    }
}

// Function to seek video forward or backward
function seekVideo(seconds) {
    if (player && typeof player.getCurrentTime === 'function') {
        const currentTime = player.getCurrentTime();
        player.seekTo(currentTime + seconds, true);
        
        // Show notification with direction and amount
        const direction = seconds > 0 ? "forward" : "backward";
        const amount = Math.abs(seconds);
        showFocusNotification(`${direction} ${amount} seconds`);
    }
}

// Function to change video volume
function changeVolume(delta) {
    if (player && player.getVolume) {
        try {
            // Get current volume (0-100)
            const currentVolume = player.getVolume();
            // Calculate new volume
            let newVolume = currentVolume + delta;
            // Clamp between 0 and 100
            newVolume = Math.max(0, Math.min(100, newVolume));
            // Set new volume
            player.setVolume(newVolume);
            
            // Show notification
            showFocusNotification(`Volume: ${newVolume}%`);
        } catch (error) {
            console.error('Error changing volume:', error);
        }
    }
}

// Function to toggle mute
function toggleMute() {
    if (player) {
        if (player.isMuted()) {
            player.unMute();
            // Get current volume to display in notification
            const currentVolume = player.getVolume();
            showFocusNotification(`Unmuted (${Math.round(currentVolume)}%)`);
        } else {
            player.mute();
            showFocusNotification("Muted");
        }
    }
}

// Function to focus on the next talk item
function focusNextItem() {
    const visibleItems = getVisibleItems();
    if (visibleItems.length === 0) return;
    
    let nextIndex = 0;
    if (currentFocusedItem) {
        const currentIndex = visibleItems.indexOf(currentFocusedItem);
        nextIndex = (currentIndex + 1) % visibleItems.length;
    }
    
    focusItem(visibleItems[nextIndex]);
}

// Function to focus on the previous talk item
function focusPreviousItem() {
    const visibleItems = getVisibleItems();
    if (visibleItems.length === 0) return;
    
    let prevIndex = visibleItems.length - 1;
    if (currentFocusedItem) {
        const currentIndex = visibleItems.indexOf(currentFocusedItem);
        prevIndex = (currentIndex - 1 + visibleItems.length) % visibleItems.length;
    }
    
    focusItem(visibleItems[prevIndex]);
}

// Function to focus on the first talk item
function focusFirstItem() {
    const visibleItems = getVisibleItems();
    if (visibleItems.length > 0) {
        focusItem(visibleItems[0]);
    }
}

// Function to focus on the last talk item
function focusLastItem() {
    const visibleItems = getVisibleItems();
    if (visibleItems.length > 0) {
        focusItem(visibleItems[visibleItems.length - 1]);
    }
}

// Helper function to get all visible talk items
function getVisibleItems() {
    const activeList = document.getElementById('transcript-list').classList.contains('hidden') 
        ? document.getElementById('claims-list') 
        : document.getElementById('transcript-list');
    
    return Array.from(activeList.querySelectorAll('.talk-item'))
        .filter(item => item.style.display !== 'none');
}

// Helper function to focus on a specific talk item
function focusItem(item) {
    if (!item) return;
    
    // Remove focus from video
    isVideoFocused = false;
    const videoSection = document.getElementById('video-section');
    if (videoSection) {
        videoSection.classList.remove('video-focused');
    }
    
    // Remove focus from previous item
    if (currentFocusedItem) {
        currentFocusedItem.classList.remove('focused-item');
    }
    
    // Focus on new item
    currentFocusedItem = item;
    currentFocusedItem.classList.add('focused-item');
    currentFocusedItem.scrollIntoView({ behavior: 'smooth', block: 'center' });
    
    // Remove any existing event listener to prevent duplicates
    document.removeEventListener('keydown', handleFocusedItemKeydown);
    
    // Add keyboard event listeners for actions on the focused item
    document.addEventListener('keydown', handleFocusedItemKeydown);
}

// Function to handle keydown events when an item is focused
function handleFocusedItemKeydown(event) {
    if (!currentFocusedItem) return;
    
    switch (event.key) {
        case 'Escape':
            // Unfocus the current item
            currentFocusedItem.classList.remove('focused-item');
            currentFocusedItem = null;
            document.removeEventListener('keydown', handleFocusedItemKeydown);
            showFocusNotification("Navigation unfocused");
            event.preventDefault();
            event.stopPropagation(); // Prevent other handlers from processing this event
            break;
        case 'Enter':
            // Jump to the timestamp in the video
            const startTime = currentFocusedItem.getAttribute('data-start-time');
            if (startTime) {
                jumpToTime(parseFloat(startTime));
                event.preventDefault();
            }
            break;
        case 'y':
            if (!event.ctrlKey && !event.metaKey) {
                // Copy text to clipboard
                const textElement = currentFocusedItem.querySelector('.talk-text');
                if (textElement) {
                    navigator.clipboard.writeText(textElement.textContent);
                    event.preventDefault();
                }
            }
            break;
        case 'l':
            if (!event.ctrlKey && !event.metaKey) {
                // Copy link to clipboard
                const startTimeForLink = currentFocusedItem.getAttribute('data-start-time');
                if (startTimeForLink) {
                    // Get the video ID directly from the player object
                    let videoId;
                    
                    try {
                        // First try to get it from the player object
                        if (player && player.getVideoData) {
                            videoId = player.getVideoData().video_id;
                        }
                        
                        // If that fails, try the old method as fallback
                        if (!videoId) {
                            const iframeSrc = document.querySelector('#video-section iframe').src;
                            const videoIdMatch = iframeSrc.match(/embed\/([a-zA-Z0-9_-]+)/);
                            videoId = videoIdMatch ? videoIdMatch[1] : null;
                        }
                        
                        if (videoId) {
                            const linkToCopy = `https://www.youtube.com/watch?v=${videoId}&t=${startTimeForLink}s`;
                            navigator.clipboard.writeText(linkToCopy)
                                .then(() => {
                                    // Format the timestamp for display (MM:SS)
                                    const minutes = Math.floor(startTimeForLink / 60);
                                    const remainingSeconds = Math.floor(startTimeForLink % 60);
                                    const formattedTime = `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
                                    showFocusNotification(`Link to ${formattedTime} copied`);
                                })
                                .catch(err => {
                                    showFocusNotification("Failed to copy link");
                                    console.error('Failed to copy: ', err);
                                });
                            event.preventDefault();
                        } else {
                            showFocusNotification("Failed to get video ID");
                            console.error('Failed to get video ID');
                        }
                    } catch (err) {
                        showFocusNotification("Failed to copy link");
                        console.error('Failed to copy link: ', err);
                    }
                }
            }
            break;
    }
}

// Function to initialize keyboard shortcuts help modal
function initKeyboardShortcutsHelp() {
    // Create modal if it doesn't exist
    if (!document.getElementById('keyboardShortcutsModal')) {
        const modal = document.createElement('div');
        modal.id = 'keyboardShortcutsModal';
        modal.className = 'modal';
        modal.style.display = 'none';
        
        modal.innerHTML = `
            <div class="modal-content">
                <span class="close" onclick="toggleKeyboardShortcutsHelp()">&times;</span>
                <div class="modal-header">
                    <h2>Keyboard Shortcuts</h2>
                </div>
                <div class="keyboard-shortcuts-container">
                    <div class="shortcuts-column">
                        <h3>Navigation</h3>
                        <div class="shortcut-item">
                            <span class="key">j</span>
                            <span class="description">Next item</span>
                        </div>
                        <div class="shortcut-item">
                            <span class="key">k</span>
                            <span class="description">Previous item</span>
                        </div>
                        <div class="shortcut-item">
                            <span class="key">g</span>
                            <span class="description">Go to first item</span>
                        </div>
                        <div class="shortcut-item">
                            <span class="key">G</span>
                            <span class="description">Go to last item</span>
                        </div>
                        <div class="shortcut-item">
                            <span class="key">h</span>
                            <span class="description">Catchup to video</span>
                        </div>
                        
                        <h3>Tabs & Tools</h3>
                        <div class="shortcut-item">
                            <span class="key">t</span>
                            <span class="description">Switch to Transcript</span>
                        </div>
                        <div class="shortcut-item">
                            <span class="key">c</span>
                            <span class="description">Switch to Claims</span>
                        </div>
                        <div class="shortcut-item">
                            <span class="key">a</span>
                            <span class="description">Assign speakers</span>
                        </div>
                    </div>
                    
                    <div class="shortcuts-column">
                        <h3>Search</h3>
                        <div class="shortcut-item">
                            <span class="key">/</span> or <span class="key">f</span>
                            <span class="description">Focus search bar</span>
                        </div>
                        
                        <h3>Video Controls</h3>
                        <div class="shortcut-item">
                            <span class="key">v</span>
                            <span class="description">Toggle video focus on/off</span>
                        </div>
                        <div class="shortcut-item">
                            <span class="key">Space</span>
                            <span class="description">Play/Pause video</span>
                        </div>
                        <div class="shortcut-item">
                            <span class="key">←</span>
                            <span class="description">Rewind 5 seconds</span>
                        </div>
                        <div class="shortcut-item">
                            <span class="key">→</span>
                            <span class="description">Forward 5 seconds</span>
                        </div>
                        <div class="shortcut-item">
                            <span class="key">↑</span>
                            <span class="description">Increase volume</span>
                        </div>
                        <div class="shortcut-item">
                            <span class="key">↓</span>
                            <span class="description">Decrease volume</span>
                        </div>
                        <div class="shortcut-item">
                            <span class="key">m</span>
                            <span class="description">Mute/Unmute</span>
                        </div>
                        
                        <h3>Focused Item Actions</h3>
                        <div class="shortcut-item">
                            <span class="key">Enter</span>
                            <span class="description">Jump to timestamp</span>
                        </div>
                        <div class="shortcut-item">
                            <span class="key">y</span>
                            <span class="description">Copy text</span>
                        </div>
                        <div class="shortcut-item">
                            <span class="key">l</span>
                            <span class="description">Copy link</span>
                        </div>
                        
                        <h3>Other</h3>
                        <div class="shortcut-item">
                            <span class="key">d</span>
                            <span class="description">Toggle dark mode</span>
                        </div>
                        <div class="shortcut-item">
                            <span class="key">?</span>
                            <span class="description">Show this help</span>
                        </div>
                        <div class="shortcut-item">
                            <span class="key">Esc</span>
                            <span class="description">Close popups/modals</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
    }
}

// Function to toggle keyboard shortcuts help modal
function toggleKeyboardShortcutsHelp() {
    const modal = document.getElementById('keyboardShortcutsModal');
    if (!modal) {
        initKeyboardShortcutsHelp();
        toggleKeyboardShortcutsHelp();
        return;
    }
    
    if (modal.style.display === 'block') {
        modal.style.display = 'none';
        document.body.classList.remove('modal-open');
    } else {
        modal.style.display = 'block';
        document.body.classList.add('modal-open');
    }
}

// Initialize keyboard shortcuts help on page load
document.addEventListener('DOMContentLoaded', function() {
    // Initialize existing code
    // ... existing code ...
    
    // Initialize keyboard shortcuts help
    initKeyboardShortcutsHelp();
});

// Make functions available globally
window.toggleKeyboardShortcutsHelp = toggleKeyboardShortcutsHelp;

// Function to export speaker mappings as a JSON file
function exportSpeakerMap() {
    try {
        // Get the current video ID
        let videoId;
        if (player && player.getVideoData) {
            videoId = player.getVideoData().video_id;
        }
        
        if (!videoId) {
            const iframeSrc = document.querySelector('#video-section iframe').src;
            const videoIdMatch = iframeSrc.match(/embed\/([a-zA-Z0-9_-]+)/);
            videoId = videoIdMatch ? videoIdMatch[1] : null;
        }
        
        if (!videoId) {
            console.error("Could not determine video ID for exporting speaker mappings");
            showFocusNotification('Failed to export: Could not determine video ID');
            return;
        }
        
        // Use video-specific storage key
        const storageKey = `speakerMappings_${videoId}`;
        const savedData = localStorage.getItem(storageKey);
        let speakerMap = {};
        
        if (savedData) {
            speakerMap = JSON.parse(savedData);
        } else {
            // If no saved mappings, create a map from current assignments
            const items = Array.from(document.querySelectorAll('.talk-item'));
            const uniqueSpeakers = new Set();
            
            // Get all unique speakers
            items.forEach(item => {
                uniqueSpeakers.add(item.getAttribute('data-speaker'));
            });
            
            // Get values from the form if it's open
            const inputs = document.querySelectorAll('#speaker-inputs input');
            if (inputs.length > 0) {
                inputs.forEach(input => {
                    const label = input.parentElement.querySelector('label.speaker-label');
                    if (label && input.value.trim()) {
                        const originalSpeaker = label.textContent.trim();
                        const newSpeaker = input.value.trim();
                        if (newSpeaker && newSpeaker !== originalSpeaker) {
                            speakerMap[originalSpeaker] = newSpeaker;
                        }
                    }
                });
            }
        }
        
        // Create a JSON string with proper formatting
        const jsonString = JSON.stringify(speakerMap, null, 4);
        
        // Create a blob with the JSON data
        const blob = new Blob([jsonString], { type: 'application/json' });
        
        // Create a download link
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = `speaker_map_${videoId}.json`; // Include video ID in filename
        
        // Trigger the download
        document.body.appendChild(a);
        a.click();
        
        // Clean up
        document.body.removeChild(a);
        URL.revokeObjectURL(a.href);
        
        // Show notification
        showFocusNotification('Speaker mappings exported as speakers.json');
        
    } catch (error) {
        console.error('Error exporting speaker mappings:', error);
        showFocusNotification('Failed to export speaker mappings');
    }
}

// Check for saved dark mode preference on page load
document.addEventListener('DOMContentLoaded', function() {
    // Apply dark mode if saved
    const darkMode = localStorage.getItem('darkMode');
    if (darkMode === 'enabled') {
        document.body.classList.add('dark-mode');
        
        // Update dark mode button icons
        const darkModeButton = document.getElementById('dark-mode-toggle');
        if (darkModeButton) {
            const icon = darkModeButton.querySelector('i');
            icon.className = 'fas fa-sun';
        }
        
        const mobileDarkModeButton = document.querySelector('.dark-mode-button-mobile button');
        if (mobileDarkModeButton) {
            const icon = mobileDarkModeButton.querySelector('i');
            icon.className = 'fas fa-sun';
        }
    } else if (darkMode === 'disabled') {
        document.body.classList.remove('dark-mode');
    }
});

// Add event listener to save timestamp when user leaves the page
window.addEventListener('beforeunload', function() {
    if (player && player.getCurrentTime) {
        const currentTime = player.getCurrentTime();
        saveVideoTimestamp(currentTime);
    }
});