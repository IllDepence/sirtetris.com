function SingleBlock(x, y) {
    this.x = x;
    this.y = y;
    this.id = window.blockID;
    window.blockID++;
    this.elem = document.createElement('div');
    this.elem.id = 'singleblock'+this.id;
    this.elem.setAttribute('style', 'height: 10px; width: 10px;'+
       'background-color:#007f9a; position: absolute; top: '+this.y+'px;'+
        'right: '+(this.x+750)+'px; position: absolute; z-index: 90;');
    return this;
    }
SingleBlock.prototype.spawn = function() {
    document.body.appendChild(this.elem);
    }
SingleBlock.prototype.despawn = function() {
    document.body.removeChild(this.elem);
    }
SingleBlock.prototype.move = function(dx, dy) {
    var x = parseInt(this.elem.style.right.replace('px',''));
    var y = parseInt(this.elem.style.top.replace('px',''));
    this.x = (x+dx);
    this.y = (y+dy);
    this.elem.style.right = (this.x)+'px';
    this.elem.style.top = (this.y)+'px';
    }

function Piece(type, x, y) {
    this.x = x;
    this.y = y;
    this.rotation = 0;
    this.living = 1;
    this.blocks = [];
    this.type = type;
    switch(type) {
        case 0:     // T piece
            this.blocks.push(new SingleBlock(this.x, this.y-10));
            this.blocks.push(new SingleBlock(this.x+10, this.y));
            this.blocks.push(new SingleBlock(this.x, this.y));
            this.blocks.push(new SingleBlock(this.x-10, this.y));
            break;
        case 1:     // L piece
            this.blocks.push(new SingleBlock(this.x, this.y-10));
            this.blocks.push(new SingleBlock(this.x, this.y));
            this.blocks.push(new SingleBlock(this.x, this.y+10));
            this.blocks.push(new SingleBlock(this.x-10, this.y+10));
            break;
        case 2:     // J piece
            this.blocks.push(new SingleBlock(this.x, this.y-10));
            this.blocks.push(new SingleBlock(this.x, this.y));
            this.blocks.push(new SingleBlock(this.x, this.y+10));
            this.blocks.push(new SingleBlock(this.x+10, this.y+10));
            break;
        case 3:     // I piece
            this.blocks.push(new SingleBlock(this.x, this.y-10));
            this.blocks.push(new SingleBlock(this.x, this.y));
            this.blocks.push(new SingleBlock(this.x, this.y+10));
            this.blocks.push(new SingleBlock(this.x, this.y+20));
            break;
        case 4:     // Z piece
            this.blocks.push(new SingleBlock(this.x+10, this.y));
            this.blocks.push(new SingleBlock(this.x, this.y));
            this.blocks.push(new SingleBlock(this.x, this.y+10));
            this.blocks.push(new SingleBlock(this.x-10, this.y+10));
            break;
        case 5:     // S piece
            this.blocks.push(new SingleBlock(this.x-10, this.y));
            this.blocks.push(new SingleBlock(this.x, this.y));
            this.blocks.push(new SingleBlock(this.x, this.y+10));
            this.blocks.push(new SingleBlock(this.x+10, this.y+10));
            break;
        case 6:     // O piece
            this.blocks.push(new SingleBlock(this.x, this.y));
            this.blocks.push(new SingleBlock(this.x+10, this.y));
            this.blocks.push(new SingleBlock(this.x, this.y+10));
            this.blocks.push(new SingleBlock(this.x+10, this.y+10));
            break;
        }
    }
Piece.prototype.spawn = function() {
    for (var i=0; i<this.blocks.length; i++) {
        this.blocks[i].spawn();
        }
    }
Piece.prototype.despawn = function() {
    for (var i=0; i<this.blocks.length; i++) {
        this.blocks[i].despawn();
        }
    }
Piece.prototype.move = function(dx, dy) {
    if (this.checkCollision(dx, dy)) {
        return false;
        }
    for (var i=0; i<this.blocks.length; i++) {
        this.blocks[i].move(dx, dy);
        }
    this.x = this.x+dx;
    this.y = this.y+dy;
    return true;
    }
Piece.prototype.rotate = function() {
    if (this.y >= 100) return;
    for (var i=0; i<window.deadBlocks.length; i++) {
        for (var j=0; j<this.blocks.length; j++) {
            blockedx = window.deadBlocks[i].x;
            blockedy = window.deadBlocks[i].y;
            x = this.blocks[j].x;
            y = this.blocks[j].y;
            if (x-20 <= blockedx && x+20 >= blockedx &&
                y-20 <= blockedy && y+20 >= blockedy) {
                return;
                }
            }
        }
    switch(this.type) {
        case 0:     // T piece
            switch(this.rotation) {
                case 0:
                    this.blocks[1].move(-10, 10);
                    this.rotation = 1;
                    break;
                case 1:
                    this.blocks[0].move(10, 10);
                    this.rotation = 2;
                    break;
                case 2:
                    this.blocks[3].move(10, -10);
                    this.rotation = 3;
                    break;
                case 3:
                    this.blocks[0].move(-10, -10);
                    this.blocks[1].move(10, -10);
                    this.blocks[3].move(-10, 10);
                    this.rotation = 0;
                    break;
                }
            break;
        case 1:     // L piece
            switch(this.rotation) {
                case 0:
                    this.blocks[0].move(-10, 10);
                    this.blocks[2].move(10, -10);
                    this.blocks[3].move(20, 0);
                    this.rotation = 1;
                    break;
                case 1:
                    this.blocks[0].move(10, 10);
                    this.blocks[2].move(-10, -10);
                    this.blocks[3].move(0, -20);
                    this.rotation = 2;
                    break;
                case 2:
                    this.blocks[0].move(10, -10);
                    this.blocks[2].move(-10, 10);
                    this.blocks[3].move(-20, 0);
                    this.rotation = 3;
                    break;
                case 3:
                    this.blocks[0].move(-10, -10);
                    this.blocks[2].move(10, 10);
                    this.blocks[3].move(0, 20);
                    this.rotation = 0;
                    break;
                }
            break;
        case 2:     // J piece
            switch(this.rotation) {
                case 0:
                    this.blocks[0].move(-10, 10);
                    this.blocks[2].move(10, -10);
                    this.blocks[3].move(0, -20);
                    this.rotation = 1;
                    break;
                case 1:
                    this.blocks[0].move(10, 10);
                    this.blocks[2].move(-10, -10);
                    this.blocks[3].move(-20, 0);
                    this.rotation = 2;
                    break;
                case 2:
                    this.blocks[0].move(10, -10);
                    this.blocks[2].move(-10, 10);
                    this.blocks[3].move(0, 20);
                    this.rotation = 3;
                    break;
                case 3:
                    this.blocks[0].move(-10, -10);
                    this.blocks[2].move(10, 10);
                    this.blocks[3].move(20, 0);
                    this.rotation = 0;
                    break;
                }
            break;
        case 3:     // I piece
            switch(this.rotation) {
                case 0:
                    this.blocks[0].move(10, 10);
                    this.blocks[2].move(-10, -10);
                    this.blocks[3].move(-20, -20);
                    this.rotation = 1;
                    break;
                case 1:
                    this.blocks[0].move(-10, -10);
                    this.blocks[2].move(10, 10);
                    this.blocks[3].move(20, 20);
                    this.rotation = 0;
                    break;
                }
            break;
        case 4:     // Z piece
            switch(this.rotation) {
                case 0:
                    this.blocks[0].move(-10, 10);
                    this.blocks[2].move(-10, -10);
                    this.blocks[3].move(0, -20);
                    this.rotation = 1;
                    break;
                case 1:
                    this.blocks[0].move(10, -10);
                    this.blocks[2].move(10, 10);
                    this.blocks[3].move(0, 20);
                    this.rotation = 0;
                    break;
                }
            break;
        case 5:     // S piece
            switch(this.rotation) {
                case 0:
                    this.blocks[0].move(10, 10);
                    this.blocks[2].move(10, -10);
                    this.blocks[3].move(0, -20);
                    this.rotation = 1;
                    break;
                case 1:
                    this.blocks[0].move(-10, -10);
                    this.blocks[2].move(-10, 10);
                    this.blocks[3].move(0, 20);
                    this.rotation = 0;
                    break;
                }
            break;
        case 6:     // O piece
            break;
        }
    }
Piece.prototype.fall = function() {
    return this.move(0, 10);
    }
Piece.prototype.live = function() {
    if (!this.living) return;
    bottom = 0;
    for (var i=0; i<this.blocks.length; i++) {
        var y = this.blocks[i].y;
        if (y > bottom) bottom = y;
        }
    if (bottom > 130) {
        this.die();
        return;
        }
    if (this.fall()) {
        if (Math.random() > .5) this.rotate();
        if (Math.random() > .3) {
            switch (Math.floor((Math.random()*2) + .5)) {
                case 0:
                    this.move(10, 0);
                    break;
                case 1:
                    this.move(-10, 0);
                    break;
                }
            }
        }
    }
Piece.prototype.die = function() {
    //this.despawn();
    window.pieceCount--;
    var idx = window.livePieces.indexOf(this);
    window.livePieces.splice(idx, 1);
    this.living = 0;
    for (var i=0; i<this.blocks.length; i++) {
        window.deadBlocks.push(this.blocks[i]);
        }
    }
Piece.prototype.checkCollision = function(dx, dy) {
    for (var i=0; i<this.blocks.length; i++) {
        for (var j=0; j<window.deadBlocks.length; j++) {
            b1 = this.blocks[i];
            x1 = parseInt(b1.x)+dx;
            y1 = parseInt(b1.y)+dy;
            b2 = window.deadBlocks[j];
            x2 = parseInt(b2.x);
            y2 = parseInt(b2.y);
            if (x1==x2 && y1==y2) {
                if(dx==0 && dy==10) {
                    this.die();
                    }
                return true;
                }
            }
        }
    return false;
    }

function spawnRandomPiece() {
    var type = Math.floor((Math.random() * 6) + .5);
    var x = Math.floor((Math.random() * 15) + .5) * 10;
    var piece = new Piece(type, x, -30);
    piece.spawn();
    return piece;
    }

function tick() {
    var now = Math.floor(new Date().getTime()/1000);
    /* spawn a new piece */
    if(window.pieceCount == 0) {
        window.livePieces.push(spawnRandomPiece());
        window.pieceCount++;
        }
    /* every tick (.5s) */
    for (var i=0; i<window.livePieces.length; i++) {
        var p = window.livePieces[i];
        p.live();
        }
    /* game over */
    for (var i=0; i<window.deadBlocks.length; i++) {
        if (window.deadBlocks[i].y <= 0) {
            clearInterval(window.tetIntvID);
            }
        }
    }

window.blockID = 0;
window.pieceCount = 0;
window.livePieces = [];
window.deadBlocks = [];

if (window.location.href.indexOf('?') == -1) {
    window.tetIntvID = window.setInterval(function(){tick()}, 500);
    }
