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
    } else {
        transcriptTab.classList.toggle('active');
        transcriptTab.classList.remove('inactive'); // Remove inactive class
        claimsTab.classList.remove('active');
        claimsTab.classList.add('inactive'); // Add inactive class
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
    } else {
        transcriptTab.classList.toggle('active');
        transcriptTab.classList.remove('inactive'); // Remove inactive class
        claimsTab.classList.remove('active');
        claimsTab.classList.add('inactive'); // Add inactive class
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
    }

    const popup = event.target.closest('.options-popup');
    if (popup) {
        popup.style.display = 'none'; // Hide the popup
    }
}

function copyLinkToClipboard(event, timestamp) {  // Accept timestamp as a parameter
    const transcriptItem = event.target.closest('.talk-item'); // Get the closest transcript item
    if (transcriptItem) {
        const iframeSrc = document.querySelector('#video-section iframe').src; // Get the iframe src
        const videoIdMatch = iframeSrc.match(/embed\/([a-zA-Z0-9_-]+)/); // Extract video ID using regex
        const videoId = videoIdMatch ? videoIdMatch[1] : null; // Get the video ID or null if not found

        if (videoId) {
            const linkToCopy = `https://www.youtube.com/watch?v=${videoId}&t=${timestamp}s`; // Generate the link with timestamp
            navigator.clipboard.writeText(linkToCopy) // Copy to clipboard
                .then(() => {
                    console.log('Link copied to clipboard!');
                })
                .catch(err => {
                    console.error('Failed to copy: ', err); // Error handling
                });
        } else {
            console.error('Video ID not found in iframe source.'); // Error handling for missing video ID
        }
    }
    
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
        if (darkModeButton.textContent === '🌞') {
            darkModeButton.textContent = '🌙';
        } else {
            darkModeButton.textContent = '🌞';
        }
    }
    
    // Update mobile dark mode button
    const mobileDarkModeButton = document.querySelector('.dark-mode-button-mobile button');
    if (mobileDarkModeButton) {
        if (mobileDarkModeButton.textContent === '🌞') {
            mobileDarkModeButton.textContent = '🌙';
        } else {
            mobileDarkModeButton.textContent = '🌞';
        }
    }
}

function toggleFilterDropdown() {
    // Determine which section is currently visible
    const transcriptList = document.getElementById('transcript-list');
    const claimsList = document.getElementById('claims-list');
    
    // Get the filterOptions based on the visible section
    const filterOptions = transcriptList.classList.contains('hidden') 
        ? claimsList.querySelector('#filterOptions') 
        : transcriptList.querySelector('#filterOptions');

    if (filterOptions) {
        const isShowing = filterOptions.style.display === 'block';
        
        // Toggle display
        filterOptions.style.display = isShowing ? 'none' : 'block';
    } else {
        console.error("Element with ID 'filterOptions' not found.");
    }
}

function closeFilterDropdown() {
    const filterOptions = document.querySelectorAll('#filterOptions');
    filterOptions.forEach(option => {
        option.style.display = 'none';
    });
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

    items.forEach(item => {
        item.style.display = selectedSpeakers.size === 0 || selectedSpeakers.has(item.getAttribute('data-speaker')) ? '' : 'none';
    });

    // Update the filter display
    updateFilterDisplay();
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

    if (event.key === 'Escape') {
        // Close filter dropdown
        closeFilterDropdown();

        // Close modals
        const modal = document.getElementById('assignSpeakersModal');
        if (modal) {
            modal.style.display = 'none';
            document.body.classList.remove('modal-open'); // Re-enable body scrolling
        }

        const helpModal = document.getElementById('helpModal');
        if (helpModal) {
            helpModal.style.display = 'none';
            document.body.classList.remove('modal-open'); // Re-enable body scrolling
        }
        
        // Close options popups
        const popups = document.querySelectorAll('.options-popup');
        popups.forEach(popup => {
            popup.style.display = 'none';
        });
    }
});

window.onclick = function(event) {
    // Close filter dropdown when clicking outside
    if (!event.target.matches('.filter-dropdown button') && 
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

    // Create input fields for each unique speaker
    uniqueSpeakers.forEach(speaker => {
        const div = document.createElement('div');
        div.innerHTML = `<div class="speaker-input-container"><label class="speaker-label">${speaker}</label><input class="speaker-input" type="text" placeholder=""></div>`;
        speakerInputs.appendChild(div);
    });

    modal.style.display = 'block'; // Show the modal
    document.body.classList.add('modal-open'); // Prevent body scrolling
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

    // For each input field, use its container to safely locate the associated label.
    inputs.forEach(input => {
        const label = input.parentElement.querySelector('label.speaker-label');
        if (label) {
            const originalSpeaker = label.textContent.trim();
            // If the input is empty, keep the original speaker name
            const newSpeaker = input.value.trim() || originalSpeaker;
            assignments[originalSpeaker] = newSpeaker;
        }
    });

    console.log("Speaker assignments:", assignments); // Log the assignments for verification

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

    closeModal(); // Close the modal after saving
}

// Expose the function to the global scope so that the inline "onsubmit" call works.
window.saveAssignments = saveAssignments;

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("speaker-form")
        .addEventListener("submit", saveAssignments);

    // Initially populate the filter buttons based on current talk items
    updateFilterButtons();
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
// VIDEO PLAYER

var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";

var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

function onPlayerReady(event) {
    console.log("Player is ready!");
}

function getVideoTime() {
    if (player && player.getCurrentTime) {
        var currentTime = player.getCurrentTime();
        scrollToTime(currentTime);
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
}

// Initialize tools state on page load
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on mobile
    if (window.innerWidth <= 768) {
        // Keep tools collapsed by default on mobile
        const toolsButtons = document.querySelectorAll('#extra-tools');
        toolsButtons.forEach(toolsSection => {
            toolsSection.classList.remove('expanded');
        });
    } else {
        // On desktop, keep tools expanded
        const toolsButtons = document.querySelectorAll('#extra-tools');
        toolsButtons.forEach(toolsSection => {
            toolsSection.classList.add('expanded');
        });
    }
    
    // Handle window resize
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            // On desktop, always keep tools expanded
            const toolsButtons = document.querySelectorAll('#extra-tools');
            toolsButtons.forEach(toolsSection => {
                toolsSection.classList.add('expanded');
            });
        }
    });
});