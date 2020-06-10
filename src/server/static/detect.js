
const detectUrl = window.location.origin + '/detect';
const updateUrl = window.location.origin + '/train';

function updateModel() {
    console.log("updating model...")
    
    // Draw posted image
    var img = new Image()

    let xhr = new XMLHttpRequest();
    var form_data = new FormData($('#updateModel')[0]);
    xhr.open('POST', updateUrl, true);
    xhr.onload = function () {
        if (this.status === 200) {
            console.log(this.response)
            images = this.response.split(',')
            images.forEach(function(image){
                var img = new Image()
                img.src = "data:image/jpeg;base64," + image
                img.style = "max-width:250px;max-height:250px"
                document.getElementById("srcImg").appendChild(img)
            })
        }
        else {
            console.log("HTTP failure, error code: " + this.status)
        }
    }
    xhr.send(form_data)
    //exCanvas.toBlob(postExamplesFile, 'image/jpeg');
}
function searchImage() {
    console.log("Searching image")
    
    let xhr = new XMLHttpRequest();
    xhr.open('POST', detectUrl, true);
    xhr.onload = function () {
        if (this.status === 200) {
            console.log(this.response)
            images = this.response.split(',')
            images.forEach(function(image){
                var img = new Image()
                img.src = "data:image/jpeg;base64," + image
                img.style = "max-width:150px;max-height:150px"
                document.getElementById("foundImg").appendChild(img)
            })
        }
        else {
            console.log("HTTP failure, error code: " + this.status)
        }
    }
    xhr.send()

}

// EVENT

window.onload = () => {

    document.getElementById("upload-file-btn").onclick = () => {
        
        updateModel();
        return false;
    };
    document.getElementById("searchImage").onclick = () => {
        
        searchImage();
        return false;
    };
};