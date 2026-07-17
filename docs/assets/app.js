(function(){
document.addEventListener('DOMContentLoaded', function() {
  var cur = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.topbar a:not(.topbar-brand)').forEach(function(a) {
    if (a.getAttribute('href') === cur) a.classList.add('active');
  });
});
})();
