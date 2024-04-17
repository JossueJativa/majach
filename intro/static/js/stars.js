const stars = document.querySelectorAll('.star');

stars.forEach((star, index) => {
    star.addEventListener('click', () => {
        for(let i = 0; i <=index; i++) {
            stars[i].classList.add('star-selected');
        }
        for(let i = index + 1; i < stars.length; i++) {
            stars[i].classList.remove('star-selected');
        }
    });
});