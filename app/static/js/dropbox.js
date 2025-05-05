document.addEventListener('DOMContentLoaded', function() {
    const dropbox = document.getElementById('dropbox');
    const fileInput = document.querySelector('input[type="file"]'); // Get the file input directly
    const uploadForm = document.getElementById('uploadForm');

    // Make dropbox clickable to open file selection
    dropbox.addEventListener('click', () => {
        fileInput.click();
    });

    // Submit form when file is selected through the file input
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            // Update dropbox text to show selected file
            dropbox.textContent = `Selected file: ${fileInput.files[0].name}`;
            // Don't auto-submit, let user click the upload button
        }
    });

    // Handle drag events
    dropbox.addEventListener('dragover', (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropbox.classList.add('dragover');
    });

    dropbox.addEventListener('dragleave', (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropbox.classList.remove('dragover');
    });

    dropbox.addEventListener('drop', (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropbox.classList.remove('dragover');
        
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length > 0) {
            // Check if the file has the correct extension
            const fileName = files[0].name;
            const fileExt = fileName.split('.').pop().toLowerCase();
            
            // Get the current page URL to determine which extension to check
            const currentPath = window.location.pathname;
            const isImage = currentPath.includes('word-to-pptx');
            const validExt = isImage ? 'png' : 'jpg' || 'jpeg';
            
            if (fileExt === validExt) {
                fileInput.files = files;
                // Update dropbox text to show selected file
                dropbox.textContent = `Selected file: ${fileName}`;
                // Don't auto-submit, let user click the upload button
            } else {
                alert(`Please upload only .${validExt} files.`);
            }
        }
    });
});
