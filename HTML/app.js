var decideButton = document.querySelector(".decide-button");
var item = document.querySelector("#choice #plan");
var loggedIn = false;

var BASE_URL = "https://peaceful-cove.herokuapp.com/"

flagFormOpen = false;
function closeForm() {
	document.getElementById("loginForm").style.display = "none";
	flagFormOpen = false;
}
function openFormNew() {
	if (flagFormOpen== false) {
		document.getElementById("newForm").style.display = "block";
		flagFormOpen = true;
	}
}
function closeFormNew() {
	document.getElementById("newForm").style.display = "none";
	flagFormOpen = false;
}


var loadPlans = function () {
	fetch(BASE_URL + "plans", {
		//sends cookies
		credentials: "include"
	}).then(function (response) {
		// put note tips here load resource: restaurants here
		if (response.status == 401){
			return;
		}
		loggedIn = true;
		document.getElementById("loginbutton").innerHTML = "Logout";
		response.json().then(function (data){
			console.log("data recieved from server", data);
			//display data values in the DOM
			var dataList = document.querySelector("#dataList");
			dataList.innerHTML = ""
			data.forEach(function (plan){
				//append each plan to a new element in the DOM

				// li tag: contains everything about one plan
				var newListItem = document.createElement("li");

				// h3 tag: contains the title
				var titleHeading = document.createElement("h3");
				titleHeading.innerHTML = plan.name;
				newListItem.appendChild(titleHeading);

				// div tag: contains the description
				var descriptionDiv = document.createElement("div");
				descriptionDiv.innerHTML = plan.description;
				newListItem.appendChild(descriptionDiv);

				var dateDiv = document.createElement("div");
				dateDiv.innerHTML = plan.date;
				newListItem.appendChild(dateDiv);

				var ratingDiv = document.createElement("div");
				ratingDiv.innerHTML = plan.rating;
				newListItem.appendChild(ratingDiv);

				// button tag: the delete button
				var deleteButton = document.createElement("button");
				deleteButton.innerHTML = "Delete";
				deleteButton.onclick = function() {
					console.log("delete clicked:", plan.id);
					if (confirm("Are you sure you want to delete this plan?")){
						deletePlan(plan.id);
					}
				};

				var editButton = document.createElement("button");
				editButton.innerHTML = "Edit";
				editButton.onclick = function() {
					console.log("update clicked:", plan.id);
					if (confirm("You are about to update with text in field, continue?")){
						editPlan(plan.name, plan.description, plan.date, plan.rating, plan.id);
					}
				};

				newListItem.appendChild(deleteButton);
				newListItem.appendChild(editButton);
				dataList.appendChild(newListItem);
			});
		});
	});
};

loadPlans();

var newAccount = document.querySelector(".New-Account-Button");
newAccount.onclick = function() {

	var newFirstName = document.querySelector("#userFirstName").value;
	var newLastName = document.querySelector("#userLastName").value;
	var newUsername = document.querySelector("#userUsername").value;
	var newPassword = document.querySelector("#userPassword").value;

	var bodyStr = "username=" + encodeURIComponent(newUsername);
	bodyStr += "&password=" + encodeURIComponent(newPassword);
	bodyStr += "&firstname=" + encodeURIComponent(newFirstName);
	bodyStr += "&lastname=" + encodeURIComponent(newLastName);

	fetch(BASE_URL + "users", {
		// request parameters:
		method: "POST",
		//sends cookies
		credentials: "include",
		body: bodyStr,
		headers: {
			"Content-Type": "application/x-www-form-urlencoded"
		}
	}).then(function (response) {
		if (response.status == 422){
			alert("bad email/password");
		}else {
			alert("Account created!")
			closeFormNew();
		}
	});
};

function openForm() {
	if (loggedIn == false) {
		if (flagFormOpen == false) {
			document.getElementById("loginForm").style.display = "block";
			flagFormOpen = true;
			return;
		}
	}
	console.log("logging out")

	fetch(BASE_URL+ "logoutUsers", {
		// request parameters:
		method: "POST",
		credentials: "include"
	}).then(function (response) {
		location.reload();
	});
}

var Login = document.querySelector(".Login-Button");
Login.onclick = function() {
	var loginUsername = document.querySelector("#loginUsername").value;
	var loginPassword = document.querySelector("#loginPassword").value;

	var bodyStr = "username=" +encodeURIComponent(loginUsername);
	bodyStr += "&password=" + encodeURIComponent(loginPassword);

	fetch(BASE_URL + "sessions", {
		// request parameters:
		method: "POST",
		//sends cookies
		credentials: "include",
		body: bodyStr,
		headers: {
			"Content-Type": "application/x-www-form-urlencoded"
		}
	}).then(function (response) {
		if (response.status == 401){
			alert("Wrong password/username")
		}else {
			closeForm();
			loadPlans();
		}
	});
}


var addButton = document.querySelector(".add-button");
addButton.onclick = function () {

	var newPlanName = document.querySelector("#new-plan-name").value;
	var newPlanDescription = document.querySelector("#new-plan-description").value;
	var newPlanDate = document.querySelector("#new-plan-date").value;
	var newPlanRating = document.querySelector("#new-plan-rating").value;

	var bodyStr = "name=" + encodeURIComponent(newPlanName);
	bodyStr += "&description=" + encodeURIComponent(newPlanDescription);
	bodyStr += "&date=" + encodeURIComponent(newPlanDate);
	bodyStr += "&rating=" + encodeURIComponent(newPlanRating);

	fetch(BASE_URL+"plans", {
		// request parameters:
		method: "POST",
		//sends cookies
		credentials: "include",
		body: bodyStr,
		headers: {
			"Content-Type": "application/x-www-form-urlencoded"
		}
	}).then(function (response) {
		//handle the response
		console.log("Button Clicked");
		//call the GET after user clicks button
		loadPlans();
		//set text field to empty
		document.getElementById('new-plan-name').value = ""
		document.getElementById('new-plan-description').value = ""
		document.getElementById('new-plan-date').value = ""
		document.getElementById('new-plan-rating').value = ""

	});
};
// inputField.value

var deletePlan = function (planID) {
	fetch(BASE_URL + "plans/"+ planID, {
		method: "DELETE",
		//sends cookies
		credentials: "include"
	}).then(function (response) {
		console.log(planID, "deleted...");
		loadPlans();
	});
};

var editPlan = function (plan_name, plan_description, plan_date, plan_rating, plan_id) {
	globalplanID = plan_id;
	document.getElementById('new-plan-name').value = plan_name;
	document.getElementById('new-plan-description').value = plan_description;
	document.getElementById('new-plan-date').value = plan_date;
	document.getElementById('new-plan-rating').value = plan_rating;
};

var updateButton = document.querySelector(".update-button");
updateButton.onclick = function () {
	var newPlanName = document.querySelector("#new-plan-name").value;
	var newPlanDescription = document.querySelector("#new-plan-description").value;
	var newPlanDate = document.querySelector("#new-plan-date").value;
	var newPlanRating = document.querySelector("#new-plan-rating").value;

	var bodyStr = "name=" + encodeURIComponent(newPlanName);
	bodyStr += "&description=" + encodeURIComponent(newPlanDescription);
	bodyStr += "&date=" + encodeURIComponent(newPlanDate);
	bodyStr += "&rating=" + encodeURIComponent(newPlanRating);

	console.log(bodyStr);
	fetch(BASE_URL + "plans/"+ globalplanID, {
		// request parameters:
		method: "PUT",
		//sends cookies
		credentials: "include",
		body: bodyStr,
		headers: {
			"Content-Type": "application/x-www-form-urlencoded"
		}
	}).then(function (response) {
		console.log(globalplanID, "updated...");
		loadPlans();

		//set text field to empty
		document.getElementById('new-plan-name').value = ""
		document.getElementById('new-plan-description').value = ""
		document.getElementById('new-plan-date').value = ""
		document.getElementById('new-plan-rating').value = ""
	});
};