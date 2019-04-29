function displayForm(this_placeholder, other_placeholder, wrapper, other_wrapper, csrf_token) {

  const form = `<form method="POST" enctype="multipart/form-data">
    <input type="hidden" name="csrfmiddlewaretoken" value="` + csrf_token + `">
    <table class="input_form" border="0" cellpadding="0" cellspacing="0">
      <tr>
        <td>
          <div style="margin: 0 10px 0 0">
            <input type="text" name="author" class="textinput" placeholder="Автор" maxlength="100" id="id_author">
          </div>
        </td>
      </tr>
      <tr>
        <td>
          <div style="margin: 0 10px 0 0">
            <input type="text" name="subject" class="textinput" placeholder="Тема" maxlength="100" id="id_subject">
          </div>
        </td>
      </tr>
      <tr>
        <td>
          <textarea name="text" cols="40" rows="10" class="textarea" placeholder="Текст сообщения" maxlength="3000" required="" id="id_text"></textarea>
        </td>
      </tr>
      <tr>
        <td>
          <input type="file" multiple="" name="upload" id="id_upload">
          <label for="id_upload" class="finput">Выбрать файл</label>
        </td>
      </tr>
    </table>
    <button class="form_submit" type="submit">Отправить</button>
  </form>`;
  const hide_form = assembleActionLink('hideForm', other_placeholder, wrapper, other_wrapper, csrf_token, 'Скрыть форму',);
  wrapper.innerHTML = form;
  this_placeholder.innerHTML = hide_form;
  
  if (other_wrapper.hasChildNodes()) {
    const show_form = assembleActionLink('displayForm', this_placeholder, other_wrapper, wrapper, csrf_token, 'Показать форму',);
    other_wrapper.removeChild(other_wrapper.firstChild);
    other_placeholder.innerHTML = show_form;
  };

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
