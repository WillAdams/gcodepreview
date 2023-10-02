//!OpenSCAD

module oopengcodefile(fn) {
	popengcodefile(fn);
}

module oclosegcodefile() {
	pclosegcodefile();
}

module owritecomment(comment) {
	writeln("(",comment,")");
}

module owriteone(first) {
	writeln(first);
}

module owritetwo(first, second) {
	writeln(first, second);
}

module owritethree(first, second, third) {
	writeln(first, second, third);
}

module owritefour(first, second, third, fourth) {
	writeln(first, second, third, fourth);
}

module owritefive(first, second, third, fourth, fifth) {
	writeln(first, second, third, fourth, fifth);
}

module owritesix(first, second, third, fourth, fifth, sixth) {
	writeln(first, second, third, fourth, fifth, sixth);
}

module owriteseven(first, second, third, fourth, fifth, sixth, seventh) {
	writeln(first, second, third, fourth, fifth, sixth, seventh);
}

module owriteeight(first, second, third, fourth, fifth, sixth, seventh,eighth) {
	writeln(first, second, third, fourth, fifth, sixth, seventh,eighth);
}

module owritenine(first, second, third, fourth, fifth, sixth, seventh, eighth, ninth) {
	writeln(first, second, third, fourth, fifth, sixth, seventh, eighth, ninth);
}

module owriteten(first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth) {
	writeln(first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth);
}

module owriteeleven(first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh) {
	writeln(first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh);
}

module owritetwelve(first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh, twelfth) {
	writeln(first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh, twelfth);
}

module owritethirteen(first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh, twelfth, thirteenth) {
	writeln(first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh, twelfth, thirteenth);
}

module osetupstock(stocklength, stockwidth, stockthickness, zeroheight, stockorigin) {
    psetupstock(stocklength, stockwidth, stockthickness, zeroheight, stockorigin);
}

//module osettool(tn){psettool(tn);}

module osettool(tn){
psettool(tn);}

function current_tool() = pcurrent_tool();
//function current_tool() = pcurrent_tool();


//function xpos() = pxpos();