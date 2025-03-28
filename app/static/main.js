document.addEventListener('DOMContentLoaded', (event) => {
    // Obtener la URL actual
    const currentUrl = window.location.pathname;

    // Obtener todos los elementos de navegación
    const navLinks = document.querySelectorAll('.nav__link');

    // Recorrer todos los enlaces de navegación
    navLinks.forEach(link => {
        // Obtener el href del enlace
        const linkHref = link.getAttribute('href');

        // Si la URL actual coincide con el href del enlace
        if (linkHref === currentUrl) {
            // Remover la clase active-link de cualquier enlace que la tenga
            document.querySelector('.nav__link.active-link')?.classList.remove('active-link');

            // Agregar la clase active-link al enlace actual
            link.classList.add('active-link');
        }
    });
});


/*=============== SCROLL SECTIONS ACTIVE LINK ===============*/



const sections = document.querySelectorAll('section[id]')

function scrollActive(){
    const scrollY = window.pageYOffset

    sections.forEach(current =>{
        const sectionHeight = current.offsetHeight,
            sectionTop = current.offsetTop - 50,
            sectionId = current.getAttribute('id')

        if(scrollY > sectionTop && scrollY <= sectionTop + sectionHeight){
            document.querySelector('.nav__menu a[href*=' + sectionId + ']').classList.add('active-link')
        }else{
            document.querySelector('.nav__menu a[href*=' + sectionId + ']').classList.remove('active-link')
        }
    })
}
window.addEventListener('scroll', scrollActive)


/*=============== CHANGE BACKGROUND HEADER ===============*/
function scrollHeader(){
    const header = document.getElementById('header')
    // When the scroll is greater than 80 viewport height, add the scroll-header class to the header tag
    if(this.scrollY >= 80) header.classList.add('scroll-header'); else header.classList.remove('scroll-header')
}
window.addEventListener('scroll', scrollHeader)