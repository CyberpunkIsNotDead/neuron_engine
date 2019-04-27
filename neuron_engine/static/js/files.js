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
