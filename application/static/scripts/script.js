'use strict'

//// Выпадающее меню поисковой строки
const inputMenu = document.querySelector('.input__menu'),
      inputHeader = document.querySelector('.input__header');
inputHeader.addEventListener('focus', () => {
    inputMenu.classList.add('input__menu_active')
})
inputHeader.addEventListener('blur', () => {
    inputMenu.classList.remove('input__menu_active')
})

//// Выпадающее меню жанров
const genreMenu = document.querySelector('.menu'),
      genreMenuList = genreMenu.querySelector('.menu__list'),
      genreMenuButton = genreMenu.querySelector('.menu__button'),
      genreMenuIcon = genreMenu.querySelector('.menu-icon'),
      genreSettingsButton = document.querySelector('.settings__extended-button');

genreMenuButton.addEventListener('click', () => {
    genreMenuList.classList.toggle('menu__list_active');
    genreMenuIcon.classList.toggle('fa-rotate-180');
})

//// Модальное окно авторизации
function showModalWindow() {
    modal.classList.remove('inactive');
}
function removeModalWindow() {
    modal.classList.add('inactive');
}

const modal = document.querySelector('.modal'),
      modalWindow = modal.querySelector('.modal__window'),
      modalCloseButton = modal.querySelector('.modal__close-button');

modalCloseButton.addEventListener('click', removeModalWindow);

modal.addEventListener('click', e => {
    if (e.target != modalWindow)
        removeModalWindow();
})

//// Слайдер рекомендаций (Без анимации)
let minActiveI = 0;
const sliderItems = document.querySelectorAll('.slider__item'),
      slider = document.querySelector('.slider'),
      sliderButtonLeft = document.querySelector('.slider__button-left'),
      sliderButtonRight = document.querySelector('.slider__button-right'),
      itemWidth = 374,
      countOfItems = sliderItems.length,
      countOfItemsInSlider = 6;

sliderButtonLeft.addEventListener('click', () => {
    if (minActiveI > 0)
    {
        sliderItems[minActiveI - 1].classList.add('slider__item_active');
        sliderItems[minActiveI + countOfItemsInSlider -1].classList.remove('slider__item_active');
        minActiveI--;
    }
})

sliderButtonRight.addEventListener('click', () => {
    if (minActiveI < countOfItems - countOfItemsInSlider)
    {
        sliderItems[minActiveI].classList.remove('slider__item_active');
        sliderItems[minActiveI + countOfItemsInSlider].classList.add('slider__item_active');
        minActiveI++;
    }
})

//// Выпадающее меню профиля
const profile = document.querySelector('.header__profile'),
      profileArrow = document.querySelector('.header__profile__arrow'),
      profileMenu = document.querySelector('.header__profile__menu');

profile.addEventListener('click', () => {
    profileArrow.classList.toggle('fa-rotate-180');
    profileMenu.classList.toggle('header__profile__menu_active');
})

//// Функционал кнопок жанров
// const settingsTypes = document.querySelector('.types'),
//       settingsButtons = settingsTypes.querySelectorAll('.types__item'),
//       firstRow = [settingsButtons[0], settingsButtons[1]],
//       secondRow = [settingsButtons[2], settingsButtons[3]];

//// Работа с кнопками настроек
const settingsForms = document.querySelectorAll('.settings__form');

for (let settingsForm of settingsForms) {
    settingsForm.addEventListener('submit', e => {
        let request = fetch('http://127.0.0.1:5000', { 
            method: "POST", 
            headers:{"content-type":"application/json"}
        }).then(response => response.text())
        console.log(request)
    });
}

//// Работа с карточками

// const cardFilmList1 = document.querySelectorAll('.input__menu__item'),
//       cardFilmList2 = document.querySelectorAll('.list__item');

// for (let film of cardFilmList1) {
//     film.addEventListener('click', e => {

//     })
// }