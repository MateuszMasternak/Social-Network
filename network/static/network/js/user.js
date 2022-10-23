document.addEventListener('DOMContentLoaded', function() {
    // showUserData();
    const followForm = document.querySelector("#follow");
    if (followForm) {
        followForm.addEventListener("submit", (e) => followUnfollow(followForm, e));
    }

    const editButton = document.querySelectorAll(".edit-btn");
    editButton.forEach(button => {
       button.addEventListener("click", () => editPost(button.parentElement));
    });

    const editForm = document.querySelectorAll(".edit-form");
    editForm.forEach(form => {
       form.addEventListener("submit", (e) => submitEdit(form, e));
    });

    const likeButton = document.querySelectorAll(".submit-like");
    likeButton.forEach(button => {
        const p = button.parentElement;
        button.addEventListener("click", () => submitLike(p.parentElement));
    });

    const deleteButtons = document.querySelectorAll(".delete-btn");
    deleteButtons.forEach(btn => {
        console.log(btn);
        const deleteForm = btn.parentElement;
        const postId = deleteForm.querySelector(".post-id").innerHTML;
        btn.addEventListener("click", () => deletePost(deleteForm, postId));
    });
});

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

function editPost(post) {
    post.querySelector(".edit-btn").style.display = "none";
    let text = post.querySelector(".post-text").innerText;
    post.querySelector(".post-text").style.display = "none";
    post.querySelector(".edit-form").style.display = "block";
    post.querySelector("textarea").innerHTML = text;
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

function submitLike(likeForm) {
    formData = new FormData(likeForm);
    fetch('/like', {
        method: 'POST',
        body: formData,
    })
        .then((response) => response.json())
        .then(() => {
            getLikesCount(likeForm);
        })
}

function getLikesCount(parent) {
    const postId = parent.querySelector(".like-id").value;
    const path = `/show-likes/${postId}`;
    fetch(path)
        .then((response) => response.json())
        .then((data) => {
            const likesNumber = data["likes"];
            parent.querySelector(".likes-count").innerHTML = likesNumber;
        })
}

function deletePost(deleteForm, postId) {
    path = `/delete-post/${postId}`
    formData = new FormData(deleteForm);
    fetch(path, {
        method: 'POST',
        body: formData,
    })
        .then((response) => response.json())
        .then(() => {
            console.log("DONE");
            deleteForm.parentElement.remove();
        })
}
