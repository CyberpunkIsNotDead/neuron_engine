var body = document.body;
console.log(body)

var width = body.clientWidth;
console.log(width);

var texts = document.querySelectorAll('.text');

for (i = 0; i < texts.length; i++) {
  texts[i].style.maxWidth=width-300+'px';
  console.log(texts[i].style.maxWidth);
};

body.onresize = function() {
  width = body.clientWidth;
  for (i = 0; i < texts.length; i++) {
    console.log(texts[i].clientWidth)
    texts[i].style.maxWidth=width-300+'px';
    console.log(texts[i]);
    console.log(texts[i].style.maxWidth);
  };
};
