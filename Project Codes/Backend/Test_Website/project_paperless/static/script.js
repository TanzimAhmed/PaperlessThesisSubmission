/*
window.addEventListener('scroll', stick_nav_bar);

let nav_bar = document.querySelector('#navigation_bar');
let stuck = false;
function stick_nav_bar() {
  if (!stuck && window.scrollY > 50) {
    nav_bar.classList.add('stick_nav_bar');
    document.querySelector('#logo').style.backgroundColor = 'transparent';
    stuck = true;
  } else if (stuck && window.scrollY < 50){
    nav_bar.classList.remove('stick_nav_bar');
    document.querySelector('#logo').style.backgroundColor = 'rgba(255, 255, 255,0.8)';
    stuck = false;
  }
}
*/

// to auto stick navbar after reload
// stick_nav_bar();