document.addEventListener('DOMContentLoaded', function() {
    const likeButton = document.querySelectorAll(".submit-like");
    likeButton.forEach(button => {
        const p = button.parentElement;
        button.addEventListener("click", () => submitLike(p.parentElement));
    });
});

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

// function showUserData() {
//     setTimeout(function() {
//         document.querySelector("#posts").innerHTML = "";
//         fetch('/following-posts')
//             .then(response => response.json())
//             .then(data => {
//                 data["posts"].forEach(post => {
//                     const element = document.createElement('article');
//                     element.innerHTML = `<a href="user/${post['author']}"><h3>${post['author']}</h3></a>`;
//                     element.innerHTML += `<p>${post['text']}</p>`;
//                     element.innerHTML += `<p>${post['timestamp']}</p>`;
//                     element.innerHTML += `<p>${post['likes']}</p>`;
//                     element.setAttribute('id', 'post');
//                     document.querySelector('#posts').append(element);
//                 });
//             });
//     }, 500);
// };