document.addEventListener('DOMContentLoaded', function() {
    const postForm = document.querySelector("#compose-form");
    if (postForm) {
        postForm.addEventListener("submit", (e) => submitPost(postForm, e));
    }

    const editButton = document.querySelectorAll(".edit-btn");
    editButton.forEach(button => {
       button.addEventListener("click", () => showForm(button.parentElement));
    });

    const editForm = document.querySelectorAll(".edit-form");
    editForm.forEach(form => {
       form.addEventListener("submit", (e) => submitEdit(form, e));
    });

    const likeButton = document.querySelectorAll(".submit-like");
    likeButton.forEach(button => {
        const likeForm = button.parentElement.parentElement.parentElement;
        button.addEventListener("click", () => submitLike(likeForm));
        getLikesCount(likeForm)
    });

    const commButton = document.querySelectorAll(".comment-btn");
    commButton.forEach(button => {
       button.addEventListener("click", () => showForm(button.parentElement));
    });

    const commForm = document.querySelectorAll("#comment-form");
    commForm.forEach(form => {
        form.addEventListener("submit", (e) => addComm(form, e));
    });

    const exitAddCommBtn = document.querySelectorAll("#exitCommentForm");
    exitAddCommBtn.forEach(button => {
       button.addEventListener("click", () => exitAddComm(button));
    });

    const deleteButtons = document.querySelectorAll(".delete-btn");
    deleteButtons.forEach(btn => {
        const deleteForm = btn.parentElement;
        const postId = deleteForm.querySelector(".post-id").innerHTML;
        btn.addEventListener("click", () => deletePost(deleteForm, postId));
    });

    const followForm = document.querySelector("#follow");
    if (followForm) {
        followForm.addEventListener("submit", (e) => followUnfollow(followForm, e));
    }

    const posts = document.querySelectorAll(".post");
    posts.forEach(post => {
        getCommCount(post, true);
    });
});

function submitPost(postForm, e) {
    e.preventDefault();
    formData = new FormData(postForm);
    fetch('/create-post', {
        method: 'POST',
        body: formData,
    })
        .then((response) => response.json())
        .then( () => {
            // postForm.reset();
            location.reload();
        })
}

function showForm(post) {
    let editBtn = post.querySelector(".edit-btn");
    let commBtn = post.querySelector(".comment-btn");
    if (editBtn) {
        editBtn.style.display = "none";
        let text = post.querySelector(".post-text").innerText;
        post.querySelector(".post-text").style.display = "none";
        post.querySelector(".edit-form").style.display = "block";
        post.querySelector("textarea").innerHTML = text;
    }
    else if (commBtn) {
        commBtn.style.display = "none";
        post.querySelector("#comment-form-body").style.display = "block";
    }
}

function submitEdit(editForm, e) {
    e.preventDefault();
    formData = new FormData(editForm);
    fetch('/edit-post', {
        method: 'POST',
        body: formData,
    })
        .then((response) => response.json())
        .then(() => {
            const post = editForm.parentElement;
            post.querySelector(".post-text").innerText = post.querySelector(".edit-textarea").value;
            post.querySelector(".post-text").style.display = "block";
            post.querySelector(".edit-form").style.display = "none";
            post.querySelector(".edit-btn").style.display = "block";
        })
}

function addComm(form, e) {
    e.preventDefault();
    formData = new FormData(form);
    const postId = form.querySelector("#post_id").innerHTML;
    const path = `/add-comment/${postId}`
    fetch(path, {
        method: 'POST',
        body: formData,
    })
        .then((response) => response.json())
        .then(() => {
            getCommCount(form);
            form.querySelector(".text-comm").value = "";
            let commBtn = form.parentElement.parentElement.querySelector(".comment-btn");
            commBtn.style.display = "block";
            commBtn.style.marginTop = "-1.3em";
            commBtn.style.marginBottom = "0.44em";
            form.parentElement.style.display = "none";
        })
}

function submitLike(likeForm) {
    formData = new FormData(likeForm);
    fetch('/like', {
        method: 'POST',
        body: formData,
    })
        .then((response) => response.json())
        .then(() => {
            getLikesCount(likeForm);
            const heartBox = likeForm.querySelector("#heart");
            const heart = heartBox.querySelector(".bi-heart");
            const filledHeart = heartBox.querySelector(".bi-heart-fill");
            if (heart) {
                heartBox.innerHTML = "";
                heartBox.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart-fill submit-like" viewBox="0 0 16 17"> <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"></path></svg>';
                const likeBtn = likeForm.querySelector('.submit-like');
                likeBtn.addEventListener("click", () => submitLike(likeForm));
            }
            else if (filledHeart) {
                heartBox.innerHTML = "";
                heartBox.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart submit-like" viewBox="0 0 16 17"><path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"></path></svg>';
                const likeBtn = likeForm.querySelector('.submit-like');
                likeBtn.addEventListener("click", () => submitLike(likeForm));
            }
        })
}

function getLikesCount(form) {
    const postId = form.querySelector(".like-id").value;
    const path = `/show-likes/${postId}`;
    fetch(path)
        .then((response) => response.json())
        .then((data) => {
            form.querySelector(".likes-count").innerHTML = data["likes"];
        })
}

function getCommCount(form, load=false) {
    const postId = form.querySelector("#post_id").innerHTML;
    const path = `/count-comments/${postId}`
    fetch(path)
        .then((response) => response.json())
        .then((data) => {
            if (!load) {
                form.parentElement.parentElement.parentElement.querySelector(".comm-count").innerHTML = data["comm_count"];
                console.log(data["comm_count"]);
            }
            else {
                form.querySelector(".comm-count").innerHTML = data["comm_count"];
                console.log(data["comm_count"]);
            }

        })
}

function exitAddComm(btn) {
    let body = btn.parentElement.parentElement.parentElement.parentElement;
    body.style.display = "none";
    let commBtn = body.parentElement.querySelector(".comment-btn");
    commBtn.style.display = "block";
    commBtn.style.marginTop = "-1.3em";
    commBtn.style.marginBottom = "0.44em";
}

function deletePost(deleteForm, postId) {
    const path = `/delete-post/${postId}`
    formData = new FormData(deleteForm);
    fetch(path, {
        method: 'POST',
        body: formData,
    })
        .then((response) => response.json())
        .then(() => {
            deleteForm.parentElement.remove();
        })
}

function followUnfollow(followForm, e   ) {
    e.preventDefault();
    formData = new FormData(followForm)

    fetch('/follow', {
        method: 'POST',
        body: formData,
    })

        .then(response => response.json())
        .then(() => {
            location.reload();
        })
}
