const navbar = document.getElementById("navbar");
const navbarContent = `
<a href="/">
	<img id="nav-logo" src="/static/images/demo.png">
	<span>Pine</span>
</a>
<div id="navigation-menu-container">
	<ul>
		<li><a href="/discover">Discover</a></li>
		<li><a href="/dashboard">Dashboard</a></li>
		<!-- <li><a href="/logout">Logout</a></li> -->
	</ul>
	<div id="user-menu-btn">
		<img src="${typeof(profilePicture) == "undefined" ? '/undefined' : profilePicture}" alt="User Menu">
	</div>
	<div id="user-menu" style="pointer-events: none">
		<ul>
			<li><a href="/settings">Settings</a></li>
			<li><a href="/logout">Logout</a></li>
		</ul>
	</div>
</div>
`;

const navbarPlainContent = `
<a href="/">
	<img id="nav-logo" src="/static/images/logo.png">
	<span>Pine</span>
</a>
<div id="navigation-menu-container">
	<ul>
		<li><a href="/login">Login</a></li>
	</ul>
	<div id="user-menu-btn">
		<a href="/register">Register</a>
	</div>
</div>
`;

if (navbar.hasAttribute('plain')) {
	navbar.innerHTML = navbarPlainContent;
} else {
	navbar.innerHTML = navbarContent;
	document.getElementById("user-menu-btn").addEventListener('click', e => {
		document.getElementById("user-menu").style.display = "block";
		document.addEventListener('click', e => {
			if (!(document.getElementById('user-menu').contains(e.target) || document.getElementById("user-menu-btn").contains(e.target))) {
				document.getElementById("user-menu").style.display = "none";
			}
		});
	});
}