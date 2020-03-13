window.onload = function () {
	let listTasks = [];
	if (localStorage.getItem('superKey') != undefined) {
		listTasks = JSON.parse(localStorage.getItem('superKey'));
		printTasks();
	}
	document.getElementById('addButton').onclick = function () {
		let newTask = document.getElementById('taskDescription').value;
		if (newTask.length == 0){
			alert("You have not entered anything, first enter in the input field.");
		}
		else {
			let temp = {};
			temp.todo = newTask;
			temp.check = false;
			listTasks[listTasks.length] = temp;
			printTasks();
			localStorage.setItem('superKey', JSON.stringify(listTasks));
			document.getElementById('taskDescription').value = '';
		}
	}

	document.getElementById('clearAll').onclick = function () {
		listTasks = [];
		printTasks();
		localStorage.setItem('superKey', JSON.stringify(listTasks));
	}

	function checkTask() {
		let checkboxes = document.getElementsByClassName("Checkboxes");
		for (let i = 0; i < listTasks.length; i++){
			if (checkboxes[i].checked){
				listTasks[i].check = true;
			}
			else {
				listTasks[i].check = false;
			}
			localStorage.setItem('superKey', JSON.stringify(listTasks));
		}
	}
	document.getElementById('output').onclick = function (e) {
		if (e.target.classList.contains("Checkboxes")){
			checkTask();
			printTasks();
		}
	}

	function printTasks() {
		let out = '';
		for (let i = 0; i < listTasks.length; i++){
			if (listTasks[i].check == true){
				out += '<input id="' + String(i)+ '" class="Checkboxes" type="checkbox" checked>';
				out += '<s>' + listTasks[i].todo + '</s><br>';

			}
			else {
				out += '<input id="' + String(i)+ '" class="Checkboxes" type="checkbox">' + listTasks[i].todo + '<br>';
			}
		}
		document.getElementById('output').innerHTML = out;
	}


	document.getElementById('delButton').onclick = function () {
		let i = 0;
		while (i < listTasks.length){
			if (listTasks[i].check == true){
				listTasks.splice(i, 1);
				// console.log(listTasks);
			}
			else {
				i++;
			}
		}
		printTasks();
		localStorage.setItem('superKey', JSON.stringify(listTasks));
		document.getElementById('taskDescription').value = '';
	}
}


