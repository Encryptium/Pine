function readTextFile(fileName) {
	var file = new XMLHttpRequest();
	file.open("GET", fileName, false);
	file.send(null);
	return file.responseText;
}

const guidePages = readTextFile('/static/guide_pages.txt').split("\n");
const searchInput = document.getElementById("search");
const searchSuggestions = document.getElementById("suggestions");

searchInput.addEventListener('keyup', e => {
	searchSuggestions.innerHTML = "";
	var searchQuery = searchInput.value.toLowerCase();
	
	if (searchQuery == "") {
		return;
	}
	
	for (var i = 0; i < guidePages.length; i++) {
		if (guidePages[i].toLowerCase().includes(searchQuery)) {
			searchSuggestions.innerHTML += `<a href="/guide/${guidePages[i].toLowerCase().replace(/\ /g, "-")}"><div>${guidePages[i]}</div></a>`;
		}
	}
});

document.addEventListener('click', e => {
	if (document.activeElement != searchInput) {
		searchSuggestions.innerHTML = "";
	}
});