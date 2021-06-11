'use strict'

//// Рендеринг карточек фильмов
// Функция рендера карточки фильма в блоке filmList
function RenderFilmCard(data) {
    let filmBlock = document.createElement('div');
    filmBlock.classList.add('list__item');
    filmBlock.innerHTML = 
    `
        <div class="list__item__info">
            <div class="list__item__info__title">       
                ${data.title}         
            </div>
            <div class="list__item__info__original-title">
                ${data.originalTitle}
            </div>
        </div>
        <div class="list__item__rating">
            ${data.rating}
        </div>
    `
    filmList.append(filmBlock);
}

const filmList = document.querySelector('#root'),
      filmsData = [ 
    {
        'id': '326', 
        'type': '1', 
        'title': 'Побег из Шоушенка (1994)', 
        'originalTitle': 'The Shawshank Redemption', 
        'year': '1994', 'country': 'США', 
        'director': 'Фрэнк Дарабонт', 
        'budget': '$25000000', 
        'runtime': '142 мин. / 02:22', 
        'worldGross': '+ $77218 = $28418687', 
        'genres': 'драма', 
        'age': '16+', 
        'actors': 'Тим Роббинс, Морган Фриман, Боб Гантон, Уильям Сэдлер, Клэнси Браун, Гил Беллоуз, Марк Ролстон, Джеймс Уитмор, Джеффри ДеМанн, Ларри Бранденбург', 
        'description': 'Бухгалтер Энди Дюфрейн обвинён в убийстве собственной жены и её любовника. Оказавшись в тюрьме под названием Шоушенк, он сталкивается с жестокостью и беззаконием, царящими по обе стороны решётки. Каждый, кто попадает в эти стены, становится их рабом до конца жизни. Но Энди, обладающий живым умом и доброй душой, находит подход как к заключённым, так и к охранникам, добиваясь их особого к себе расположения.', 
        'image': 'img-data/326.jpg', 
        'imageUrl': 'http://avatars.mds.yandex.net/get-kinopoisk-image/1599028/0b..', 
        'rating': '9.1', 
        'count': '766K', 
        'ratingImdb': '9.30', 
        'countImdb': '2 403K'
    },
    {
        'id': '86326', 
        'type': '1', 
        'title': 'Счастливое число Слевина (2005)', 
        'originalTitle': 'Lucky Number Slevin', 
        'year': '2005', 
        'country': 'Германия, Великобритания, США, Канада', 
        'director': 'Пол МакГиган', 
        'budget': '$27000000', 
        'runtime': '110 мин. / 01:50', 
        'worldGross': '+ $33813415 = $56308881', 
        'genres': 'боевик, триллер, драма, криминал', 
        'age': '16+', 
        'actors': 'Джош Хартнетт, Брюс Уиллис, Люси Лью, Морган Фриман, Бен Кингсли, Майкл Рубенфильд, Питер Аутербридж, Стэнли Туччи, Кевин Чэмберлин, Дориан Миссик', 
        'description': 'Слевину не везет. Дом опечатан, девушка ушла к другому… Его друг Ник уезжает из Нью-Йорка и предлагает Слевину пожить в пустой квартире. В это время крупный криминальный авторитет по прозвищу Босс хочет рассчитаться со своим бывшим партнером за убийство сына и в отместку «заказать» его наследника.', 
        'image': 'img-data/86326.jpg', 
        'imageUrl': 'http://avatars.mds.yandex.net/get-kinopoisk-image/1704946/92..', 
        'rating': '8.1', 
        'count': '326K', 
        'ratingImdb': '7.70', 
        'countImdb': '302K'
    },
    {
        'id': '435', 
        'type': '1', 
        'title': 'Зеленая миля (1999)', 
        'originalTitle': 'The Green Mile', 
        'year': '1999', 'country': 'США', 
        'director': 'Фрэнк Дарабонт', 
        'budget': '$60000000', 
        'runtime': '189 мин. / 03:09',
        'worldGross': '+ $150000000 = $286801374', 
        'genres': 'фэнтези, драма, криминал, детектив', 
        'age': '16+', 
        'actors': 'Том Хэнкс, Дэвид Морс, Бонни Хант, Майкл Кларк Дункан, Джеймс Кромуэлл, Майкл Джитер, Грэм Грин, Даг Хатчисон, Сэм Рокуэлл, Барри Пеппер', 
        'description': 'Пол Эджкомб - начальник блока смертников в тюрьме «Холодная гора», каждый из узников которого однажды проходит «зеленую милю» по пути к месту казни. Пол повидал много заключённых и надзирателей за время работы. Однако гигант Джон Коффи, обвинённый в страшном преступлении, стал одним из самых необычных обитателей блока.', 
        'image': 'img-data/435.jpg', 
        'imageUrl': 'http://avatars.mds.yandex.net/get-kinopoisk-image/1599028/40..', 
        'rating': '9.1', 
        'count': '669K', 
        'ratingImdb': '8.60', 
        'countImdb': '1 177K'
    },
    {
        'id': '448', 
        'type': '1', 
        'title': 'Форрест Гамп (1994)', 
        'originalTitle': 'Forrest Gump', 
        'year': '1994', 
        'country': 'США', 
        'director': 'Роберт Земекис', 
        'budget': '$55000000', 
        'runtime': '142 мин. / 02:22', 
        'worldGross': '+ $347693217 = $677387716', 
        'genres': 'драма, мелодрама, комедия, история, военный', 
        'age': '12+', 
        'actors': 'Том Хэнкс, Робин Райт, Салли Филд, Гэри Синиз, Майкелти Уильямсон, Майкл Коннер Хэмпфри, Ханна Р. Холл, Сэм Андерсон, Шиван Фэллон, Ребекка Уильямс', 
        'description': 'От лица главного героя Форреста Гампа, слабоумного безобидного человека с благородным и открытым сердцем, рассказывается история его необыкновенной жизни.', 
        'image': 'img-data/448.jpg', 
        'imageUrl': 'http://avatars.mds.yandex.net/get-kinopoisk-image/1599028/35..', 
        'rating': '8.9', 
        'count': '619K', 
        'ratingImdb': '8.80', 
        'countImdb': '1 857K'
    },
    {
        'id': '324', 
        'type': '1', 
        'title': 'Поймай меня, если сможешь (2002)', 
        'originalTitle': 'Catch Me If You Can', 
        'year': '2002', 
        'country': 'США, Канада', 
        'director': 'Стивен Спилберг', 
        'budget': '$52000000', 
        'runtime': '141 мин. / 02:21', 
        'worldGross': '+ $187498961 = $352114312', 
        'genres': 'криминал, биография, комедия', 
        'age': '12+', 
        'actors': 'Леонардо ДиКаприо, Том Хэнкс, Кристофер Уокен, Мартин Шин, Натали Бай, Эми Адамс, Джеймс Бролин, Брайан Хау, Фрэнк Джон Хьюз, Стив Истин', 
        'description': 'Фрэнк Эбегнейл успел поработать врачом, адвокатом и пилотом на пассажирской авиалинии – и все это до достижения полного совершеннолетия в 21 год. Мастер в обмане и жульничестве, он также обладал искусством подделки документов, что в конечном счете принесло ему миллионы долларов, которые он получил по фальшивым чекам.', 
        'image': 'img-data/324.jpg', 
        'imageUrl': 'http://avatars.mds.yandex.net/get-kinopoisk-image/1704946/e3..', 
        'rating': '8.5', 
        'count': '425K', 
        'ratingImdb': '8.10', 
        'countImdb': '859K'
    },
    {
        'id': '448', 
        'type': '1', 
        'title': 'Форрест Гамп (1994)', 
        'originalTitle': 
        'Forrest Gump', 
        'year': '1994', 
        'country': 'США', 
        'director': 'Роберт Земекис', 
        'budget': '$55000000', 
        'runtime': '142 мин. / 02:22', 
        'worldGross': '+ $347693217 = $677387716', 
        'genres': 'драма, мелодрама, комедия, история, военный', 
        'age': '12+', 
        'actors': 'Том Хэнкс, Робин Райт, Салли Филд, Гэри Синиз, Майкелти Уильямсон, Майкл Коннер Хэмпфри, Ханна Р. Холл, Сэм Андерсон, Шиван Фэллон, Ребекка Уильямс', 
        'description': 'От лица главного героя Форреста Гампа, слабоумного безобидного человека с благородным и открытым сердцем, рассказывается история его необыкновенной жизни.', 
        'image': 'img-data/448.jpg',
        'imageUrl': 'http://avatars.mds.yandex.net/get-kinopoisk-image/1599028/35..', 
        'rating': '8.9', 
        'count': '619K', 
        'ratingImdb': '8.80', 
        'countImdb': '1 857K'
    }
]

// Рендер всех фильмов
for (let filmData of filmsData) {
    RenderFilmCard(filmData);
}


//// Выпадающее меню
const menu = document.querySelector('.menu'),
      menuList = menu.querySelector('.menu__list'),
      menuButton = menu.querySelector('.menu__button'),
      menuIcon = menu.querySelector('.menu-icon'),
      settingsButton = document.querySelector('.settings__extended-button');

menuButton.addEventListener('click', () => {
    menuList.classList.toggle('menu__list_active');
    menuIcon.classList.toggle('fa-rotate-180');
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