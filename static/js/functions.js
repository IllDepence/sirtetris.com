function js_init() {
    var toggles = document.querySelectorAll('a.vis-tggl');
    for(var i=0; i<toggles.length; i++) {
        var t = toggles[i];
        t.href = '';
        t.setAttribute('onclick', 'toggle_vis(this); return false;');
        }
    }
function toggle_vis(elem) {
    var yt_id = elem.id;
    var cntnt = document.querySelector('span[id*="'+yt_id+'"]');
    if(cntnt.className == "vis-off") {
        var ifr = document.createElement('iframe');
        ifr.width = 700;
        ifr.height = 436;
        ifr.frameBorder = 0;
        ifr.src = '//www.youtube.com/embed/'+yt_id;
        cntnt.appendChild(ifr);
        cntnt.className = "vis-on";
        }
    else {
        var ifr = cntnt.firstChild;
        cntnt.removeChild(ifr);
        cntnt.className = "vis-off";
        }
    }
document.addEventListener('DOMContentLoaded', function() { js_init(); }, false);
