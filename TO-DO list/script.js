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


	function printTasks() {
		let out = '';
		for (let i = 0;i < listTasks.length; i++){
			if (listTasks[i].check == true){
				out += '<input id="flag" type="checkbox" checked>';
			}
			else {
				out += '<input id="flag" type="checkbox">';
			}
			out += listTasks[i].todo + '<br>';

		}
		document.getElementById('output').innerHTML = out;
	}

};

