'use strict';
const $ = id => document.getElementById(id);
try { document.documentElement.dataset.theme=localStorage.getItem('wiki-dash-theme')||'light'; } catch (_) {}
$('theme').onclick=()=>{const t=document.documentElement.dataset.theme==='dark'?'light':'dark';document.documentElement.dataset.theme=t;try{localStorage.setItem('wiki-dash-theme',t);}catch(_){}};
const routes={
vct:['Initial 4F² transition','Gain density from the cell architecture','A vertical access channel allows a more compact cell footprint. Density can improve without asking lithography to deliver the entire gain through a tighter pitch.','Potential breathing room, not EUV removal',['DUV and Low-NA EUV remain relevant.','UBS / Gaudois (14 Jan 2026): first-node lithography intensity may pause or fall.','ASML (28 Jan 2026): expects both immersion and EUV intensity to rise.'],'This scenario is the core disagreement between the broker baseline and the company view.'],
six:['Keep 6F² and shrink','Keep the architecture; tighten the pattern','Without the 4F² architectural reset, achieving a denser array relies more heavily on smaller features. This strengthens the need for demanding patterning.','High-NA becomes more relevant',['Low-NA multipatterning and High-NA are process alternatives on critical layers.','UBS APAC tour (22 Sep 2026): a 6F² path makes High-NA more likely at 0a.','The same checks say SK hynix had not made a final architecture choice.'],'A delayed 4F² transition does not automatically mean weaker lithography demand. This is a conditional interpretation of UBS checks.'],
later:['Later 4F² nodes','The architectural gain is not repeatable forever','Once the cell is already 4F², further density gains again require tighter features, further structural changes, or both.','Advanced patterning returns to the foreground',['UBS / Gaudois (14 Jan 2026): subsequent nodes need lithographic shrink and eventually High-NA.','The insertion point depends on integration, economics and vendor execution.','A vertical access transistor alone is not a many-tier 3D DRAM architecture.'],'This is a direction of travel, not a committed insertion date or scanner forecast.']
};
function route(k){const r=routes[k];$('scenario').innerHTML='<div><span class="eyebrow">'+r[0]+'</span><h3>'+r[1]+'</h3><p>'+r[2]+'</p><p class="note">Sources [1–4], linked below.</p></div><div><h3>'+r[3]+'</h3><ul>'+r[4].map(x=>'<li>'+x+'</li>').join('')+'</ul><p class="callout note">'+r[5]+'</p></div>';document.querySelectorAll('[data-route]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.route===k)));}
document.querySelectorAll('[data-route]').forEach(b=>b.onclick=()=>route(b.dataset.route));route('vct');
try {
if(!window.THREE)throw Error('3D library unavailable');
const T=THREE, canvas=$('scene'),renderer=new T.WebGLRenderer({canvas,antialias:true,alpha:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.outputEncoding=T.sRGBEncoding;renderer.toneMapping=T.ACESFilmicToneMapping;
const scene=new T.Scene(),camera=new T.PerspectiveCamera(35,1,.1,100),root=new T.Group();scene.add(root);
scene.add(new T.HemisphereLight(0xffffff,0x506077,.85));const light=new T.DirectionalLight(0xffffff,.8);light.position.set(1,8,6);scene.add(light);
const colors={base:0x8394a7,gate:0xdf8a35,bit:0x218bdb,cap:0x16a79b,dielectric:0xe2e8ef,charge:0xffd655};
const capParts=[],moving=[],paths=[];
function material(c){return new T.MeshStandardMaterial({color:c,roughness:.42,metalness:.18});}
function box(g,w,h,d,x,y,z,c){let o=new T.Mesh(new T.BoxGeometry(w,h,d),material(c));o.position.set(x,y,z);g.add(o);return o;}
function cyl(g,r,h,x,y,z,c){let o=new T.Mesh(new T.CylinderGeometry(r,r,h,48),material(c));o.position.set(x,y,z);g.add(o);return o;}
function tube(g,pts,r,c){let curve=new T.CatmullRomCurve3(pts.map(p=>new T.Vector3(...p)));let o=new T.Mesh(new T.TubeGeometry(curve,60,r,10,false),material(c));g.add(o);return o;}
function movable(o,weight){moving.push({o,y:o.position.y,weight});return o;}
function capacitor(g,x,z){const group=new T.Group();group.position.set(x,2.35,z);g.add(group);cyl(group,.35,1.35,0,.55,0,colors.cap);cyl(group,.37,.07,0,1.25,0,colors.dielectric);cyl(group,.37,.07,0,-.12,0,colors.dielectric);capParts.push(group);movable(group,1.6);return group;}
function mark(g,text,x,y,z){const c=document.createElement('canvas');c.width=384;c.height=88;const ctx=c.getContext('2d');ctx.fillStyle='#f4f5f7';ctx.fillRect(0,0,384,88);ctx.fillStyle='#243247';ctx.font='bold 37px system-ui';ctx.textAlign='center';ctx.fillText(text,192,59);const s=new T.Sprite(new T.SpriteMaterial({map:new T.CanvasTexture(c)}));s.position.set(x,y,z);s.scale.set(1.8,.42,1);g.add(s);}
const left=new T.Group(),right=new T.Group();left.position.x=-2.45;right.position.x=2.45;root.add(left,right);
box(left,3,.35,2,0,0,0,colors.base);
box(left,.65,.45,.7,-1,.36,0,colors.base);box(left,.65,.45,.7,1,.36,0,colors.base);
tube(left,[[-1,.62,0],[-.7,.25,0],[0,.2,0],[.7,.25,0],[1,.62,0]],.15,colors.base);
box(left,1.45,.12,.78,0,.48,0,colors.dielectric);
movable(box(left,1.2,.3,.68,0,.7,0,colors.gate),.35);
box(left,.4,.55,.4,-1,.95,0,colors.bit);box(left,.4,.15,2.25,-1,1.18,0,colors.bit);
movable(cyl(left,.17,1.75,1,1.36,0,colors.base),.65);capacitor(left,1,0);
paths.push(tube(left,[[-1,.7,.29],[-.65,.32,.29],[0,.28,.29],[.7,.32,.29],[1,.7,.29]],.035,colors.charge));
mark(left,'3F × 2F',0,-.55,1.05);
box(right,2,.35,2,0,0,0,colors.base);
box(right,.4,.18,2.25,0,.3,0,colors.bit);
cyl(right,.18,1.95,0,1.24,0,colors.base);
const collar=new T.Mesh(new T.CylinderGeometry(.23,.23,.75,48,1,true),material(colors.dielectric));collar.position.y=1.05;right.add(collar);
const gate=new T.Mesh(new T.CylinderGeometry(.34,.34,.65,48,1,true,Math.PI/3,Math.PI*1.6),new T.MeshStandardMaterial({color:colors.gate,side:T.DoubleSide,metalness:.25,roughness:.4}));gate.position.y=1.05;right.add(gate);movable(gate,.35);
movable(box(right,1.7,.22,.22,-.7,1.05,-.12,colors.gate),.35);capacitor(right,0,0);
paths.push(tube(right,[[0,.43,.24],[0,1,.24],[0,1.95,.24]],.035,colors.charge));
mark(right,'2F × 2F',0,-.55,1.05);
let yaw=.12,pitch=.25,drag=false,lastX=0,lastY=0;
function view(v){if(v==='top'){yaw=0;pitch=1.1;}else if(v==='front'){yaw=0;pitch=-.17;}else{yaw=.12;pitch=.25;}draw();}
function draw(){const w=canvas.clientWidth,h=canvas.clientHeight;renderer.setSize(w,h,false);camera.aspect=w/h;camera.position.set(0,6,15);camera.lookAt(0,1.1,0);camera.updateProjectionMatrix();root.rotation.set(pitch,yaw,0);const aspect=w/h;camera.position.z=Math.max(11,4.7/(Math.tan(Math.PI*35/360)*aspect));camera.lookAt(0,1.1,0);renderer.render(scene,camera);}
document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>view(b.dataset.view));
canvas.onpointerdown=e=>{drag=true;lastX=e.clientX;lastY=e.clientY;canvas.setPointerCapture(e.pointerId);};
canvas.onpointermove=e=>{if(!drag)return;yaw+=(e.clientX-lastX)*.008;pitch=Math.max(-.45,Math.min(1.1,pitch+(e.clientY-lastY)*.007));lastX=e.clientX;lastY=e.clientY;draw();};
canvas.onpointerup=canvas.onpointercancel=()=>drag=false;
$('explode').oninput=()=>{const v=Number($('explode').value)/100;moving.forEach(({o,y,weight})=>o.position.y=y+weight*v);draw();};
$('capacitor').onchange=()=>{capParts.forEach(o=>o.visible=$('capacitor').checked);draw();};
$('charge').onchange=()=>{paths.forEach(o=>o.visible=$('charge').checked);draw();};
$('reset').onclick=()=>{$('explode').value=0;$('explode').oninput();$('capacitor').checked=true;$('capacitor').onchange();$('charge').checked=true;$('charge').onchange();view('angle');};
new ResizeObserver(draw).observe(canvas.parentElement);draw();
} catch(e){$('scene').style.display='none';$('fallback').style.display='block';document.querySelectorAll('.controls button,.controls input').forEach(b=>b.disabled=true);console.warn(e);}

