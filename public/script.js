document.getElementById("diaryButton").addEventListener("click", function() {
    fetch("http://127.0.0.1:8000/diary")
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Преобразование ответа в JSON
    })
    .then(data => {
        // Очищаем таблицу перед добавлением новых данных
        const tbody = document.getElementById("diaryTable").getElementsByTagName('tbody')[0];
        tbody.innerHTML = "";
        
        // Добавляем строку в таблицу из полученных данных
        const newRow = document.createElement("tr");
        newRow.innerHTML = `
            <td>${data.name}</td>
            <td>${data.grade}</td>
            <td>${data.date}</td>
        `;
        tbody.appendChild(newRow);
    })
    .catch(error => {
        // Обработка ошибок
        console.error('There has been a problem with your fetch operation:', error);
    });
});
