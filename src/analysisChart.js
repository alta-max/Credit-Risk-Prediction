const analysisBtn = document.getElementById('anyl_btn');

function getData()
{
    var filePath = document.getElementById("csvFileInput").files[0].path;
    const { spawn } = require('child_process');
    const pytonProcess = spawn('python',["python/getData.py",filePath]);
    pytonProcess.stdout.on('data',(data)=>{
        var stringData_chart = data.toString();
        var jsonData_chart = JSON.parse(stringData_chart);
        console.log(jsonData_chart);
    });
}

analysisBtn.addEventListener('click', function(){
    getData();
});