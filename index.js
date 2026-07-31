
function generating(){
    const generate = document.getElementById('generate-btn')
    generate.setAttribute("class", "loading")
    generate.innerHTML = "<span></span>&nbsp&nbspGenerating your QrCode..."
}

function downloading(){
    const download = document.getElementById('download')
    download.setAttribute('class','loading')
    download.innerHTML = "<span></span>&nbsp&nbspDownloading your QrCode..."
}