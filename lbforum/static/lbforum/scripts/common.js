function getExt(file){
	return (-1 !== file.indexOf('.')) ? file.replace(/.*[.]/, '') : '';
}

function isImg(file) {
	ext = getExt(file);
	return ext && /^(jpg|png|jpeg|gif)$/.test(ext.toLowerCase());
}
