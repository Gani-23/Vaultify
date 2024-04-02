var eventSource = new EventSource('/stream');
eventSource.onmessage = function(event) {
    var data = JSON.parse(event.data);
    var cpuPercent = data.cpu_percent;
    var cpuElement = document.getElementById('cpu_percent');
    
    cpuElement.innerText = 'CPU ' + cpuPercent + '%';
    
    if (cpuPercent >= 80) {
       alert('Cpu exeeds 80%')
    
    } else if (cpuPercent >= 90) {
        alert('Cpu exeeds 90%')
    }
    else{
        return
    }
};

// Function to remove the alert message after 3 seconds
setTimeout(function() {
    var alertElement = document.querySelector('.alert');
    if (alertElement) {
        alertElement.remove();
    }
}, 3000);