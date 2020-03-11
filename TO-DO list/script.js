window.onload = function () {
	let listTasks = [];
	if (localStorage.getItem('superKey') !== undefined) {
		listTasks = JSON.parse(localStorage.getItem('superKey'));
		printTasks();
	}
	document.getElementById('addButton').onclick = function () {
		let newTask = document.getElementById('taskDescription').value;
		let temp = {};
		temp.todo = newTask;
		temp.check = false;
		listTasks[listTasks.length] = temp;
		printTasks();
		localStorage.setItem('superKey', JSON.stringify(listTasks));
		document.getElementById('taskDescription').value = '';
	};
	document.getElementById('clearAll').onclick = function () {
		listTasks = [];
		printTasks();
		localStorage.setItem('superKey', JSON.stringify(listTasks));
	}


	function printTasks() {
		let out = '';
		for (let task in listTasks){
			if (listTasks[task].check === true){
				out += '<input id="flag" type="checkbox" checked>';
			}
			else {
				out += '<input id="flag" type="checkbox">';
			}
			out += listTasks[task].todo + '<br>';

		}
		document.getElementById('output').innerHTML = out;
	}

};

