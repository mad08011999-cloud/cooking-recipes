const $=s=>document.querySelector(s), esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const MOODS={rainy:['🌧️','Rainy / cozy evening'],weeknight:['⚡','Quick weeknight'],weekend:['🏡','Slow weekend cook'],brunch:['☀️','Weekend brunch'],movie:['🍿','Movie / game night'],party:['🎉','Guests & dinner party'],mealprep:['📦','Meal-prep Sunday'],gym:['💪','Post-workout'],latenight:['🌙','Late-night craving'],festive:['🪔','Festive / celebration'],sweet:['🍫','Sweet-treat baking day']};
const CAT_ORDER=['Breakfast','Entree','Snack','Main Course','Side Dish','Dessert'];
const CAT_LABEL={'Entree':'Entrée / Starter','Main Course':'Main Course','Side Dish':'Side Dish','Breakfast':'Breakfast','Snack':'Snack','Dessert':'Dessert'};
const CAT_GRAD={'Breakfast':['#ffd36e','#ff9f43'],'Entree':['#ff8a5b','#d63031'],'Snack':['#fdcb6e','#e17055'],'Main Course':['#e17055','#8e2d10'],'Side Dish':['#a8e6a1','#2f9e5b'],'Dessert':['#c49bff','#6c3483']};
const DIETS=['Vegetarian','Vegan','Eggetarian','Pescatarian','Non-veg'];
const EMOJI=[[/lava|chocolate|alfajor/i,'🍫'],[/biryani/i,'🍛'],[/fried rice|jeera rice/i,'🍚'],[/burrito|bowl/i,'🥙'],[/al pastor|wrap/i,'🌯'],[/sandwich|toastie|chivito|club/i,'🥪'],[/burger|maggi/i,'🍔'],[/garlic bread/i,'🥖'],[/pasta/i,'🍝'],[/noodle|frankie/i,'🍜'],[/salad/i,'🥗'],[/potato/i,'🥔'],[/bread|omelette/i,'🍳'],[/fish/i,'🐟'],[/spring roll/i,'🥢'],[/tofu|soya/i,'🌶️'],[/paneer/i,'🧀'],[/popcorn|fried chicken|65/i,'🍗'],[/tikka|tandoori/i,'🍢'],[/curry|masala|butter chicken|manchurian/i,'🍲'],[/chicken/i,'🍗']];
const emo=r=>(EMOJI.find(([re])=>re.test(r.name))||[0,'🍽️'])[1];
const store=JSON.parse(localStorage.getItem('cookbook')||'{"fav":{},"cooked":{}}');
const save=()=>localStorage.setItem('cookbook',JSON.stringify(store));
let ALL=[], st={q:'',cat:'all',cuisine:'all',diet:'all',time:'all',kcal:'all',sort:'saved',moods:new Set(),tags:new Set()};
const cuisineGroup=c=>c.replace(/\s*\(.*\)/,'').replace(/-inspired|-American| fusion/g,'').trim();
const dietOf=r=>DIETS.find(d=>r.tags.includes(d))||'Non-veg';
const fmtT=m=>m<60?m+' min':Math.floor(m/60)+' h'+(m%60?' '+m%60+' min':'');
const EST='<span class="est" title="Estimated — not from the source data">est.</span>';
const MODE={repo:['repo','From repo'],completed:['completed','Repo + filled in ★'],rewritten:['rewritten','Rewritten']};
function toast(m){const t=$('#toast');t.textContent=m;t.classList.add('show');clearTimeout(t._t);t._t=setTimeout(()=>t.classList.remove('show'),1800)}
function picHTML(r,cls){const g=CAT_GRAD[r.category]||['#ddd','#999'];
  return `<div class="${cls}" style="background:linear-gradient(135deg,${g[0]},${g[1]})"><span class="emo">${emo(r)}</span>${r.image?`<img loading="lazy" src="${esc(r.image)}/preview" onerror="if(!this.dataset.f){this.dataset.f=1;this.src='${esc(r.image)}'}else this.remove()" alt="${esc(r.name)}">`:''}`}
function filtered(){const q=st.q.trim().toLowerCase();
  let L=ALL.filter(r=>{
    if(st.cat==='fav')return store.fav[r.id]; if(st.cat==='cooked')return store.cooked[r.id];
    if(st.cat!=='all'&&r.category!==st.cat)return false;
    if(st.cuisine!=='all'&&cuisineGroup(r.cuisine)!==st.cuisine)return false;
    if(st.diet!=='all'&&dietOf(r)!==st.diet)return false;
    if(st.time!=='all'){const t=+st.time;if(t===999?r.total<=60:r.total>t)return false}
    if(st.kcal!=='all'){const[a,b]=st.kcal.split('-').map(Number);if(r.nutrition.kcal<a||r.nutrition.kcal>=b)return false}
    for(const m of st.moods)if(!r.moods.includes(m))return false;
    for(const t of st.tags)if(!r.tags.includes(t))return false;
    if(q){const hay=[r.name,r.repo.name,r.cuisine,r.category,r.tags.join(' '),r.ingredients.map(i=>i[1]).join(' '),r.origin.place||''].join(' ').toLowerCase();if(!q.split(/\s+/).every(w=>hay.includes(w)))return false}
    return true});
  const S={saved:(a,b)=>b.saved-a.saved,quick:(a,b)=>a.total-b.total,light:(a,b)=>a.nutrition.kcal-b.nutrition.kcal,protein:(a,b)=>b.nutrition.protein-a.nutrition.protein,az:(a,b)=>a.name.localeCompare(b.name)};
  return L.sort(S[st.sort]);}
function card(r){return `<article class="card" data-id="${r.id}" tabindex="0">${picHTML(r,'pic')}
  <span class="badge">${esc(CAT_LABEL[r.category]||r.category)}</span><button class="fav" data-fav="${r.id}" title="Save">${store.fav[r.id]?'❤️':'🤍'}</button>
  <div class="stats"><span>⏱ ${fmtT(r.total)}</span><span>🔥 ${r.nutrition.kcal} kcal</span>${store.cooked[r.id]?'<span>✅ cooked</span>':''}</div></div>
  <div class="body"><div class="t">${esc(r.name)}</div><div class="s">${esc(r.cuisine)} · ${esc(dietOf(r))} · ${esc(r.difficulty)} · serves ${r.servings}</div>
  <div class="s">📍 ${esc(r.origin.place||'')}</div>
  <div class="mm">${r.moods.slice(0,3).map(m=>`<span>${MOODS[m][0]} ${MOODS[m][1]}</span>`).join('')}</div></div></article>`}
function render(){const L=filtered();
  $('#grid').innerHTML=L.length?L.map(card).join(''):'<div class="empty">No recipes match these filters. <button class="btn" onclick="resetAll()">Reset filters</button></div>';
  $('#info').textContent=`Showing ${L.length} of ${ALL.length} recipes · times & nutrition are estimates`;
  document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('on',t.dataset.c===st.cat));
  document.querySelectorAll('#moods .chip').forEach(c=>c.classList.toggle('on',st.moods.has(c.dataset.m)));
  document.querySelectorAll('#tags .chip').forEach(c=>c.classList.toggle('on',st.tags.has(c.dataset.t)));}
function tabs(){const n=c=>ALL.filter(r=>r.category===c).length;
  $('#tabs').innerHTML=`<button class="tab" data-c="all">All<small>${ALL.length}</small></button>`+CAT_ORDER.filter(n).map(c=>`<button class="tab" data-c="${c}">${CAT_LABEL[c]}<small>${n(c)}</small></button>`).join('')
   +`<button class="tab" data-c="fav">❤️ Saved<small>${Object.keys(store.fav).length}</small></button><button class="tab" data-c="cooked">✅ Cooked<small>${Object.keys(store.cooked).length}</small></button>`;}
function bar(lbl,v,unit,max,col){return `<div class="nb"><span>${lbl}</span><div class="bar"><i style="width:${Math.min(100,v/max*100)}%;background:${col}"></i></div><b>${v}${unit}</b></div>`}
function detail(id){const r=ALL.find(x=>x.id===id); if(!r)return; const n=r.nutrition,o=r.origin,m=MODE[r.mode];
  const post=[]; if(r.repo.post.kcal!=null)post.push(`${r.repo.post.kcal} kcal`); if(r.repo.post.time_min!=null)post.push(`${r.repo.post.time_min} min`);
  const oimg=o.image?`<figure><img src="${esc(o.image.src)}" alt="${esc(o.place_title)}" loading="lazy"><figcaption>${esc(o.place_title)} · photo: ${esc(o.image.artist||'Wikimedia Commons')} · <a href="${esc(o.image.file_page)}" target="_blank" rel="noopener">${esc(o.image.license)}</a> via Wikimedia Commons</figcaption></figure>`:'<figure></figure>';
  const sentences=(t,k)=>{const s=(t||'').match(/[^.!?]+[.!?]+(\s|$)/g)||[t||''];return s.slice(0,k).join('').trim()};
  $('#detBody').innerHTML=`<div class="hero" style="background:linear-gradient(135deg,${(CAT_GRAD[r.category]||['#ddd','#999']).join(',')})"><span class="emo">${emo(r)}</span>${r.image?`<img src="${esc(r.image)}" alt="${esc(r.name)}" onerror="this.remove()">`:''}
   <div class="ht"><span class="badge" style="position:static;display:inline-block;margin-bottom:8px">${esc(CAT_LABEL[r.category])}</span><h2>${esc(r.name)}</h2><div class="s">${esc(r.cuisine)} · 📍 ${esc(o.place||'')}${r.repo.name!==r.name?` · saved as “${esc(r.repo.name)}”`:''}</div>
   <div class="tagl">${r.tags.map(t=>`<span>${esc(t)}</span>`).join('')}</div></div></div>
  <div class="db">
   <div class="kv"><div><small>Prep ${EST}</small><b>${fmtT(r.prep)}</b></div><div><small>Cook ${EST}</small><b>${fmtT(r.cook)}</b></div><div><small>Total ${EST}</small><b>${fmtT(r.total)}</b>${r.extra?`<span class="s">${esc(r.extra)}</span>`:''}</div>
   <div><small>Serves ${EST}</small><b>${r.servings}</b></div><div><small>Difficulty ${EST}</small><b>${esc(r.difficulty)}</b></div><div><small>Calories ${EST}</small><b>${n.kcal} kcal</b><span class="s">per serving</span></div></div>
   <div class="actions"><button class="btn ${store.fav[r.id]?'on':''}" data-dfav="${r.id}">${store.fav[r.id]?'❤️ Saved':'🤍 Save'}</button><button class="btn ${store.cooked[r.id]?'on':''}" data-dcook="${r.id}">${store.cooked[r.id]?'✅ Cooked it':'🍳 Mark as cooked'}</button>${r.youtube?`<a class="btn" href="${esc(r.youtube)}" target="_blank" rel="noopener">▶️ Video (YouTube)</a>`:''}<button class="btn" data-share="${r.id}">🔗 Copy link</button></div>
   <div class="cols"><div class="sec">
     <h3>🧺 Ingredients <span class="s">(${r.ingredients.length}) · tap to tick off</span></h3>
     <ul class="ing">${r.ingredients.map(([q,i])=>`<li><span class="q">${esc(q||'—')}</span><span>${esc(i)}</span></li>`).join('')}</ul>
     <h3>🥗 Nutrition per serving ${EST}</h3>
     <div class="nut">${bar('Calories',n.kcal,'',900,'#e8590c')}${bar('Protein',n.protein,' g',60,'#2f9e5b')}${bar('Carbs',n.carbs,' g',100,'#d18a00')}${bar('Fat',n.fat,' g',50,'#c2255c')}${bar('Fibre',n.fiber,' g',15,'#1c7ed6')}</div>
     <p class="src">Rough estimate from the ingredients for ${r.servings} serving${r.servings>1?'s':''}; not lab-measured.${post.length?` The original post said: <b>${post.join(' · ')}</b>.`:''}</p>
     <h3>🛋️ Best comfy times to cook ${EST}</h3>
     <div class="moods">${r.moods.map(x=>`<span>${MOODS[x][0]} ${MOODS[x][1]}</span>`).join('')}</div>
     <p class="src">Repo suggestion: “${esc(r.repo.best_time)}”</p>
   </div><div class="sec">
     <h3>👩‍🍳 Step by step <span class="s">· tap a step when done</span></h3>
     <ol class="steps">${r.steps.map(s=>`<li>${esc(s)}</li>`).join('')}</ol>
     <div class="note"><span class="mode ${m[0]}">${m[1]}</span> ${esc(r.note)}
      <table class="rd"><tr><td>Repo name</td><td>${esc(r.repo.name)}</td></tr><tr><td>Repo category / cuisine</td><td>${esc(r.repo.category)} / ${esc(r.repo.cuisine||'—')}</td></tr>
      <tr><td>Repo time</td><td>${r.repo.time_min} min (${esc(r.repo.time_source)})</td></tr><tr><td>Repo calories</td><td>${r.repo.calories} kcal (${esc(r.repo.calories_source)})</td></tr>
      <tr><td>Repo recipe source</td><td>${esc(r.repo.source)} · ${r.repo.n_ing} ingredients, ${r.repo.n_steps} steps</td></tr><tr><td>Times saved</td><td>${r.saved}</td></tr></table></div>
   </div></div>
   <section class="origin">${oimg}<div class="ot"><span class="pill">🌍 Where it comes from</span><h3>${esc(o.place||'')}</h3>${o.place_desc?`<div class="src">${esc(o.place_desc)}</div>`:''}
     <p><b>${esc(o.dish_title)}:</b> ${esc(sentences(o.dish_extract,3))}</p>
     <p><b>About ${esc(o.place_title)}:</b> ${esc(sentences(o.place_extract,2))}</p>
     ${r.fact?`<p>💡 <b>Good to know:</b> ${esc(r.fact)}</p>`:''}
     <div class="src">Sources: <a href="${esc(o.dish_url)}" target="_blank" rel="noopener">Wikipedia — ${esc(o.dish_title)}</a> · <a href="${esc(o.place_url)}" target="_blank" rel="noopener">Wikipedia — ${esc(o.place_title)}</a> (text CC BY-SA 4.0)</div></div></section>
  </div>`;
  const d=$('#det'); if(!d.open)d.showModal(); d.scrollTop=0; history.replaceState(null,'','#'+r.id);}
function resetAll(){st={...st,q:'',cat:'all',cuisine:'all',diet:'all',time:'all',kcal:'all',moods:new Set(),tags:new Set()};['q','cuisine','diet','time','kcal'].forEach(k=>$('#'+k).value=st[k]);render()}
window.resetAll=resetAll;
function toggle(kind,id){if(store[kind][id])delete store[kind][id];else store[kind][id]=Date.now();save();tabs();render();}
async function init(){
  const th=localStorage.getItem('cbTheme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');document.documentElement.dataset.theme=th;
  const data=await (await fetch('recipes.json')).json(); ALL=data.recipes;
  $('#cnt').textContent=`${ALL.length} recipes`; $('#cnt2').textContent=ALL.length;
  const cz=[...new Set(ALL.map(r=>cuisineGroup(r.cuisine)))].sort(); $('#cuisine').innerHTML+=cz.map(c=>`<option>${esc(c)}</option>`).join('');
  $('#diet').innerHTML+=DIETS.filter(d=>ALL.some(r=>dietOf(r)===d)).map(d=>`<option>${d}</option>`).join('');
  const mc=m=>ALL.filter(r=>r.moods.includes(m)).length;
  $('#moods').innerHTML=Object.entries(MOODS).filter(([k])=>mc(k)).map(([k,[e,l]])=>`<button class="chip" data-m="${k}">${e} ${l}<small>${mc(k)}</small></button>`).join('');
  const tc={};ALL.forEach(r=>r.tags.filter(t=>!DIETS.includes(t)).forEach(t=>tc[t]=(tc[t]||0)+1));
  $('#tags').innerHTML=Object.entries(tc).sort((a,b)=>b[1]-a[1]).map(([t,c])=>`<button class="chip" data-t="${esc(t)}">${esc(t)}<small>${c}</small></button>`).join('');
  tabs(); render();
  $('#q').oninput=e=>{st.q=e.target.value;render()};
  ['cuisine','diet','time','kcal','sort'].forEach(k=>$('#'+k).onchange=e=>{st[k]=e.target.value;render()});
  $('#tabs').onclick=e=>{const t=e.target.closest('.tab');if(t){st.cat=t.dataset.c;render()}};
  $('#moods').onclick=e=>{const c=e.target.closest('.chip');if(!c)return;const m=c.dataset.m;st.moods.has(m)?st.moods.delete(m):st.moods.add(m);render()};
  $('#tags').onclick=e=>{const c=e.target.closest('.chip');if(!c)return;const t=c.dataset.t;st.tags.has(t)?st.tags.delete(t):st.tags.add(t);render()};
  $('#reset').onclick=resetAll;
  $('#grid').onclick=e=>{const f=e.target.closest('[data-fav]');if(f){e.stopPropagation();toggle('fav',f.dataset.fav);toast(store.fav[f.dataset.fav]?'Saved ❤️':'Removed');return}
    const c=e.target.closest('.card');if(c)detail(c.dataset.id)};
  $('#grid').onkeydown=e=>{if(e.key==='Enter'&&e.target.classList.contains('card'))detail(e.target.dataset.id)};
  $('#detBody').onclick=e=>{const li=e.target.closest('.ing li,.steps li');if(li){li.classList.toggle('done');return}
    const f=e.target.closest('[data-dfav]');if(f){toggle('fav',f.dataset.dfav);detail(f.dataset.dfav);return}
    const k=e.target.closest('[data-dcook]');if(k){toggle('cooked',k.dataset.dcook);detail(k.dataset.dcook);return}
    const s=e.target.closest('[data-share]');if(s){navigator.clipboard?.writeText(location.href.split('#')[0]+'#'+s.dataset.share);toast('Link copied')}};
  $('#detX').onclick=()=>$('#det').close(); $('#det').addEventListener('close',()=>history.replaceState(null,'',location.pathname));
  $('#det').onclick=e=>{if(e.target===$('#det'))$('#det').close()};
  $('#aboutBtn').onclick=()=>$('#about').showModal(); $('#aboutX').onclick=()=>$('#about').close(); $('#about').onclick=e=>{if(e.target===$('#about'))$('#about').close()};
  $('#themeBtn').onclick=()=>{const t=document.documentElement.dataset.theme==='dark'?'light':'dark';document.documentElement.dataset.theme=t;localStorage.setItem('cbTheme',t)};
  if(location.hash.length>1)detail(location.hash.slice(1));
}
init();
