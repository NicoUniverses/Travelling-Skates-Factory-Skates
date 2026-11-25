(function(){
  function masonry(){
    document.querySelectorAll('.masonry').forEach(function(m){
      var cols=+m.getAttribute('data-cols')||3, gap=+m.getAttribute('data-gap')||25;
      var items=[].slice.call(m.children); if(!items.length) return;
      var w=(m.clientWidth-gap*(cols-1))/cols, hs=[];
      for(var c=0;c<cols;c++) hs.push(0);
      items.forEach(function(it){
        var c=hs.indexOf(Math.min.apply(null,hs));
        it.style.left=(c*(w+gap))+'px'; it.style.top=hs[c]+'px'; it.style.width=w+'px';
        hs[c]+=it.offsetHeight+gap;
      });
      var h=Math.max.apply(null,hs)-gap; m.style.height=h+'px';
      var st=m.parentNode, need=m.offsetTop+h;
      if(st.classList.contains('stage')&&need>st.offsetHeight) st.style.height=need+'px';
    });
  }
  masonry();
  if(document.fonts&&document.fonts.ready) document.fonts.ready.then(masonry);
  window.addEventListener('load',masonry);

  function slider(root, slideSel, dotSel, prevSel, nextSel, onChange){
    var slides=[].slice.call(root.querySelectorAll(slideSel));
    var dots=[].slice.call(root.querySelectorAll(dotSel));
    if(!slides.length) return;
    var i=0, timer=null, auto=parseFloat(root.getAttribute('data-auto'))||0;
    function go(n){
      slides[i].classList.remove('on'); if(dots[i]) dots[i].classList.remove('on');
      i=(n+slides.length)%slides.length;
      slides[i].classList.add('on');
      if(dots[i]){dots[i].classList.add('on'); var p=dots[i].parentNode; if(p.scrollWidth>p.clientWidth){p.scrollLeft=dots[i].offsetLeft-p.clientWidth/2+dots[i].clientWidth/2;}}
      if(onChange) onChange(slides,i);
      restart();
    }
    function restart(){ if(timer) clearInterval(timer); if(auto>0&&slides.length>1) timer=setInterval(function(){go(i+1)},auto*1000); }
    dots.forEach(function(d,n){d.addEventListener('click',function(){go(n)})});
    slides.forEach(function(s,n){s.addEventListener('click',function(){ if(n!==i&&onChange) go(n); })});
    var p=root.querySelector(prevSel), nx=root.querySelector(nextSel);
    if(p) p.addEventListener('click',function(){go(i-1)});
    if(nx) nx.addEventListener('click',function(){go(i+1)});
    if(onChange){ onChange(slides,i); window.addEventListener('resize',function(){onChange(slides,i)}); }
    restart();
  }
  function showcase(slides,i){
    var stage=slides[0].parentNode, w=stage.clientHeight*4/3, x0=(stage.clientWidth-w)/2;
    slides.forEach(function(s,k){ s.style.width=w+'px'; s.style.left=(x0+(k-i)*(w+5))+'px'; });
  }
  document.querySelectorAll('.thumbs').forEach(function(r){
    var full=(r.getAttribute('style')||'').indexOf('100vw')>-1;
    if(full) r.classList.add('showcase');
    slider(r,'.t-slide','.t-th','.t-prev','.t-next', full?showcase:null);
  });
  document.querySelectorAll('.strip-ss').forEach(function(r){slider(r,'.ss-slide','.ss-dot','.ss-prev','.ss-next')});

  document.querySelectorAll('.yt-lite').forEach(function(b){
    b.addEventListener('click',function(){
      if(b.querySelector('iframe')) return;
      var f=document.createElement('iframe');
      f.src='https://www.youtube-nocookie.com/embed/'+b.getAttribute('data-yt')+'?autoplay=1';
      f.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture'; f.allowFullscreen=true;
      b.innerHTML=''; b.appendChild(f);
    });
  });

  document.querySelectorAll('[data-fbshare]').forEach(function(a){
    a.href='https://www.facebook.com/sharer/sharer.php?u='+encodeURIComponent(location.href); a.target='_blank'; a.rel='noopener';
  });

  var lb=document.getElementById('lb');
  if(lb){
    var img=lb.querySelector('img'), t=lb.querySelector('.g-t'), d=lb.querySelector('.g-d');
    var group=[], idx=0;
    function show(n){ idx=(n+group.length)%group.length; var e=group[idx];
      img.src=e.getAttribute('data-src'); img.alt=e.getAttribute('data-title')||'';
      t.textContent=e.getAttribute('data-title')||''; d.textContent=e.getAttribute('data-desc')||''; }
    document.addEventListener('click',function(ev){
      var e=ev.target.closest('[data-lb]'); if(!e) return;
      group=[].slice.call(document.querySelectorAll('[data-lb="'+e.getAttribute('data-lb')+'"]'));
      show(group.indexOf(e)); lb.hidden=false; document.body.style.overflow='hidden';
    });
    function close(){lb.hidden=true; document.body.style.overflow='';}
    lb.querySelector('.lb-x').addEventListener('click',close);
    lb.querySelector('.lb-p').addEventListener('click',function(){show(idx-1)});
    lb.querySelector('.lb-n').addEventListener('click',function(){show(idx+1)});
    lb.addEventListener('click',function(ev){ if(ev.target===lb) close(); });
    document.addEventListener('keydown',function(ev){ if(lb.hidden) return;
      if(ev.key==='Escape') close(); if(ev.key==='ArrowLeft') show(idx-1); if(ev.key==='ArrowRight') show(idx+1); });
  }
})();
