var rootStyle = getComputedStyle(document.querySelector(':root'));
var joinBtn = document.getElementById("join-project");
var participantCount = document.getElementById("participant-number");
var page = window.location.pathname.split("/").pop();

try {
	joinBtn.addEventListener('click', e => {
		fetch(`/api/v1/participate?project_id=${page}`).then(response => {
			joinBtn.setAttribute('joined', "true");
			participantCount.innerHTML = (parseInt(participantCount.innerHTML)+1).toString();
		});
	});
} catch (error) {
	console.log("Join Button Not Available");
}


var dates = document.querySelectorAll('.convert-date');

for (var i = 0; i < dates.length; i++) {
	str = dates[i].innerHTML.split("-");
	year = parseInt(str[0]);
	month = parseInt(str[1])-1;
	day = parseInt(str[2])+1;
	
	var completeDate = new Date(Date.UTC(year, month, day));
	const options = {year: 'numeric', month: 'long', day: 'numeric' };
	dates[i].innerHTML = completeDate.toLocaleDateString(undefined, options);
}


var participants = document.querySelectorAll(".participant");

participants.forEach(element => {
	element.addEventListener('click', e => {
		var participantName = e.target.getAttribute("participant");
		fetch(`/api/v1/remove/${page}?remove=${participantName}`)
			.then(response => response.json())
			.then(data => {
				if (data["status"] == "success") {
					e.target.parentElement.parentElement.remove();
			}
		});
	});
});