function toggle_vis(elem) {
    var yt_id = elem.id;
    var cntnt = document.querySelector('div[id*="'+yt_id+'"]');
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
