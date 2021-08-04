const predictBtn = document.getElementById('pred_btn');
predictBtn.onclick = getReport;

const download = function(data){
    const blob = new Blob([data],{type:'text/csv'});
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.setAttribute('hidden','');
    a.setAttribute('href',url);
    a.setAttribute('download','download.csv');
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

const objectToCsv = function(data){
    const csvRows = [];
    const headers = Object.keys(data[0]);
    csvRows.push(headers.join(','));

    for(const row of data)
    {
        const values = headers.map(header=>{
            const escaped = (''+row[header]).replace(/"/g,'\\"');
            return `"${escaped}"`;
        });
        csvRows.push(values.join(','));
    }
    return csvRows.join('\n');
};

function getReport()
{
    var filePath = document.getElementById("csvFileInput").files[0].path;
    const { spawn } = require('child_process');
    const pytonProcess = spawn('python',["python/predict.py",filePath]);
    pytonProcess.stdout.on('data',(data)=>{
        var stringData = data.toString();
        var jsonData = JSON.parse(stringData);
        const csvData = objectToCsv(jsonData);
        download(csvData);
    });
}