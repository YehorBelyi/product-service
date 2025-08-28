const changeProductPhoto = (src) => {
    const image = document.querySelector('.main-image img');
    if (image) {
        image.src = src;
    }
}