function showFullName(obj, full_name) {
  obj.innerHTML=full_name;
  obj.style.backgroundColor='black';
  obj.style.minWidth='16em';
  obj.style.width='auto';
  obj.style.overflow='visible';
  obj.style.zIndex='2';
};

function showShortName(obj, size, short_name) {
  obj.innerHTML=size+', '+short_name;
  obj.style.backgroundColor='transparent';
  obj.style.width='16em';
  obj.style.overflow='hidden';
  obj.style.zIndex='1';
};

var single_pics = document.getElementsByClassName('single_pic');

var links = {};

for(let i = 0; i < single_pics.length; i++) {
  single_pics[i].addEventListener("click", expandSinglePic, false);
};

function expandSinglePic(e) {
  e.preventDefault();

  let link = this.getAttribute("href");
  let thumb_link = this.children[0].src;

  Object.assign(links, {[link]: thumb_link});

  this.innerHTML = '<img src="' + link + '">';
  this.className = 'single_pic_expanded';
  this.parentNode.style.gridTemplateColumns = 'auto';
  this.parentNode.style.gridTemplateRows = 'auto auto';

  this.removeEventListener("click", expandSinglePic, false);
  this.addEventListener("click", collapseSinglePic, false);
};

function collapseSinglePic(e) {
  e.preventDefault();

  let link = this.getAttribute("href");
  let thumb_link = links[link];

  this.innerHTML = '<img class="thumbnail" src="' + thumb_link + '">';
  this.className = 'single_pic';
  this.parentNode.style.gridTemplateColumns = '';
  this.parentNode.style.gridTemplateRows = '';

  this.removeEventListener("click", collapseSinglePic, false);
  this.addEventListener("click", expandSinglePic, false);
  delete links[link];
};

var multiple_pics = document.getElementsByClassName('multiple_pic');

for(let i = 0; i < multiple_pics.length; i++) {
  multiple_pics[i].addEventListener("click", expandMultiplePic, false);
};

function expandMultiplePic(e) {
  e.preventDefault();

  let link = this.getAttribute("href");
  let thumb_link = this.children[0].src;

  Object.assign(links, {[link]: thumb_link});

  this.innerHTML = '<img src="' + link + '">';
  this.className = 'multiple_pic_expanded';
  this.parentNode.style.height = 'min-content';
  this.parentNode.style.width = 'min-content';

  this.parentNode.parentNode.style.height = 'auto';
  this.parentNode.parentNode.style.width = 'auto';
  this.parentNode.parentNode.style.display = 'block';
  this.parentNode.parentNode.style.margin = '10px 10px';

  this.removeEventListener("click", expandMultiplePic, false);
  this.addEventListener("click", collapseMultiplePic, false);
};

function collapseMultiplePic(e) {
  e.preventDefault();

  let link = this.getAttribute("href");
  let thumb_link = links[link];

  this.innerHTML = '<img class="thumbnail" src="' + thumb_link + '">';
  this.className = 'multiple_pic';
  this.parentNode.style.height = '';
  this.parentNode.style.width = '';

  this.parentNode.parentNode.style.height = '';
  this.parentNode.parentNode.style.width = '';
  this.parentNode.parentNode.style.display = '';
  this.parentNode.parentNode.style.margin = '';

  this.removeEventListener("click", collapseMultiplePic, false);
  this.addEventListener("click", expandMultiplePic, false);
  delete links[link];
};
