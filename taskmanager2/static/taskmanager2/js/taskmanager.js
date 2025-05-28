document.addEventListener("DOMContentLoaded", function(){
    // Function to attach event listeners to tasks
    function attachTaskEventListeners() {
        // Toggle task completion via AJAX
        document.querySelectorAll(".task-checkbox").forEach(function(checkbox) {
            checkbox.addEventListener("change", function (){
                const taskId = this.dataset.taskId;
                const taskItem = this.closest(".list-group-item");

                fetch(`/task/toggle/${taskId}/`, {
                    method: "POST",
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'X-Requested-With': 'XMLHttpRequest',
                    }
                })
                .then(response => {
                    if (response.ok) {
                        taskItem.classList.toggle("task-completed");
                        taskItem.classList.add("task-completed-animation");
                        setTimeout(() => {
                            taskItem.classList.remove("task-completed-animation");
                        }, 500);
                    }
                })
                .catch(error => {
                    console.error("Error toggling task:", error);
                });
            });
        });

        // Delete Confirmation
        document.querySelectorAll(".btn-outline-danger").forEach(button => {
            button.addEventListener("click", function(e) {
                if (this.textContent.trim() === "Delete" && !confirm("Are you sure you want to delete this task?")) {
                    e.preventDefault();
                } else if (this.textContent.trim() === "Delete" && confirm("Are you sure you want to delete this task?")) {
                    // Allow default action (navigation to delete URL)
                } else if (this.textContent.trim() === "Delete Category" && !confirm("Are you sure you want to delete this category?")) {
                    e.preventDefault();
                } else if (this.textContent.trim() === "Delete Category" && confirm("Are you sure you want to delete this category?")) {
                    // Allow default action for category deletion
                }
            });
        });

        // Format due dates
        document.querySelectorAll(".due-date").forEach(dateElement => {
            const dateText = dateElement.textContent.trim();
            if (dateText) {
                const date = new Date(dateText);
                const today = new Date();
                today.setHours(0,0,0,0);

                if(date < today) {
                    dateElement.classList.add("overdue");
                }
                dateElement.textContent = date.toLocaleDateString("en-US", {
                    month: "short",
                    day: "numeric",
                    year: "numeric"
                });
            }
        });
    }

    // Handle Edit Category buttons
    const categoryModal = document.getElementById("categoryModal");
    if (document.querySelectorAll(".edit-category-btn").length > 0 && categoryModal) {
        document.querySelectorAll(".edit-category-btn").forEach(btn => {
            btn.addEventListener("click", function(e) {
                e.preventDefault();
                const categoryId = this.dataset.categoryId;
                fetch(`/category/edit/${categoryId}/`)
                .then(response => response.text())
                .then(html => {
                    categoryModal.querySelector(".modal-content").innerHTML = html;
                    const bsModal = new bootstrap.Modal(categoryModal);
                    bsModal.show();
                    // Re-attach event listener for the edit category form inside the modal
                    const editCategoryForm = document.getElementById("category-form");
                    if (editCategoryForm) {
                        editCategoryForm.addEventListener("submit", handleCategoryFormSubmit);
                    }
                })
                .catch(error => {
                    console.error("Error fetching category edit form:", error);
                });
            });
        });
    }

    // Category Add Button
    const addCategoryBtn = document.getElementById("add-category-btn");

    if (addCategoryBtn && categoryModal) {
        addCategoryBtn.addEventListener("click", function() {
            // Clear the modal content and set title for adding
            categoryModal.querySelector(".modal-content").innerHTML = `
                <div class="modal-header">
                    <h5 class="modal-title">Add New Category</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <form id="category-form" method="post" action="/category/add/">
                        {% csrf_token %}
                        <div class="mb-3">
                            <label for="category-name" class="form-label">Category Name</label>
                            <input type="text" class="form-control" id="category-name" name="name" required>
                        </div>
                        <button type="submit" class="btn btn-primary">Save</button>
                    </form>
                </div>
            `;
            const bsModal = new bootstrap.Modal(categoryModal);
            bsModal.show();
            // Attach event listener for the add category form inside the modal
            const addCategoryForm = document.getElementById("category-form");
            if (addCategoryForm) {
                addCategoryForm.addEventListener("submit", handleCategoryFormSubmit);
            }
        });
    }

    // Ajax category form submission handler (for both add and edit)
    function handleCategoryFormSubmit(e) {
        e.preventDefault();
        const form = this;
        fetch(form.action, {
            method: 'POST',
            body: new FormData(form),
            headers: {
                "X-CSRFToken": getCookie('csrftoken'),
                "X-Requested-With": "XMLHttpRequest",
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            } else {
                // Handle errors (e.g., display error messages in the modal)
                console.error("Error submitting category form:", data);
                // You might want to update the modal to show errors
            }
        })
        .catch(error => {
            console.error("Error submitting category form:", error);
        });
    }

    // Helper function to get CSRF Token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if(cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Initialize task event listeners on page load
    attachTaskEventListeners();
});