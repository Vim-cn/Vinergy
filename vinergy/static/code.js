var do_highlight = function(href){
  var a = document.querySelectorAll('.highlight .linenodiv a.linehighlight');
  for(var i=0, len=a.length; i<len; i++){
    if(a[i].href != window.location.href){
      a[i].className = '';
    }
  }
  a = document.querySelector('.highlight .linenodiv a[href="' + href + '"]');
  if(a){
    a.className = 'linehighlight';
  }
}
if(window.location.hash !== ''){
  window.scrollBy(-900, 0);
  do_highlight(window.location.hash);
}
window.addEventListener('hashchange', function(e){
  do_highlight(window.location.hash);
  if(window.location.hash !== ''){
    window.scrollBy(-900, 0);
  }
}, false);
var lines = document.getElementsByClassName('line');
for(var i=0, len=lines.length; i<len; i++){
  lines[i].addEventListener('mouseover', function(e){
    console.log(e);
    var t = e.target;
    while(t.nodeName != 'DIV'){
      t = t.parentNode;
    }
    var href = '#' + t.getAttribute('id');
    do_highlight(href);
  }, false);
}
var highlights = document.getElementsByClassName('highlight');
for(var i=0, len=highlights.length; i<len; i++){
  highlights[i].addEventListener('mouseout', function(e){
    do_highlight('nonexists');
  }, false);
}
