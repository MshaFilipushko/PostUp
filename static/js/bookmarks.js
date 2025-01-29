
document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".bookmark-btn").forEach(button => {
        button.addEventListener("click", function() {
            let postId = this.getAttribute("data-post-id");

            fetch(`/toggle_bookmark/${postId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "Content-Type": "application/json"
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.bookmarked) {
                    this.classList.remove("btn-outline-secondary");
                    this.classList.add("btn-warning");
                    this.querySelector("span").textContent = "В закладках";
                } else {
                    this.classList.remove("btn-warning");
                    this.classList.add("btn-outline-secondary");
                    this.querySelector("span").textContent = "Закладки";
                }
            });
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            let cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                let cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
