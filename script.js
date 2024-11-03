document.getElementById('upload-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];
    const messageDiv = document.getElementById('message');

    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('https://secure-file-transfers.onrender.com/upload', { // Your backend URL
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            messageDiv.innerText = result.message;
        } catch (error) {
            messageDiv.innerText = 'Error uploading file.';
        }
    } else {
        messageDiv.innerText = 'No file selected.';
    }
});
