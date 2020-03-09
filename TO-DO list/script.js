let addTaskButton= document.querySelector('.addTaskButton');
var listTasks = document.getElementById('listTasks');


addTaskButton.onclick = function() {
	let newTask = document.querySelector('.taskDescription').value;
	alert('Вы добавили новую задачу: ' + newTask);
	var entry = document.createElement('li', checked = "False");
	entry.appendChild(document.createTextNode(newTask));
	listTasks.appendChild(entry);
	}

