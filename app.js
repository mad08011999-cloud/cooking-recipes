const $=s=>document.querySelector(s), esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const MOODS={rainy:['🌧️','Rainy / cozy evening'],weeknight:['⚡','Quick weeknight'],weekend:['🏡','Slow weekend cook'],brunch:['☀️','Weekend brunch'],movie:['🍿','Movie / game night'],party:['🎉','Guests & dinner party'],mealprep:['📦','Meal-prep Sunday'],gym:['💪','Post-workout'],latenight:['🌙','Late-night craving'],festive:['🪔','Festive / celebration'],sweet:['🍫','Sweet-treat baking day']};
const CAT_ORDER=['Breakfast','Entree','Snack','Main Course','Side Dish','Dessert','Beverage'];
const CAT_LABEL={'Entree':'Entrée / Starter','Main Course':'Main Course','Side Dish':'Side Dish','Breakfast':'Breakfast','Snack':'Snack','Dessert':'Dessert','Beverage':'Beverage'};
const CAT_GRAD={'Breakfast':['#ffd36e','#ff9f43'],'Entree':['#ff8a5b','#d63031'],'Snack':['#fdcb6e','#e17055'],'Main Course':['#e17055','#8e2d10'],'Side Dish':['#a8e6a1','#2f9e5b'],'Dessert':['#c49bff','#6c3483'],'Beverage':['#81ecec','#0984e3']};
const DIETS=['Vegetarian','Vegan','Eggetarian','Pescatarian','Non-veg'];
const EMOJI=[[/lava|chocolate|alfajor/i,'🍫'],[/biryani/i,'🍛'],[/fried rice|jeera rice/i,'🍚'],[/burrito|bowl/i,'🥙'],[/al pastor|wrap/i,'🌯'],[/sandwich|toastie|chivito|club/i,'🥪'],[/burger|maggi/i,'🍔'],[/garlic bread/i,'🥖'],[/pasta/i,'🍝'],[/noodle|frankie/i,'🍜'],[/salad/i,'🥗'],[/potato/i,'🥔'],[/bread|omelette/i,'🍳'],[/fish/i,'🐟'],[/spring roll/i,'🥢'],[/tofu|soya/i,'🌶️'],[/paneer/i,'🧀'],[/popcorn|fried chicken|65/i,'🍗'],[/tikka|tandoori/i,'🍢'],[/curry|masala|butter chicken|manchurian/i,'🍲'],[/chicken/i,'🍗']];
const emo=r=>(EMOJI.find(([re])=>re.test(r.name))||[0,'🍽️'])[1];
const store=JSON.parse(localStorage.getItem('cookbook')||'{"fav":{},"cooked":{}}');store.ts=store.ts||{};
const save=()=>localStorage.setItem('cookbook',JSON.stringify(store));
let ALL=[], st={q:'',cat:'all',cuisine:'all',diet:'all',time:'all',kcal:'all',data:'full',sort:'best',moods:new Set(),tags:new Set()};
const cuisineGroup=c=>c.replace(/\s*\(.*\)/,'').replace(/-inspired|-American| fusion/g,'').trim();
const dietOf=r=>DIETS.find(d=>r.tags.includes(d))||'Non-veg';
const n0=r=>!!(r.nutrition&&r.nutrition.kcal!=null);
const fmtTn=m=>m==null?'—':fmtT(m);
const fmtT=m=>m<60?m+' min':Math.floor(m/60)+' h'+(m%60?' '+m%60+' min':'');
const EST='<span class="est" title="Estimated — not from the source data">est.</span>';
const MODE={repo:['repo','From repo'],'repo-prev':['repo','From repo (earlier version)'],completed:['completed','Repo + filled in ★'],rewritten:['rewritten','Rewritten'],partial:['partial','Partial in repo'],check:['check','Check: steps may be mixed'],missing:['missing','Recipe missing in repo']};
const FULL=new Set(['repo','repo-prev','completed','rewritten']),RANK={repo:0,'repo-prev':1,completed:2,rewritten:3,check:4,partial:5,missing:6};
const PAGE=48;let shown=PAGE;
const srcTag=s=>s==='from post'?'<span class="est" style="color:var(--acc2)" title="Stated in the original post">from post</span>':EST;
function toast(m){const t=$('#toast');t.textContent=m;t.classList.add('show');clearTimeout(t._t);t._t=setTimeout(()=>t.classList.remove('show'),1800)}
function picHTML(r,cls){const g=CAT_GRAD[r.category]||['#ddd','#999'];
  return `<div class="${cls}" style="background:linear-gradient(135deg,${g[0]},${g[1]})"><span class="emo">${emo(r)}</span>${r.image?`<img loading="lazy" src="${esc(r.image)}/preview" onerror="if(!this.dataset.f){this.dataset.f=1;this.src='${esc(r.image)}'}else this.remove()" alt="${esc(r.name)}">`:''}`}
function filtered(){const q=st.q.trim().toLowerCase();
  let L=ALL.filter(r=>{
    if(st.cat==='fav')return store.fav[r.id]; if(st.cat==='cooked')return store.cooked[r.id];
    if(st.cat!=='all'&&r.category!==st.cat)return false;
    if(st.data==='full'&&!FULL.has(r.status))return false; if(st.data==='repo'&&!['repo','repo-prev'].includes(r.status))return false;
    if(st.data==='partial'&&!['partial','check'].includes(r.status))return false; if(st.data==='missing'&&r.status!=='missing')return false;
    if(st.cuisine!=='all'&&cuisineGroup(r.cuisine)!==st.cuisine)return false;
    if(st.diet!=='all'&&dietOf(r)!==st.diet)return false;
    if(st.time!=='all'){const t=+st.time;if(r.total==null)return false;if(t===999?r.total<=60:r.total>t)return false}
    if(st.kcal!=='all'){const[a,b]=st.kcal.split('-').map(Number);if(!n0(r))return false;if(r.nutrition.kcal<a||r.nutrition.kcal>=b)return false}
    for(const m of st.moods)if(!r.moods.includes(m))return false;
    for(const t of st.tags)if(!r.tags.includes(t))return false;
    if(q){const hay=[r.name,r.repo_name,r.cuisine,r.category,r.tags.join(' '),r.ingredients.map(i=>i[1]).join(' '),(r.origin&&r.origin.place)||''].join(' ').toLowerCase();if(!q.split(/\s+/).every(w=>hay.includes(w)))return false}
    return true});
  const S={best:(a,b)=>(RANK[a.status]>=4)-(RANK[b.status]>=4)||b.saved-a.saved,saved:(a,b)=>b.saved-a.saved,quick:(a,b)=>(a.total??999)-(b.total??999),light:(a,b)=>(n0(a)?a.nutrition.kcal:1e4)-(n0(b)?b.nutrition.kcal:1e4),protein:(a,b)=>(n0(b)?b.nutrition.protein:-1)-(n0(a)?a.nutrition.protein:-1),az:(a,b)=>a.name.localeCompare(b.name)};
  return L.sort(S[st.sort]);}
function card(r){const m=MODE[r.status];return `<article class="card ${r.status==='missing'?'missing':''}" data-id="${r.id}" tabindex="0">${picHTML(r,'pic')}
  <span class="badge">${esc(CAT_LABEL[r.category]||r.category)}</span><button class="fav" data-fav="${r.id}" title="Save">${store.fav[r.id]?'❤️':'🤍'}</button>
  <div class="stats">${r.total!=null?`<span>⏱ ${r.time_source==='from post'?'':'~'}${fmtT(r.total)}</span>`:''}${n0(r)?`<span>🔥 ${r.kcal_source==='from post'?'':'~'}${r.nutrition.kcal} kcal</span>`:''}${store.cooked[r.id]?'<span>✅ cooked</span>':''}</div></div>
  <div class="body"><div class="t">${esc(r.name)}</div><div class="s">${esc(r.cuisine)} · ${esc(dietOf(r))} · ${esc(r.difficulty)}</div>
  <div class="s">${r.origin?'📍 '+esc(r.origin.place):''} <span class="mode ${m[0]}">${m[1]}</span></div>
  <div class="mm">${r.moods.slice(0,3).map(m=>`<span>${MOODS[m][0]} ${MOODS[m][1]}</span>`).join('')}</div></div></article>`}
function render(){const L=filtered();
  $('#more').style.display=L.length>shown?'':'none';
  $('#grid').innerHTML=L.length?L.slice(0,shown).map(card).join(''):'<div class="empty">No recipes match these filters. <button class="btn" onclick="resetAll()">Reset filters</button></div>';
  $('#info').textContent=`${L.length} of ${ALL.length} dishes match`+(L.length>shown?` · showing ${shown}`:'')+` · ${ALL.filter(r=>FULL.has(r.status)).length} have a full recipe · ~ = estimate`;
  document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('on',t.dataset.c===st.cat));
  document.querySelectorAll('#moods .chip').forEach(c=>c.classList.toggle('on',st.moods.has(c.dataset.m)));
  document.querySelectorAll('#tags .chip').forEach(c=>c.classList.toggle('on',st.tags.has(c.dataset.t)));}
function tabs(){const n=c=>ALL.filter(r=>r.category===c).length;
  $('#tabs').innerHTML=`<button class="tab" data-c="all">All<small>${ALL.length}</small></button>`+CAT_ORDER.filter(n).map(c=>`<button class="tab" data-c="${c}">${CAT_LABEL[c]}<small>${n(c)}</small></button>`).join('')
   +`<button class="tab" data-c="fav">❤️ Saved<small>${Object.keys(store.fav).length}</small></button><button class="tab" data-c="cooked">✅ Cooked<small>${Object.keys(store.cooked).length}</small></button>`;}
function bar(lbl,v,unit,max,col){return `<div class="nb"><span>${lbl}</span><div class="bar"><i style="width:${Math.min(100,v/max*100)}%;background:${col}"></i></div><b>${v}${unit}</b></div>`}
function detail(id){const r=ALL.find(x=>x.id===id); if(!r)return; const n=r.nutrition,o=r.origin,m=MODE[r.status];
  const sentences=(t,k)=>{const s=(t||'').match(/[^.!?]+[.!?]+(\s|$)/g)||[t||''];return s.slice(0,k).join('').trim()};
  const oimg=o&&o.image?`<figure><img src="${esc(o.image.src)}" alt="${esc(o.place_title)}" loading="lazy"><figcaption>${esc(o.place_title)} · photo: ${esc(o.image.artist||'Wikimedia Commons')} · <a href="${esc(o.image.file_page)}" target="_blank" rel="noopener">${esc(o.image.license)}</a> via Wikimedia Commons</figcaption></figure>`:'<figure></figure>';
  const isCuisine=o&&/cuisine/i.test(o.dish_title||'');
  const originHTML=o?`<section class="origin">${oimg}<div class="ot"><span class="pill">🌍 Where it comes from</span><h3>${esc(o.place)}</h3>${o.place_desc?`<div class="src">${esc(o.place_desc)}</div>`:''}
     ${o.dish_extract?`<p><b>${isCuisine?'About '+esc(o.dish_title):esc(o.dish_title)}:</b> ${esc(sentences(o.dish_extract,3))}</p>`:''}
     <p><b>About ${esc(o.place_title)}:</b> ${esc(sentences(o.place_extract,2))}</p>
     ${r.fact?`<p>💡 <b>Good to know:</b> ${esc(r.fact)}</p>`:''}
     <div class="src">${o.basis&&o.basis!=='cuisine'?'Matched from the dish name. ':o.basis==='cuisine'?'Matched from the cuisine. ':''}Sources: ${o.dish_url?`<a href="${esc(o.dish_url)}" target="_blank" rel="noopener">Wikipedia — ${esc(o.dish_title)}</a> · `:''}<a href="${esc(o.place_url)}" target="_blank" rel="noopener">Wikipedia — ${esc(o.place_title)}</a> (text CC BY-SA 4.0)</div></div></section>`
     :`<div class="miss">🌍 The dish’s place of origin couldn’t be identified from its name or the repo’s cuisine field.</div>`;
  const yt=`https://www.youtube.com/results?search_query=${encodeURIComponent(r.name+' recipe')}`;
  const ingHTML=r.ingredients.length?`<ul class="ing">${r.ingredients.map(([q,i,h])=>h?`<li style="cursor:default;font-weight:700;border:0;padding-top:12px">${esc(i)}</li>`:`<li><span class="q">${esc(q||'—')}</span><span>${esc(i)}</span></li>`).join('')}</ul>`:'<div class="miss">No ingredient list in the repo.</div>';
  const stepsHTML=r.steps.length?`<ol class="steps">${r.steps.map(s=>`<li>${esc(s)}</li>`).join('')}</ol>`:'<div class="miss">No usable steps in the repo.</div>';
  const other=r.other_steps&&r.other_steps.length?`<details class="warn"><summary>⚠️ The repo’s current steps for this entry (they don’t match the ingredients)</summary><ol>${r.other_steps.map(s=>`<li>${esc(s)}</li>`).join('')}</ol></details>`:'';
  const body=r.status==='missing'?`<div class="miss" style="text-align:left"><b>No recipe for this dish in the repo yet.</b> ${esc(r.note)}.<br><br>It’s listed because it’s in your saved collection (saved ${r.saved}×). <a class="btn" style="margin-top:10px" href="${yt}" target="_blank" rel="noopener">▶️ Find a video recipe on YouTube</a></div>`
   :`<div class="cols"><div class="sec">
     <h3>🧺 Ingredients <span class="s">(${r.ingredients.filter(x=>!x[2]).length}) · tap to tick off</span></h3>${ingHTML}
     <h3>🥗 Nutrition per serving</h3>
     <div class="nut">${bar('Calories',n.kcal,'',900,'#e8590c')}${bar('Protein',n.protein,' g',60,'#2f9e5b')}${bar('Carbs',n.carbs,' g',100,'#d18a00')}${bar('Fat',n.fat,' g',50,'#c2255c')}${bar('Fibre',n.fiber,' g',15,'#1c7ed6')}</div>
     <p class="src">Calories: ${r.kcal_source==='from post'?'stated in the post':'estimate'} ${srcTag(r.kcal_source)} · protein/carbs/fat: ${r.macro_source==='from post'?'from the post':r.macro_source==='mixed'?'partly from the post, rest estimated':'rough estimate'} ${srcTag(r.macro_source==='from post'?'from post':'estimated')} · fibre ${EST}</p>
     <h3>🛋️ Best comfy times to cook ${EST}</h3>
     <div class="moods">${r.moods.map(x=>`<span>${MOODS[x][0]} ${MOODS[x][1]}</span>`).join('')}</div>
     <p class="src">Repo suggestion: “${esc(r.best_time)}”</p>
   </div><div class="sec">
     <h3>👩‍🍳 Step by step <span class="s">· tap a step when done</span></h3>${stepsHTML}${other}
   </div></div>`;
  $('#detBody').innerHTML=`<div class="hero" style="background:linear-gradient(135deg,${(CAT_GRAD[r.category]||['#ddd','#999']).join(',')})"><span class="emo">${emo(r)}</span>${r.image?`<img src="${esc(r.image)}" alt="${esc(r.name)}" onerror="this.remove()">`:''}
   <div class="ht"><span class="badge" style="position:static;display:inline-block;margin-bottom:8px">${esc(CAT_LABEL[r.category]||r.category)}</span><h2>${esc(r.name)}</h2><div class="s">${esc(r.cuisine)}${r.cuisine_inferred?' (inferred)':''}${o?' · 📍 '+esc(o.place):''}${r.repo_name!==r.name?` · saved as “${esc(r.repo_name)}”`:''}</div>
   <div class="tagl">${r.tags.map(t=>`<span>${esc(t)}</span>`).join('')}</div></div></div>
  <div class="db">
   <div class="kv">${r.prep!=null?`<div><small>Prep ${EST}</small><b>${fmtT(r.prep)}</b></div><div><small>Cook ${EST}</small><b>${fmtT(r.cook)}</b></div>`:''}<div><small>Total time ${r.total!=null?srcTag(r.time_source):''}</small><b>${fmtTn(r.total)}</b>${r.extra?`<span class="s">${esc(r.extra)}</span>`:''}</div>
   <div><small>Serves ${r.serv_source==='from recipe'?'<span class="est" style="color:var(--acc2)" title="Stated in the recipe steps">from recipe</span>':EST}</small><b>${r.servings??'—'}</b></div><div><small>Difficulty ${r.difficulty!=='—'?EST:''}</small><b>${esc(r.difficulty)}</b></div><div><small>Calories ${n0(r)?srcTag(r.kcal_source):''}</small><b>${n0(r)?n.kcal+' kcal':'—'}</b><span class="s">${n0(r)?'per serving':'no recipe to base it on'}</span></div></div>
   <div class="actions"><button class="btn ${store.fav[r.id]?'on':''}" data-dfav="${r.id}">${store.fav[r.id]?'❤️ Saved':'🤍 Save'}</button><button class="btn ${store.cooked[r.id]?'on':''}" data-dcook="${r.id}">${store.cooked[r.id]?'✅ Cooked it':'🍳 Mark as cooked'}</button>${r.youtube?`<a class="btn" href="${esc(r.youtube)}" target="_blank" rel="noopener">▶️ Video (YouTube)</a>`:''}<button class="btn" data-share="${r.id}">🔗 Copy link</button></div>
   <div class="note"><span class="mode ${m[0]}">${m[1]}</span> ${esc(r.note||(r.status==='repo'?'Ingredients and steps are exactly as in the repo (lightly cleaned).':''))}
      <table class="rd"><tr><td>Repo name</td><td>${esc(r.repo_name)}</td></tr><tr><td>Repo category${r.repo_category!==r.category?' (re-checked → '+esc(CAT_LABEL[r.category]||r.category)+')':''}</td><td>${esc(r.repo_category)}</td></tr><tr><td>Repo cuisine</td><td>${esc(r.repo_cuisine||'— (not set)')}</td></tr>
      <tr><td>Repo recipe source</td><td>${esc(r.recipe_source)}${r.mealdb?' · TheMealDB “'+esc(r.mealdb)+'”':''}</td></tr><tr><td>Times saved</td><td>${r.saved}</td></tr>${r.post_macros&&r.post_macros.length?`<tr><td>Nutrition line in post</td><td>${esc(r.post_macros.join(' · '))}</td></tr>`:''}</table></div>
   ${r.status==='check'?`<div class="warn">⚠️ ${esc(r.note)}</div>`:''}
   ${body}
   ${originHTML}
  </div>`;
  const d=$('#det'); if(!d.open)d.showModal(); d.scrollTop=0; history.replaceState(null,'','#'+r.id);}
function resetAll(){st={...st,q:'',cat:'all',cuisine:'all',diet:'all',time:'all',kcal:'all',data:'all',moods:new Set(),tags:new Set()};['q','cuisine','diet','time','kcal','data'].forEach(k=>$('#'+k).value=st[k]);shown=PAGE;render()}
window.resetAll=resetAll;
function toggle(kind,id){if(store[kind][id])delete store[kind][id];else store[kind][id]=Date.now();store.ts[id]=new Date().toISOString();save();tabs();render();window.cloudPush&&cloudPush(id)}
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
  $('#q').oninput=e=>{st.q=e.target.value;shown=PAGE;render()};
  ['cuisine','diet','time','kcal','sort','data'].forEach(k=>$('#'+k).onchange=e=>{st[k]=e.target.value;shown=PAGE;render()});
  $('#more').onclick=()=>{shown+=PAGE;render()};
  $('#tabs').onclick=e=>{const t=e.target.closest('.tab');if(t){st.cat=t.dataset.c;if(['fav','cooked'].includes(st.cat)){st.data='all';$('#data').value='all'}shown=PAGE;render()}};
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

// ---- Account sync (same Supabase project & auth setup as the movie site) ----
(function(){
const SB_URL="https://mazrqepjgdtdraxpcptk.supabase.co",SB_KEY="sb_publishable_-2do3uyVQ4kcl7PfnBeDpw_mWEc7TXN",SITE="https://mad08011999-cloud.github.io/cooking-recipes/";
const sb=window.supabase?window.supabase.createClient(SB_URL,SB_KEY):null;let user=null,cloudOK=true;
const sync=m=>{$('#sync').textContent=m;const e=$('#syncM');if(e)e.textContent=m};
const row=id=>({user_id:user.id,recipe_id:id,saved:!!store.fav[id],cooked:!!store.cooked[id],updated_at:store.ts[id]||new Date().toISOString()});
function fail(e){console.error(e);if(/recipe_status|PGRST205|42P01|schema cache|does not exist/i.test((e&&(e.message||e.code))||'')){cloudOK=false;sync('Signed in · account sync not set up yet — saved in this browser')}else sync('⚠️ Sync failed – will retry')}
async function pushIds(ids){if(!sb||!user||!cloudOK||!ids.length)return;sync('⏳ Saving…');
  try{const up=ids.filter(id=>store.fav[id]||store.cooked[id]).map(row),del=ids.filter(id=>!store.fav[id]&&!store.cooked[id]);
    if(up.length){const{error}=await sb.from('recipe_status').upsert(up,{onConflict:'user_id,recipe_id'});if(error)throw error}
    if(del.length){const{error}=await sb.from('recipe_status').delete().eq('user_id',user.id).in('recipe_id',del);if(error)throw error}
    sync('☁️ Synced to your account')}catch(e){fail(e)}}
window.cloudPush=id=>pushIds([id]);
async function load(){if(!sb||!user)return;sync('⏳ Loading your saved recipes…');
  const{data,error}=await sb.from('recipe_status').select('recipe_id,saved,cooked,updated_at');if(error)return fail(error);cloudOK=true;
  const remote={};data.forEach(r=>remote[r.recipe_id]=r);const mk='cb_merged_'+user.id,first=!localStorage.getItem(mk),toPush=[];
  const ids=new Set([...Object.keys(remote),...Object.keys(store.fav),...Object.keys(store.cooked)]);
  ids.forEach(id=>{const r=remote[id],lt=store.ts[id]||'';
    if(r&&(!lt||r.updated_at>=lt||!first)){r.saved?store.fav[id]=store.fav[id]||Date.parse(r.updated_at):delete store.fav[id];r.cooked?store.cooked[id]=store.cooked[id]||Date.parse(r.updated_at):delete store.cooked[id];store.ts[id]=r.updated_at}
    else if(!r&&first)toPush.push(id)
    else if(!r&&!first){delete store.fav[id];delete store.cooked[id]}
    else toPush.push(id)});
  localStorage.setItem(mk,'1');save();tabs();render();await pushIds(toPush);if(cloudOK)sync('☁️ Synced to your account')}
let mode='in';
const show=(el,t,good)=>{el.textContent=t;el.className='msg show '+(good?'good':'bad')},hide=el=>el.className='msg';
const friendly=e=>{const m=(e&&e.message||String(e)).toLowerCase();
  if(m.includes('provider is not enabled')||m.includes('unsupported provider'))return"Google sign-in isn't switched on yet. Please use email for now.";
  if(m.includes('invalid login'))return"That email and password don't match. Try again or reset your password.";
  if(m.includes('email not confirmed'))return'Please confirm your email first — check your inbox for the confirmation link.';
  if(m.includes('already registered'))return'An account with this email already exists. Try signing in instead.';
  if(m.includes('rate limit')||m.includes('too many'))return'Too many attempts. Please wait a minute and try again.';
  if(m.includes('password should be')||m.includes('weak'))return'Password is too weak — use at least 6 characters.';
  if(m.includes('failed to fetch')||m.includes('network'))return"Can't reach the server. Check your connection.";
  return e.message||'Something went wrong. Please try again.'};
const emOk=v=>/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
const busy=(b,on,t)=>{b.disabled=on;if(on){b._t=b.innerHTML;b.textContent=t||'Please wait…'}else if(b._t)b.innerHTML=b._t};
function setMode(m){mode=m;document.querySelectorAll('#auth .seg button').forEach(b=>b.classList.toggle('on',b.dataset.m===m));
  $('#aTitle').textContent=m==='in'?'Welcome back':'Create your account';$('#aSub').textContent=m==='in'?'Sign in':'Create account';
  $('#aPw').autocomplete=m==='in'?'current-password':'new-password';$('#forgot').style.visibility=m==='in'?'':'hidden';hide($('#msg'));$('#eEm').textContent=$('#ePw').textContent=''}
function openAuth(rec){$('#aMain').style.display=rec?'none':'';$('#aRec').style.display=rec?'':'none';if(!rec)setMode(mode);$('#auth').showModal()}
function authUI(){const b=$('#authBox');
  if(!sb){b.innerHTML='';sync('Saved in this browser');return}
  if(user){const md=user.user_metadata||{},nm=md.full_name||md.name||'',pic=md.avatar_url||md.picture||'',ini=esc((nm||user.email||'?')[0].toUpperCase());
    b.innerHTML=`<div class="acct"><button class="btn" id="acctBtn" style="padding:4px 10px 4px 4px"><span class="av" ${pic?`style="background-image:url('${esc(pic)}')"`:''}>${pic?'':ini}</span><span class="s" style="max-width:150px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${esc(nm||user.email)}</span>▾</button>
    <div class="menu" id="acctMenu">${nm?`<b>${esc(nm)}</b><br>`:''}<span class="s">${esc(user.email||'')}</span><p class="hint" id="syncM" style="margin:8px 0">${esc($('#sync').textContent)}</p><button class="btn wide" id="out">Sign out</button></div></div>`;
    $('#acctBtn').onclick=()=>$('#acctMenu').classList.toggle('open');$('#out').onclick=async()=>{await sb.auth.signOut();toast('Signed out')}}
  else{b.innerHTML='<button class="btn acc" id="in">Sign in</button>';sync('Saved in this browser');$('#in').onclick=()=>openAuth(false)}}
if(sb){
  document.querySelectorAll('#auth .seg button').forEach(b=>b.onclick=()=>setMode(b.dataset.m));
  $('#authX').onclick=()=>$('#auth').close();
  $('#pwT').onclick=()=>{const p=$('#aPw').type==='password';$('#aPw').type=p?'text':'password';$('#pwT').textContent=p?'Hide':'Show'};
  $('#gBtn').onclick=async()=>{hide($('#msg'));busy($('#gBtn'),true,'Redirecting to Google…');
    try{let en=true;try{const r=await fetch(SB_URL+'/auth/v1/settings',{headers:{apikey:SB_KEY}});if(r.ok)en=!!(await r.json()).external?.google}catch(_){}
      if(!en)throw new Error('provider is not enabled');const{error}=await sb.auth.signInWithOAuth({provider:'google',options:{redirectTo:SITE}});if(error)throw error}catch(e){show($('#msg'),friendly(e));busy($('#gBtn'),false)}};
  $('#aForm').onsubmit=async e=>{e.preventDefault();hide($('#msg'));const em=$('#aEm').value.trim(),pw=$('#aPw').value;let bad=false;
    if(!emOk(em)){$('#eEm').textContent='Enter a valid email address.';bad=true}
    if(pw.length<6){$('#ePw').textContent=pw?'Password must be at least 6 characters.':'Enter your password.';bad=true}
    if(bad)return;const b=$('#aSub');busy(b,true);
    try{if(mode==='in'){const{error}=await sb.auth.signInWithPassword({email:em,password:pw});if(error)throw error;$('#auth').close();toast('Signed in ✓')}
      else{const{data,error}=await sb.auth.signUp({email:em,password:pw,options:{emailRedirectTo:SITE}});if(error)throw error;
        if(data.user&&data.user.identities&&data.user.identities.length===0)throw new Error('already registered');
        if(data.session){$('#auth').close();toast('Account created ✓')}else show($('#msg'),'Almost there! Check your inbox to confirm your email, then sign in.',true)}}
    catch(x){show($('#msg'),friendly(x))}busy(b,false)};
  $('#forgot').onclick=async()=>{const em=$('#aEm').value.trim();if(!emOk(em)){$('#eEm').textContent='Enter your email above, then click Forgot password.';return}
    const{error}=await sb.auth.resetPasswordForEmail(em,{redirectTo:SITE});error?show($('#msg'),friendly(error)):show($('#msg'),'Password reset link sent — check your email.',true)};
  $('#magic').onclick=async()=>{const em=$('#aEm').value.trim();if(!emOk(em)){$('#eEm').textContent='Enter your email above to get a sign-in link.';return}
    const{error}=await sb.auth.signInWithOtp({email:em,options:{emailRedirectTo:SITE}});error?show($('#msg'),friendly(error)):show($('#msg'),'Sign-in link sent — check your email.',true)};
  $('#aRec').onsubmit=async e=>{e.preventDefault();const pw=$('#nPw').value;if(pw.length<6){$('#eN').textContent='At least 6 characters.';return}
    const{error}=await sb.auth.updateUser({password:pw});if(error)show($('#msg2'),friendly(error));else{$('#auth').close();toast('Password updated ✓')}};
  document.addEventListener('click',e=>{const m=$('#acctMenu');if(m&&!e.target.closest('.acct'))m.classList.remove('open')});
  sb.auth.onAuthStateChange((ev,s)=>{const nu=s?.user||null,changed=(nu?.id)!==(user?.id);user=nu;authUI();if(nu&&changed)setTimeout(load,300);if(ev==='PASSWORD_RECOVERY')setTimeout(()=>openAuth(true),0)});
}
authUI();
})();
