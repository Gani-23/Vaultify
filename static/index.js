var eventSource = new EventSource('/stream');
eventSource.onmessage = function (event) {
    var data = JSON.parse(event.data);
    var cpuPercent = data.cpu_percent;
    var cpuElement = document.getElementById('cpu_percent');

    cpuElement.innerText = 'CPU ' + cpuPercent + '%';

    if (cpuPercent >= 80) {
        alert('Cpu exeeds 80%')

    } else if (cpuPercent >= 90) {
        alert('Cpu exeeds 90%')
    }
    else {
        return
    }
};

setTimeout(function () {
    var alertElement = document.querySelector('.alert');
    if (alertElement) {
        alertElement.remove();
    }
}, 3000);

function showSuccessNotification() {

    alert("Sucessfully uploaded to the server!, you'd be rediredted to output page shortly. if empty please make sure to add config properly");
}