const table = document.getElementById("transfer-table");
const defaultData = [...table.getElementsByClassName("table-row")];
const arrow = document.getElementById("sort-arrow");
const dialog = document.getElementById("dialog");
const filesInput = document.getElementById("files-input");
const loading = document.getElementById("files-loading");
filesInput.onchange = filesInputTrigger;

function sortTable(element) {
    if(!defaultData){
        return;
    }
    let reg = new RegExp(`(\\d+)(deg)`);
    let source = element;
    if (source.getElementsByClassName("fas fa-sort-down").length > 0) {
        let tr = arrow.style.transform;
        let match = reg.exec(tr);
        if (match[1] === "0") {
            sortBy(element.getAttribute("id"), "asc");
            arrow.style.webkitTransform = "rotate(180deg)";
            arrow.style.msTransform = "rotate(180deg)";
            arrow.style.transform = "rotate(180deg)";
        } else {
            sortBy(element.getAttribute("id"), "desc");
            arrow.style.webkitTransform = "rotate(0)";
            arrow.style.msTransform = "rotate(0)";
            arrow.style.transform = "rotate(0)";
        }
    } else {
        sortBy(element.getAttribute("id"), "desc");
        arrow.style.webkitTransform = "rotate(0)";
        arrow.style.msTransform = "rotate(0)";
        arrow.style.transform = "rotate(0)";
    }
    source.appendChild(arrow);
}

function sortBy(field, type) {
    let items = Array.prototype.slice.call([...defaultData]);
    let dividedItems = divideByType(items);
    let result = [];
    dividedItems.forEach(function(item){
        if (type === "asc") {
            item.sort(function (a, b) {
                return a.querySelector("div.table-" + field + " > span").textContent.toLocaleLowerCase().localeCompare(b.querySelector("div.table-" + field + " > span").textContent.toLocaleLowerCase());
            });
        } else {
            item.sort(function (a, b) {
                return b.querySelector("div.table-" + field + " > span").textContent.toLocaleLowerCase().localeCompare(a.querySelector("div.table-" + field + " > span").textContent.toLocaleLowerCase());
            });
        }
        result.push(item);
    });
    result = [...result[0], ...result[1]];
    for (let i = 0, len = result.length; i < len; i++) {
        result[i].querySelector("div.table-index > span").textContent = i+1;
        let parent = result[i].parentNode;
        let detatchedItem = parent.removeChild(result[i]);
        parent.appendChild(detatchedItem);
    }
}

function divideByType(data) {
    let result = [[], []];
    for (let i = 0; i < data.length; i++) {
        if (data[i].querySelector("div.table-type > span").textContent === "File folder") {
            result[0].push(data[i]);
        } else {
            result[1].push(data[i]);
        }
    }
    return result
}

function showQRcode(folder, file){
    toggleDialog();
    let form = {folder: folder, file: file};
    xhr.open("POST", "/qrcode");
    xhr.responseType = 'blob';
    xhr.onload = function(){
        let response = new Blob([xhr.response], {type: 'image/png'});
        let urlCreator = window.URL || window.webkitURL;
        let imageUrl = urlCreator.createObjectURL(response);
        let namePlacement = document.getElementById("qrcode-filename");
        let imagePlacement = document.getElementById("qrcode-img");
        namePlacement.textContent = file;
        imagePlacement.src = imageUrl;
    };
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify(form));
}

function toggleDialog(){
    let qrwindow = dialog.querySelector("div#qrcode-window");
    if(dialog.className === "display-none"){
        dialog.className = "";
        qrwindow.className = "popOutOpen";
    } else {
        qrwindow.className = "popOutClose";
        setTimeout(() => {dialog.className = "display-none";}, 400)
    }
}

function download(event, element, type) {
    let sourcePath = document.getElementById("directory-input").value;
    let filePath = element.querySelector("div.table-name > span").textContent;
    if(event.target.getAttribute("id") === "qrcode" ||
        (event.target.className === "table-barcode" && event.target.querySelector("i#qrcode"))){
        showQRcode(sourcePath, filePath);
        return;
    }
    if (type === "File folder") {
        window.location.href = 'transfer?folder=' + (sourcePath === "\\" ? "" : sourcePath)  + "\\" + filePath;
    }
    window.open('download?folder=' + sourcePath + "&file=" + filePath, "Downloading file...");
}

function filesInputTrigger(event){
    const uploadText = document.querySelector("label[for=files-input] > span > span");
    if(event.target.files.length === 1){
        uploadText.textContent = event.target.files.length + " file selected"
    } else if(event.target.files.length > 1) {
        uploadText.textContent = event.target.files.length + " files selected"
    } else {
        uploadText.textContent = "Choose a file..."
    }
}

function upload(){
    uploadFile([...filesInput.files]);
}

function abortUpload() {
    if(xhr.status === 0){
        xhr.abort();
    } else {
        toggleLoading()
    }
}

function uploadFile(files){
    let fileCount = loading.querySelector("div#progress > span#progress-counts");
    let abortButton = loading.querySelector("div#files-abort > span");
    let span = loading.querySelector("span");
    let form = new FormData();
    abortButton.textContent = "Abort";
    if(files.length === 1){
        fileCount.textContent = files.length + " file uploading...";
    } else {
        fileCount.textContent = files.length + " files uploading...";
    }
    files.map(file => form.append("files", file));
    toggleLoading();
    xhr.upload.onprogress = onProgressTrigger;
    xhr.upload.onerror = onErrorTrigger;
    xhr.upload.onabort = onAbortTrigger;
    xhr.open("POST", "/upload");
    xhr.onload = function () {
        if(xhr.status === 200){
            abortButton.textContent = "Close";
            if(files.length === 1){
                fileCount.textContent = files.length + " file uploaded!";
            } else {
                fileCount.textContent = files.length + " files uploaded!";
            }
            span.textContent = "";
            console.log("Uploaded!");
        } else {
            console.log("Hi")
        }
    };
    xhr.send(form);
}

function onProgressTrigger(event){
    let span = loading.querySelector("span");
    let progressBar = loading.querySelector("div#progress-bar");
    let percent = ((event.loaded / event.total) * 100).toFixed(2);
    let size_loaded = (event.loaded / 1048576).toFixed(2);
    let size_full = (event.total / 1048576).toFixed(2);
    progressBar.style.width = percent + "%";
    span.textContent = percent + "%" + " (" + size_loaded + " MB of " + size_full + " MB)";
}

function onErrorTrigger(){
    toggleLoading();
}

function onAbortTrigger(){
    toggleLoading();
}

function toggleLoading() {
    let uploadButton =  document.querySelector("input#upload");
    let uploadInput =  document.querySelector("input#files-input");
    let uploadLabel =  document.querySelector("label[for=files-input]");
    if(loading.className === "display-none"){
        uploadButton.disabled = true;
        uploadInput.disabled = true;
        loading.className = "slideDownOpen";
    } else{

        loading.className = "slideDownClose";
        setTimeout(() => {
            loading.className = "display-none";
            uploadButton.disabled = false;
            uploadInput.disabled = false;
        }, 400);
    }
}