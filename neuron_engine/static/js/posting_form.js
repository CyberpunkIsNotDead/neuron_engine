function displayForm(this_placeholder, other_placeholder, wrapper, other_wrapper, csrf_token) {

  const form = `<form method="POST" enctype="multipart/form-data">
    <input type="hidden" name="csrfmiddlewaretoken" value="` + csrf_token + `">
    <div class="input_form" border="0" cellpadding="0" cellspacing="0">
        <input type="text" name="author" class="textinput" placeholder="Автор" maxlength="100" id="id_author">
        <input type="text" name="subject" class="textinput" placeholder="Тема" maxlength="100" id="id_subject">
        <textarea name="text" class="textarea" placeholder="Текст сообщения" maxlength="3000" required="" id="id_text"></textarea>
        <div id="files_selection">
          <p>Перетащи файл сюда</p>
          <div id="images"></div>
          <input type="file" multiple="" name="upload" id="id_upload">
          <label for="id_upload" class="finput">Выбрать файл(ы)</label>
        </div>
    </div>
    <div id="form_submit">Отправить</div>
  </form>`;
  const hide_form = assembleActionLink('hideForm', other_placeholder, wrapper, other_wrapper, csrf_token, 'Скрыть форму',);

  wrapper.innerHTML = form;
  this_placeholder.innerHTML = hide_form;
  
  if (other_wrapper.hasChildNodes()) {
    const show_form = assembleActionLink('displayForm', this_placeholder, other_wrapper, wrapper, csrf_token, 'Показать форму',);
    other_wrapper.removeChild(other_wrapper.firstChild);
    other_placeholder.innerHTML = show_form;
  };
  
  var drop_area = document.getElementById('files_selection');

  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    drop_area.addEventListener(eventName, preventDefaults, false)
  });

  drop_area.addEventListener('drop', handleDrop, false);

  function preventDefaults (e) {
    e.preventDefault()
    e.stopPropagation()
  };

  function handleDrop(e) {
    let dt = e.dataTransfer
    let files = dt.files

    handleFiles(files)
  };

  var files_arr = [];

  function handleFiles(files) {
    files = [...files]
    files.forEach(previewFile);
    files.forEach(push);
  };

  function previewFile(file) {
    let reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = function() {
      let img = document.createElement('img');
      img.src = reader.result;
      document.getElementById('images').appendChild(img);
    };
  };

  function push(file) {
    files_arr.push(file)
  };

  document.getElementById('form_submit').onclick = function sendFormData() {
    url = window.location.href
    let formData = new FormData(document.querySelector("form"));
    files_arr.forEach(processFile);
    function processFile(file) {
      console.log(file)
      formData.append('upload', file);
    };
    fetch(url, {
      method: 'POST',
      body: formData
    });
  };
    /*.then(() => { ready });
    .catch(() => { error });*/

};


function hideForm(
  this_placeholder,
  other_placeholder,
  wrapper,
  other_wrapper,
  csrf_token
  ) {
  const show_form = assembleActionLink('displayForm', other_placeholder, wrapper, other_wrapper, csrf_token, 'Показать форму',);
  wrapper.removeChild(wrapper.firstChild);
  this_placeholder.innerHTML = show_form;
};

function assembleActionLink(func, p, w1, w2, csrf_token, inner_str) {
  return (`    [ <a href="javascript:void(0);"
  onclick="` + func + `(
  this.parentNode,
  document.getElementById('` + p.id + `'),
  document.getElementById('` + w1.id + `'),
  document.getElementById('` + w2.id + `'),
  '` + csrf_token + `',
  )">` + inner_str + `</a> ]`);
}
