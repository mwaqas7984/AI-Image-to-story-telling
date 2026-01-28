/**
 * Frontend JavaScript for AI Image Storyteller
 * Handles image upload, API communication, and result rendering
 */

class ImageStoryteller {
    constructor() {
        this.initializeElements();
        this.bindEvents();
    }

    initializeElements() {
        // Input elements
        this.imageInput = document.getElementById('image-input');
        this.imagePreview = document.getElementById('image-preview');
        this.analyzeButton = document.getElementById('analyze-button');
        this.fileInputLabel = document.querySelector('.file-input-label');
        
        // Results container
        this.resultsContainer = document.getElementById('results');
        
        // API endpoint
        this.apiEndpoint = 'http://127.0.0.1:8000/api/image-analyze';
    }

    bindEvents() {
        // File input change event
        this.imageInput.addEventListener('change', (e) => this.handleFileSelect(e));
        
        // Analyze button click event
        this.analyzeButton.addEventListener('click', () => this.analyzeImage());
        
        // Drag and drop events
        const fileInputWrapper = document.querySelector('.file-input-wrapper');
        
        fileInputWrapper.addEventListener('dragover', (e) => {
            e.preventDefault();
            fileInputWrapper.classList.add('drag-over');
        });
        
        fileInputWrapper.addEventListener('dragleave', (e) => {
            e.preventDefault();
            fileInputWrapper.classList.remove('drag-over');
        });
        
        fileInputWrapper.addEventListener('drop', (e) => {
            e.preventDefault();
            fileInputWrapper.classList.remove('drag-over');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleFileSelect({ target: { files: files } });
            }
        });
        
        // Navigation toggle
        const navToggle = document.querySelector('.nav-toggle');
        const navMenu = document.querySelector('.nav-menu');
        
        if (navToggle && navMenu) {
            navToggle.addEventListener('click', () => {
                navMenu.classList.toggle('active');
                navToggle.classList.toggle('active');
            });
        }
    }

    handleFileSelect(event) {
        const file = event.target.files[0];
        if (file) {
            this.handleFile(file);
        }
    }

    handleFile(file) {
        // Validate file type
        if (!file.type.startsWith('image/')) {
            this.showError('Please select an image file (JPEG, PNG, GIF, etc.)');
            return;
        }

        // Validate file size (10MB limit)
        if (file.size > 10 * 1024 * 1024) {
            this.showError('File size must be less than 10MB');
            return;
        }

        // Show preview
        this.showImagePreview(file);
        
        // Enable analyze button
        this.analyzeButton.disabled = false;
        
        // Clear previous results
        this.resultsContainer.innerHTML = '';
    }

    showImagePreview(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            this.imagePreview.src = e.target.result;
            this.imagePreview.style.display = 'block';
            this.fileInputLabel.textContent = `Selected: ${file.name}`;
        };
        reader.readAsDataURL(file);
    }

    async analyzeImage() {
        const file = this.imageInput.files[0];
        if (!file) {
            this.showError('Please select an image first');
            return;
        }

        // Show loading state
        this.showLoading();
        
        try {
            // Create FormData for file upload
            const formData = new FormData();
            formData.append('file', file);
            
            console.log('Sending file to backend:', file.name, 'size:', file.size);
            
            // Send request to backend
            const response = await fetch(this.apiEndpoint, {
                method: 'POST',
                body: formData
            });

            console.log('Response status:', response.status);
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error('Error response:', errorText);
                throw new Error(`HTTP ${response.status}: ${errorText}`);
            }

            const result = await response.json();
            console.log('Full analysis result:', result);
            console.log('Result keys:', Object.keys(result));
            console.log('Story field:', result.story);
            this.displayResults(result);

        } catch (error) {
            console.error('Analysis error:', error);
            this.showError(error.message || 'Failed to analyze image. Please try again.');
        }
    }

    getBase64Image(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.onerror = reject;
            reader.readAsDataURL(file);
        });
    }

    showLoading() {
        const loadingSection = document.getElementById('loading-section');
        const resultsSection = document.getElementById('results');
        
        if (loadingSection) loadingSection.style.display = 'block';
        if (resultsSection) resultsSection.style.display = 'none';
    }

    showError(message) {
        // Hide loading and show error
        const loadingSection = document.getElementById('loading-section');
        const resultsSection = document.getElementById('results');
        
        if (loadingSection) loadingSection.style.display = 'none';
        if (resultsSection) {
            resultsSection.style.display = 'block';
            resultsSection.innerHTML = `
                <div class="results-header">
                    <h2><i class="fas fa-exclamation-triangle"></i> Error</h2>
                </div>
                <div class="results-grid">
                    <div class="result-card">
                        <h3><i class="fas fa-exclamation-circle"></i> Error</h3>
                        <div class="result-content">
                            <p>${message}</p>
                            <button class="btn btn-secondary" onclick="createNewStory()">
                                <i class="fas fa-redo"></i>
                                Try Again
                            </button>
                        </div>
                    </div>
                </div>
            `;
        }
    }

    displayResults(result) {
        console.log('=== DISPLAY RESULTS CALLED ===');
        console.log('Full result object:', result);
        
        // Store the result for potential retry
        this.lastResult = result;
        
        // Hide loading and show results
        const loadingSection = document.getElementById('loading-section');
        const resultsSection = document.getElementById('results');
        
        console.log('Results section before:', resultsSection);
        console.log('Results section children before:', resultsSection ? resultsSection.children.length : 'no section');
        
        if (loadingSection) loadingSection.style.display = 'none';
        if (resultsSection) {
            resultsSection.style.display = 'block';
            console.log('Results section after show:', resultsSection);
            console.log('Results section children after show:', resultsSection.children.length);
            
            // Log all children
            if (resultsSection.children.length > 0) {
                console.log('Children details:');
                Array.from(resultsSection.children).forEach((child, index) => {
                    console.log(`Child ${index}:`, child.tagName, child.id, child.className);
                });
            }
        }
        
        // Check if results section has been corrupted
        if (!resultsSection || resultsSection.children.length === 0) {
            console.log('❌ Results section is empty or missing! Rebuilding...');
            this.rebuildResultsSection();
            return;
        }
        
        // Now populate the data
        this.populateResults(result);
    }
    
    populateResults(result) {
        const resultsSection = document.getElementById('results');
        
        // Display original image
        const resultImage = document.getElementById('result-image');
        if (resultImage && this.imagePreview.src) {
            resultImage.src = this.imagePreview.src;
            console.log('✅ Image displayed');
        }
        
        // Display caption
        const captionResult = document.getElementById('caption-result');
        if (captionResult) {
            captionResult.innerHTML = `<p>${result.caption || 'No caption available'}</p>`;
            console.log('✅ Caption displayed:', result.caption);
        } else {
            console.log('❌ Caption result element not found');
        }
        
        // Display objects
        const objectsResult = document.getElementById('objects-result');
        if (objectsResult) {
            if (result.objects && result.objects.length > 0) {
                const objectsList = result.objects.map(obj => `<span class="object-tag">${obj}</span>`).join('');
                objectsResult.innerHTML = `<div class="objects-container">${objectsList}</div>`;
                console.log('✅ Objects displayed:', result.objects);
            } else {
                objectsResult.innerHTML = '<p>No objects detected</p>';
                console.log('❌ No objects detected');
            }
        } else {
            console.log('❌ Objects result element not found');
        }
        
        // Display emotion
        const emotionResult = document.getElementById('emotion-result');
        if (emotionResult) {
            emotionResult.innerHTML = `
                <div class="emotion-display">
                    <span class="emotion-icon">${this.getEmotionIcon(result.emotion)}</span>
                    <span>${result.emotion || 'neutral'}</span>
                </div>
            `;
            console.log('✅ Emotion displayed:', result.emotion);
        } else {
            console.log('❌ Emotion result element not found');
        }
        
        // Display story - THIS IS THE KEY PART
        const storyResult = document.getElementById('story-result');
        console.log('=== STORY DEBUG ===');
        console.log('Looking for element with ID: story-result');
        console.log('Story element found:', !!storyResult);
        
        if (storyResult) {
            console.log('Story element tag:', storyResult.tagName);
            console.log('Story element parent:', storyResult.parentElement);
            console.log('Story element visible:', storyResult.style.display !== 'none');
            console.log('Story element parent visible:', storyResult.parentElement ? storyResult.parentElement.style.display !== 'none' : 'no parent');
            console.log('Results section visible:', resultsSection ? resultsSection.style.display !== 'none' : 'no results section');
            
            console.log('Story data:', result.story);
            console.log('Story type:', typeof result.story);
            console.log('Story length:', result.story ? result.story.length : 'undefined');
            
            if (result.story) {
                let storyText = '';
                if (Array.isArray(result.story)) {
                    storyText = result.story.join(' ');
                    console.log('✅ Story joined from array, length:', storyText.length);
                    console.log('Story preview:', storyText.substring(0, 100) + '...');
                } else if (typeof result.story === 'string') {
                    storyText = result.story;
                    console.log('✅ Story as string, length:', storyText.length);
                    console.log('Story preview:', storyText.substring(0, 100) + '...');
                } else {
                    storyText = JSON.stringify(result.story);
                    console.log('✅ Story converted to string:', storyText);
                }
                
                if (storyText.trim().length > 0) {
                    storyResult.innerHTML = `<p class="story-text">${storyText}</p>`;
                    console.log('✅ Story HTML set successfully');
                    console.log('Story element innerHTML length:', storyResult.innerHTML.length);
                    console.log('Story element innerHTML:', storyResult.innerHTML);
                    
                    // Force visibility check
                    setTimeout(() => {
                        console.log('Story element after timeout - visible:', storyResult.style.display !== 'none');
                        console.log('Story element computed style:', window.getComputedStyle(storyResult).display);
                    }, 100);
                } else {
                    storyResult.innerHTML = '<p>No story generated (empty)</p>';
                    console.log('❌ Story is empty');
                }
            } else {
                storyResult.innerHTML = '<p>No story generated (undefined)</p>';
                console.log('❌ Story is undefined');
            }
        } else {
            console.log('❌ Story element not found!');
            // Check if there are any elements with similar IDs
            const allElements = document.querySelectorAll('[id*="story"]');
            console.log('Elements with "story" in ID:', Array.from(allElements).map(el => el.id));
            
            // Check if results section exists
            if (resultsSection) {
                console.log('Results section exists, checking children...');
                const resultElements = resultsSection.querySelectorAll('[id]');
                console.log('All elements in results section:', Array.from(resultElements).map(el => el.id));
            }
        }
        
        // Scroll to results
        if (resultsSection) {
            resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
        
        this.showToast('Story generated successfully!', 'success');
        console.log('=== DISPLAY RESULTS COMPLETED ===');
    }
    
    rebuildResultsSection() {
        console.log('🔧 Rebuilding results section...');
        const resultsSection = document.getElementById('results');
        
        if (resultsSection) {
            resultsSection.innerHTML = `
                <div class="results-header">
                    <h2><i class="fas fa-sparkles"></i> Your AI-Generated Story</h2>
                </div>

                <div class="results-grid">
                    <!-- Original Image -->
                    <div class="result-card">
                        <h3><i class="fas fa-image"></i> Original Image</h3>
                        <div class="result-image">
                            <img id="result-image" src="" alt="Original">
                        </div>
                    </div>

                    <!-- Analysis Results -->
                    <div class="result-card">
                        <h3><i class="fas fa-closed-captioning"></i> Caption</h3>
                        <div class="result-content" id="caption-result">
                            <p>Loading...</p>
                        </div>
                    </div>

                    <div class="result-card">
                        <h3><i class="fas fa-cube"></i> Detected Objects</h3>
                        <div class="result-content" id="objects-result">
                            <p>Loading...</p>
                        </div>
                    </div>

                    <div class="result-card">
                        <h3><i class="fas fa-heart"></i> Emotion</h3>
                        <div class="result-content" id="emotion-result">
                            <p>Loading...</p>
                        </div>
                    </div>

                    <div class="result-card story-card">
                        <h3><i class="fas fa-book-open"></i> Generated Story</h3>
                        <div class="result-content" id="story-result">
                            <p>Loading...</p>
                        </div>
                    </div>
                </div>

                <!-- Actions -->
                <div class="result-actions">
                    <button class="action-button" onclick="copyStory()">
                        <i class="fas fa-copy"></i>
                        Copy Story
                    </button>
                    <button class="action-button" onclick="downloadStory()">
                        <i class="fas fa-download"></i>
                        Download Story
                    </button>
                    <button class="action-button" onclick="createNewStory()">
                        <i class="fas fa-plus"></i>
                        Create New Story
                    </button>
                </div>
            `;
            
            console.log('✅ Results section rebuilt');
            console.log('New children count:', resultsSection.children.length);
            
            // Try to display results again with the stored data
            setTimeout(() => {
                console.log('🔄 Retrying display results...');
                if (this.lastResult) {
                    this.populateResults(this.lastResult);
                } else {
                    console.log('❌ No stored result to retry with');
                }
            }, 100);
        }
    }
    
    getEmotionIcon(emotion) {
        const emotionIcons = {
            'happy': '😊',
            'sad': '😢',
            'angry': '😠',
            'surprised': '😮',
            'fear': '😨',
            'disgust': '🤢',
            'neutral': '😐',
            'working': '💼',
            'focused': '🎯',
            'relaxed': '😌',
            'excited': '🎉',
            'peaceful': '🕊️'
        };
        
        return emotionIcons[emotion?.toLowerCase()] || '😐';
    }
    
    showToast(message, type = 'success') {
        // Create toast element if it doesn't exist
        let toast = document.getElementById('toast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'toast';
            toast.className = 'toast';
            document.body.appendChild(toast);
        }
        
        const toastMessage = document.getElementById('toast-message');
        if (!toastMessage) {
            const messageEl = document.createElement('span');
            messageEl.id = 'toast-message';
            toast.appendChild(messageEl);
        }
        
        // Set message and type
        document.getElementById('toast-message').textContent = message;
        toast.className = `toast ${type}`;
        
        // Show toast
        setTimeout(() => toast.classList.add('show'), 100);
        
        // Hide after 3 seconds
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }

    renderCaption(caption) {
        return `
            <div class="card caption-card">
                <h2 class="card-title">Caption</h2>
                <p style="font-size: 1.1rem; line-height: 1.6;">${this.escapeHtml(caption)}</p>
            </div>
        `;
    }

    renderSummary(summary) {
        const summaryItems = summary.map(line => 
            `<li>${this.escapeHtml(line)}</li>`
        ).join('');

        return `
            <div class="card">
                <h2 class="card-title">Summary</h2>
                <ul class="summary-list">
                    ${summaryItems}
                </ul>
            </div>
        `;
    }

    renderObjects(objects) {
        const objectTags = objects.map(obj => 
            `<span class="tag">${this.escapeHtml(obj)}</span>`
        ).join('');

        return `
            <div class="card">
                <h2 class="card-title">Detected Objects</h2>
                <div class="tags-container">
                    ${objectTags}
                </div>
            </div>
        `;
    }

    renderEmotion(emotion) {
        const emotionClass = emotion.toLowerCase().replace(/[^a-z0-9]/g, '');
        return `
            <div class="card">
                <h2 class="card-title">Emotion / Mood</h2>
                <span class="badge-emotion ${emotionClass}">${this.escapeHtml(emotion)}</span>
            </div>
        `;
    }

    renderStory(story) {
        const storyLines = story.map(line => 
            `<div class="story-line">${this.escapeHtml(line)}</div>`
        ).join('');

        return `
            <div class="card story-block">
                <h2 class="card-title">Creative Story</h2>
                ${storyLines}
            </div>
        `;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ImageStoryteller();
});

// Global functions for button actions
function copyStory() {
    const storyResult = document.getElementById('story-result');
    if (storyResult) {
        const storyText = storyResult.textContent;
        
        navigator.clipboard.writeText(storyText).then(() => {
            showToast('Story copied to clipboard!', 'success');
        }).catch(err => {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = storyText;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            showToast('Story copied to clipboard!', 'success');
        });
    }
}

function downloadStory() {
    const storyResult = document.getElementById('story-result');
    const captionResult = document.getElementById('caption-result');
    const objectsResult = document.getElementById('objects-result');
    const emotionResult = document.getElementById('emotion-result');
    
    if (storyResult) {
        const storyText = storyResult.textContent;
        const caption = captionResult ? captionResult.textContent : '';
        const objects = objectsResult ? objectsResult.textContent : '';
        const emotion = emotionResult ? emotionResult.textContent : '';
        
        const content = `AI Generated Story\n\n${'='.repeat(50)}\n\nCaption:\n${caption}\n\nObjects:\n${objects}\n\nEmotion:\n${emotion}\n\nStory:\n${storyText}\n\n${'='.repeat(50)}\nGenerated by AI Storyteller\nhttps://ai-storyteller.com`;
        
        const blob = new Blob([content], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `ai-story-${Date.now()}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        
        showToast('Story downloaded successfully!', 'success');
    }
}

function createNewStory() {
    // Reset everything
    const imageInput = document.getElementById('image-input');
    const imagePreview = document.getElementById('image-preview');
    const analyzeButton = document.getElementById('analyze-button');
    const resultsSection = document.getElementById('results');
    const fileInputLabel = document.querySelector('.file-input-label');
    
    if (imageInput) imageInput.value = '';
    if (imagePreview) imagePreview.style.display = 'none';
    if (analyzeButton) analyzeButton.disabled = true;
    if (resultsSection) resultsSection.style.display = 'none';
    if (fileInputLabel) fileInputLabel.textContent = 'Choose Image';
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
    
    showToast('Ready for a new story!', 'success');
}

function showToast(message, type = 'success') {
    // Create toast element if it doesn't exist
    let toast = document.getElementById('toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'toast';
        toast.className = 'toast';
        document.body.appendChild(toast);
    }
    
    const toastMessage = document.getElementById('toast-message');
    if (!toastMessage) {
        const messageEl = document.createElement('span');
        messageEl.id = 'toast-message';
        toast.appendChild(messageEl);
    }
    
    // Set message and type
    document.getElementById('toast-message').textContent = message;
    toast.className = `toast ${type}`;
    
    // Show toast
    setTimeout(() => toast.classList.add('show'), 100);
    
    // Hide after 3 seconds
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}
