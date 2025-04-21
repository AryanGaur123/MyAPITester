// API Tester JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Add event listener to method selector to toggle request body visibility
    const methodSelector = document.getElementById('id_method');
    const bodyContainer = document.getElementById('id_body').closest('.mb-3');
    
    if (methodSelector && bodyContainer) {
        // Initial check
        toggleBodyVisibility();
        
        // Add change event listener
        methodSelector.addEventListener('change', toggleBodyVisibility);
        
        function toggleBodyVisibility() {
            const method = methodSelector.value;
            if (method === 'GET' || method === 'DELETE') {
                bodyContainer.style.display = 'none';
            } else {
                bodyContainer.style.display = 'block';
            }
        }
    }
    
    // Add copy button functionality for response data
    const copyButtons = document.querySelectorAll('.copy-btn');
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const textToCopy = this.getAttribute('data-copy-target');
            const targetElement = document.querySelector(textToCopy);
            
            if (targetElement) {
                const textArea = document.createElement('textarea');
                textArea.value = targetElement.textContent;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                
                // Show copied tooltip
                this.setAttribute('data-original-title', 'Copied!');
                const tooltip = bootstrap.Tooltip.getInstance(this);
                tooltip.show();
                
                // Reset tooltip after 2 seconds
                setTimeout(() => {
                    this.setAttribute('data-original-title', 'Copy to clipboard');
                }, 2000);
            }
        });
    });
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Add JSON validation for request body
    const requestBodyField = document.getElementById('id_body');
    const requestForm = requestBodyField ? requestBodyField.closest('form') : null;
    
    if (requestForm && requestBodyField) {
        requestForm.addEventListener('submit', function(event) {
            const method = methodSelector.value;
            const bodyContent = requestBodyField.value.trim();
            
            // Only validate JSON for POST and PUT requests with content
            if ((method === 'POST' || method === 'PUT') && bodyContent !== '') {
                try {
                    JSON.parse(bodyContent);
                } catch (e) {
                    event.preventDefault();
                    alert('Invalid JSON in request body. Please check your syntax.');
                }
            }
        });
    }
});
