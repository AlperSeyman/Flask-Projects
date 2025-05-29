document.querySelectorAll('.delete-btn').forEach(button => {
    button.addEventListener('click', () => {
        const noteId = button.getAttribute('data-id'); // data-id değerini al
        fetch("/delete-note", {
            method: "POST",
            body: JSON.stringify({ noteId: noteId }),
            headers: {
                "Content-Type": "application/json" // Header ekle
            }
        }).then(response => {
            if (response.ok) {
                window.location.href = "/"; // Silme başarılıysa sayfayı yenile
            } else {
                response.json().then(data => console.error(data.error));
            }
        }).catch(error => console.error('Error:', error));
    });
});
