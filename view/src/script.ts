// Define the shape of a Task based on our TDD
interface Task {
    id: string;
    title: string;
    status: string;
}

// Function to fetch and display tasks from the backend
async function fetchTasks(): Promise<void> {
    // Send a GET request to our FastAPI endpoint
    const response: Response = await fetch('http://127.0.0.1:8000/tasks');
    const tasks: Task[] = await response.json();
    
    const list = document.getElementById('taskList') as HTMLUListElement;
    list.innerHTML = ''; // Clear current list

    // Loop through tasks and create list items
    tasks.forEach(task => {
        const li: HTMLLIElement = document.createElement('li');
        li.textContent = `${task.title} - [${task.status}]`;
        list.appendChild(li);
    });
}

// Function to send a new task to the backend
async function addTask(): Promise<void> {
    const input = document.getElementById('taskInput') as HTMLInputElement;
    const title: string = input.value;

    if (!title) return;

    // Send a POST request with the task title
    await fetch('http://127.0.0.1:8000/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: title })
    });

    input.value = ''; // Clear input
    fetchTasks(); // Refresh the list
}

// Initial load
fetchTasks();