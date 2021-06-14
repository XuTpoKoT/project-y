'use strict'

//// Выпадающее меню поисковой строки
const inputMenu = document.querySelector('.input__menu'),
      inputHeader = document.querySelector('.input__header');
inputHeader.addEventListener('focus', () => {
    inputMenu.classList.add('input__menu_active')
})
inputHeader.addEventListener('click', () => {
    inputMenu.classList.add('input__menu_active')
})
inputMenu.addEventListener('mouseout', () => {
    inputMenu.classList.remove('input__menu_active')
})
inputMenu.addEventListener('mouseover', () => {
    inputMenu.classList.add('input__menu_active')
})

//// Выпадающее меню жанров
const genreMenu = document.querySelector('.menu'),
      genreMenuList = document.querySelector('.menu__list'),
      genreMenuButton = document.querySelector('.settings__form__key'),
      genreMenuIcon = document.querySelector('.menu-icon');

genreMenuButton.addEventListener('click', () => {
    genreMenuList.classList.toggle('menu__list_active');
    genreMenuIcon.classList.toggle('fa-rotate-180');
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

//// Работа с кнопками настроек
const settingsForms = document.querySelectorAll('.settings__form');

for (let settingsForm of settingsForms) {
    settingsForm.addEventListener('submit', e => {
        let request = fetch('/', { 
            method: "POST", 
            headers:{"content-type":"application/json"}
        }).then(response => response.text())
    });
}

//// Работа с кнопками настроек жангров
const genreList = document.querySelectorAll('li.menu__list__item'),
      inputGenreSettings = document.querySelector('form.settings__form').querySelector('input');
let genre;
for (let genreLi of genreList) {
    genreLi.addEventListener('click', e => {
        genre = e.target.innerHTML;
        genre = genre.toLowerCase();
        inputGenreSettings.value = genre;
        genreMenuList.classList.toggle('menu__list_active');
    })
}

//// Позиционирование блока настроек
$(document).ready(() => {
    const navOffset = $('.settings').offset().top;
    $(window).scroll(() => {
        const scrolled = $(this).scrollTop();
        if (scrolled + 50 > navOffset) {
            $('.settings').addClass('settings_fixed')
        } else {
            $('.settings').removeClass('settings_fixed')
        }
    })
})