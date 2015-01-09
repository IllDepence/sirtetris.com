document.querySelector('#graph').innerHTML='';
var st = document.createElement('link');
st.rel = 'stylesheet';
st.type = 'text/css';
st.href = 'static/img/projects/d3graph.css'
document.querySelector('head').appendChild(st);

function loadd3(callback) {
    var d3 = document.createElement('script');
    d3.src='static/img/projects/d3/d3.js';
    d3.charset='utf-8';
    d3.async = true;
    d3.onreadystatechange = d3.onload = function() {
        var state = d3.readyState;
        if (!callback.done && (!state || /loaded|complete/.test(state))) {
            callback.done = true;
            callback();
        }
    };
    document.querySelector('head').appendChild(d3);
}

function refub(data) {
    return {
        date: parseDate(data[0]),
        kanji: data[1],
        words: data[2],
        rate: data[3]
        }
    }
function parseData(rows) {
    var data = dsv.parseRows(rows, refub);
    show(data);
    }
function show(data) {
    x.domain(d3.extent(data, function(d) { return d.date; }));
    var wmax = d3.max(data.map(function(data) { return +data.words }))
    var kmax = d3.max(data.map(function(data) { return +data.kanji }))
    var rmax = d3.max(data.map(function(data) { return +data.rate }))
    y0.domain([0, wmax]);
    y1.domain([0, rmax]);
    var kline = d3.svg.line()
                      .x(function(d) { return x(d.date); })
                      .y(function(d) { return y0(d.kanji); });
    var wline = d3.svg.line()
                      .x(function(d) { return x(d.date); })
                      .y(function(d) { return y0(d.words); });
    var rline = d3.svg.line()
                      .x(function(d) { return x(d.date); })
                      .y(function(d) { return y1(d.rate); });
    svg.append('g')
       .attr('class', 'x axis')
       .attr('transform', 'translate(0,' + height + ')')
       .call(xAxis)
       .selectAll('text')
         .style('text-anchor', 'end')
         .attr('transform', 'rotate(-90)')
         .attr('dy', '-5px')
         .attr('dx', '-9px');
    svg.append('g')
       .attr('class', 'y axis')
       .attr('transform', 'translate(' + width + ', 0)')
       .call(yAxisRight);
    svg.append('g')
       .attr('class', 'y axis secondary')
       .attr('transform', 'translate(0, ' + height + ')')
       .attr('transform', 'rotate(90)')
       .call(yAxisLeft)
       .selectAll('text')
         .style('text-anchor', 'end')
         .attr('transform', 'rotate(-90)')
         .attr('dy', '-5px')
         .attr('dx', '-9px');
    var line = svg.append('g')
                  .attr('class', 'line')
    line.append('path')
        .attr('class', 'kanji')
        .attr('d', kline(data));
    line.append('path')
        .attr('class', 'words')
        .attr('d', wline(data));
    line.append('path')
        .attr('class', 'rate secondary')
        .attr('d', rline(data));
    var focus = svg.append('g')
                   .attr('class', 'focus')
                   .style('display', 'none');
    var fline = focus.append('line')
                     .attr('y1', height-1)
                     .attr('y2', 0);
    var vlinek = focus.append('line')
                      .attr('x2', width-1)
                      .attr('class', 'kanji');
    var vlinew = focus.append('line')
                      .attr('x2', width-1)
                      .attr('class', 'words');
    var valw = svg.append('text')
                  .attr('x', 20)
                  .attr('y', 15)
                  .attr('class', 'wordstext')
                  .text('words: ' + wmax);
    var valk = svg.append('text')
                  .attr('x', 22)
                  .attr('y', 32)
                  .attr('class', 'kanjitext')
                  .text('kanji: ' + kmax);
    var valr = svg.append('text')
                  .attr('x', 22)
                  .attr('y', 49)
                  .attr('class', 'secondary')
                  .text('kanji/month: -');
    svg.append('rect')
       .attr('class', 'overlay')
       .attr('width', width)
       .attr('height', height)
       .on('mousemove', mousemove)
       .on('mouseover', function() { focus.style('display', null); })
       .on('mouseout', function() { focus.style('display', 'none');
                                    valw.text('words: ' + wmax);
                                    valk.text('kanji: ' + kmax);
                                    valr.text('kanji/month: -'); });
    dates = data.map(function(d) { return d.date });
    function mousemove() {
        var mx = d3.mouse(this)[0],
            dx = x.invert(mx),
            idx = d3.bisectLeft(dates, dx),
            kanji = data[idx].kanji,
            words = data[idx].words;
        fline.attr('x1', mx).attr('x2', mx);
        vlinek.attr('x1', mx)
              .attr('y1', y0(data[idx].kanji))
              .attr('y2', y0(data[idx].kanji));
        valk.text('kanji: ' + data[idx].kanji);
        vlinew.attr('x1', mx)
              .attr('y1', y0(data[idx].words))
              .attr('y2', y0(data[idx].words));
        valw.text('words: ' + data[idx].words);
        valr.text('kanji/month: ' + data[idx].rate);
        }
    }

loadd3(function() {

margin = {top: 6, right: 54, bottom: 64, left: 54},
    width = 700 - margin.left - margin.right,
    height = 300 - margin.top - margin.bottom;
parseDate = d3.time.format('%y%m%d').parse;
x = d3.time.scale()
          .range([0, width]);
y0 = d3.scale.linear()      // kanji & vocab
          .range([height, 0]);
y1 = d3.scale.linear()      // kanji rate
          .range([height, 0]);
color = d3.scale.category10();
xAxis = d3.svg.axis()
              .scale(x)
              .tickFormat(function(d) {
                    mo = d3.time.format('%b')
                    jo = d3.time.format('%Y')
                    if(mo(d) != 'Jan') return mo(d)
                    else return jo(d)
                    })
              .orient('bottom');
yAxisRight = d3.svg.axis()
              .scale(y0)
              .orient('right');
yAxisLeft = d3.svg.axis()
              .scale(y1)
              .orient('Left');
svg = d3.select('#graph').append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
            .append('g')
            .attr('transform', 'translate('+margin.left+','+margin.top+')');
dsv = d3.dsv(' ', 'text/plain');
d3.text('static/img/projects/kanji.dat', 'text/plain', function(text) {
    lines = text.split('\n');
    var currMonth = -1;
    var lastMonth = -1;
    var monthDelta = -1;
    for(var i=0; i<lines.length; i++) {
        if(lines[i].length==0) continue;
        var parts = lines[i].split(' ');
        var date = parseDate(parts[0]);
        var kanji = parts[1];
        var words = parts[2];
        getDeltaMonth = date.getMonth();
        if(getDeltaMonth == lastMonth) {
            }
        else {
            currMonth = getDeltaMonth;
            monthLow = kanji;
            for(var j=i; currMonth==getDeltaMonth; j++) {
                if(typeof(lines[j])=='undefined') break;
                if(lines[j].length==0) continue;
                var tparts = lines[j].split(' ');
                var tdate = parseDate(tparts[0]);
                var tkanji = tparts[1];
                currMonth = tdate.getMonth();
                monthHigh = tkanji;
                }
            monthDelta = monthHigh-monthLow;
            }
        parts.push(monthDelta)
        lines[i] = parts.join(' ');
        lastMonth = getDeltaMonth;
        }
    text = lines.join('\n');
    parseData(text);
    });

});