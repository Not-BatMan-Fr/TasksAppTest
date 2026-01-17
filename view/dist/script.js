"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
// Function to fetch and display tasks from the backend
function fetchTasks() {
    return __awaiter(this, void 0, void 0, function* () {
        // Send a GET request to our FastAPI endpoint
        const response = yield fetch('http://127.0.0.1:8000/tasks');
        const tasks = yield response.json();
        const list = document.getElementById('taskList');
        list.innerHTML = ''; // Clear current list
        // Loop through tasks and create list items
        tasks.forEach(task => {
            const li = document.createElement('li');
            li.textContent = `${task.title} - [${task.status}]`;
            list.appendChild(li);
        });
    });
}
// Function to send a new task to the backend
function addTask() {
    return __awaiter(this, void 0, void 0, function* () {
        const input = document.getElementById('taskInput');
        const title = input.value;
        if (!title)
            return;
        // Send a POST request with the task title
        yield fetch('http://127.0.0.1:8000/tasks', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title: title })
        });
        input.value = ''; // Clear input
        fetchTasks(); // Refresh the list
    });
}
// Initial load
fetchTasks();
